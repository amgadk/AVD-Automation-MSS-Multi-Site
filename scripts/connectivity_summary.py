#!/usr/bin/env python3
"""
Reads an ANTA NRFU JSON report (anta nrfu json -o <file>) and prints a
department-to-department connectivity summary: for each (campus, source
department, destination department) triple, whether ICMP/TCP/UDP/Telnet
passed across every host-pair ANTA actually tested for that combination.

Every test result is accounted for, no matter how it failed. ANTA marks a
result "error" (instead of "failure") whenever the probe itself couldn't run
- eg. the underlying eAPI command timed out or errored before our test()
code ever set its normal "from X to Y" description (see testing/custom/ports.py).
That's exactly what tends to happen when segmentation blocks a path hard
enough, so it must never be silently dropped from this summary - it has to
show up as a FAIL like any other failed test.
"""

import json
import re
import sys
from collections import defaultdict

from rich.console import Console
from rich.table import Table

DEFAULT_INPUT = "testing/reports/nrfu_results.json"
PROTOCOLS = ["ICMP", "TCP", "UDP", "Telnet"]

# Kept in sync with PEER_DEVICES in testing/custom/ports.py. Duplicated here
# (rather than imported) so this script only depends on `rich`, not on
# anta/pydantic being importable.
PEER_DEVICES = {
    "172.16.11.10": "c1-Staff-H1",
    "172.16.21.10": "c1-Media-H2",
    "172.16.31.10": "c1-IOT-H3",
    "172.16.41.10": "c1-Sales-H4",
    "172.16.12.10": "c2-Staff-H1",
    "172.16.22.10": "c2-Media-H2",
    "172.16.32.10": "c2-IOT-H3",
    "172.16.42.10": "c2-Sales-H4",
    "172.16.13.10": "c3-Staff-H1",
    "172.16.23.10": "c3-Media-H2",
    "172.16.33.10": "c3-IOT-H3",
    "172.16.43.10": "c3-Sales-H4",
}

HOSTNAME_RE = re.compile(r"^c(\d+)-([A-Za-z]+)-H\d+$")
FROM_TO_RE = re.compile(r"from (\S+) to (\S+) \(Port")
ICMP_PREFIX = "ICMP reachability validation for: "
ICMP_FAILED_RE = re.compile(r"target device: (\S+)")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def department(hostname):
    """Split a device hostname like c1-Staff-H1 into ('campus1', 'Staff')."""
    m = HOSTNAME_RE.match(hostname)
    if not m:
        return None
    return f"campus{m.group(1)}", m.group(2)


def destinations_from_messages(messages):
    """Best-effort recovery of destination host(s) mentioned in a result's messages.

    Used when a test errored before its test() body ran, so `description` was
    never rewritten with the real "from X to Y" text. The raw command text
    embedded in ANTA's own error message (eg. "nc -zw 3 172.16.21.10 22 ...
    has failed: ...") still carries the destination IP, so we recover the peer
    name from that instead of giving up on the result entirely.
    """
    text = " ".join(messages)
    ips = dict.fromkeys(IPV4_RE.findall(text))  # de-dupe, preserve order
    return [PEER_DEVICES.get(ip, ip) for ip in ips]


def pairs_from_result(result):
    """Yield (source_host, dest_host, passed) for every host-pair covered by this test result.

    Always yields at least one entry for every test result ANTA produced -
    including ones that errored out before ever reaching our custom test()
    code - so nothing silently vanishes from the summary. When a destination
    truly can't be determined (no IP recoverable from the messages), it is
    yielded as "unknown" rather than dropped, so it still surfaces as an
    unattributed failure instead of disappearing.

    ICMP bundles every peer it pinged from a given host into a single TestResult, so a
    failure there only names the peers that actually failed in `messages` - everything else
    listed in the description passed. TCP/UDP/Telnet each describe exactly one host-pair.
    """
    test = result["test"]
    description = result["description"]
    status = result["result"]
    passed = status == "success"
    source = result["name"]
    messages = result.get("messages", [])

    if test == "ICMP":
        if description.startswith(ICMP_PREFIX):
            failed_targets = {m.group(1) for m in ICMP_FAILED_RE.finditer(" ".join(messages))}
            for leg in description[len(ICMP_PREFIX):].split(", "):
                leg_source, _, dest = leg.partition(" to ")
                if not dest:
                    continue
                yield leg_source, dest, dest not in failed_targets
            return
        # test() never ran (eg. the ping command itself errored/timed out at
        # the eAPI layer) - description is still the static class default and
        # won't match ICMP_PREFIX. Recover the destination from messages.
        for dest in destinations_from_messages(messages) or ["unknown"]:
            yield source, dest, False
        return

    m = FROM_TO_RE.search(description)
    if m:
        yield m.group(1), m.group(2), passed
        return

    # Same "test() never ran" situation as above, for TCP/UDP/Telnet.
    for dest in destinations_from_messages(messages) or ["unknown"]:
        yield source, dest, False


def build_summary(results):
    """Return ({(campus, src_dept, dst_dept): {protocol: [total, passed]}}, unattributed).

    `unattributed` holds (source, dest, test, status, detail) tuples for any
    host-pair whose source/destination couldn't be mapped to a known
    campus/department - kept separate so the caller can still surface them
    instead of them disappearing.
    """
    summary = defaultdict(lambda: {p: [0, 0] for p in PROTOCOLS})
    unattributed = []

    for result in results:
        if result["test"] not in PROTOCOLS:
            continue
        for source, dest, passed in pairs_from_result(result):
            src = department(source)
            dst = department(dest)
            if not src or not dst:
                detail = "; ".join(result.get("messages", [])) or result["description"]
                unattributed.append((source, dest, result["test"], result["result"], detail))
                continue
            src_campus, src_dept = src
            _, dst_dept = dst
            counts = summary[(src_campus, src_dept, dst_dept)][result["test"]]
            counts[0] += 1
            counts[1] += 1 if passed else 0

    return summary, unattributed


def render_table(summary):
    table = Table(title="Department Connectivity Summary", header_style="bold cyan")
    table.add_column("Campus")
    table.add_column("Source")
    table.add_column("Dest")
    for proto in PROTOCOLS:
        table.add_column(proto, justify="center")

    for campus, src, dst in sorted(summary):
        row = [campus, src, dst]
        for proto in PROTOCOLS:
            total, passed = summary[(campus, src, dst)][proto]
            if total == 0:
                row.append("[dim]-[/dim]")
            elif passed == total:
                row.append("[bold green]PASS[/bold green]")
            else:
                row.append(f"[bold red]FAIL({passed}/{total})[/bold red]")
        table.add_row(*row)

    return table


def render_unattributed(entries):
    table = Table(title="Errored Tests Not Attributable to a Department Pair", header_style="bold red")
    table.add_column("Source")
    table.add_column("Destination")
    table.add_column("Test")
    table.add_column("Status")
    table.add_column("Detail")

    for source, dest, test, status, detail in entries:
        table.add_row(source, dest, test, f"[bold red]{status.upper()}[/bold red]", detail)

    return table


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    with open(input_path) as f:
        results = json.load(f)

    summary, unattributed = build_summary(results)
    console = Console()

    if not summary and not unattributed:
        print("No connectivity test results found.")
        return

    if summary:
        console.print(render_table(summary))
    if unattributed:
        console.print(render_unattributed(unattributed))


if __name__ == "__main__":
    main()
