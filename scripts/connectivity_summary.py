#!/usr/bin/env python3
"""
Reads an ANTA NRFU JSON report (anta nrfu json -o <file>) and prints a
department-to-department connectivity summary: for each (campus, source
department, destination department) triple, whether ICMP/TCP/UDP/Telnet
passed across every host-pair ANTA actually tested for that combination.
"""

import json
import re
import sys
from collections import defaultdict

from rich.console import Console
from rich.table import Table

DEFAULT_INPUT = "testing/reports/nrfu_results.json"
PROTOCOLS = ["ICMP", "TCP", "UDP", "Telnet"]

HOSTNAME_RE = re.compile(r"^c(\d+)-([A-Za-z]+)-H\d+$")
FROM_TO_RE = re.compile(r"from (\S+) to (\S+) \(Port")
ICMP_PREFIX = "ICMP reachability validation for: "
ICMP_FAILED_RE = re.compile(r"target device: (\S+)")


def department(hostname):
    """Split a device hostname like c1-Staff-H1 into ('campus1', 'Staff')."""
    m = HOSTNAME_RE.match(hostname)
    if not m:
        return None
    return f"campus{m.group(1)}", m.group(2)


def pairs_from_result(result):
    """Yield (source_host, dest_host, passed) for every host-pair covered by this test result.

    ICMP bundles every peer it pinged from a given host into a single TestResult, so a
    failure there only names the peers that actually failed in `messages` - everything else
    listed in the description passed. TCP/UDP/Telnet each describe exactly one host-pair.
    """
    test = result["test"]
    description = result["description"]
    status = result["result"]

    if test == "ICMP":
        if not description.startswith(ICMP_PREFIX):
            return
        failed_targets = {m.group(1) for m in ICMP_FAILED_RE.finditer(" ".join(result.get("messages", [])))}
        for leg in description[len(ICMP_PREFIX):].split(", "):
            source, _, dest = leg.partition(" to ")
            if not dest:
                continue
            yield source, dest, dest not in failed_targets
        return

    m = FROM_TO_RE.search(description)
    if not m:
        return
    yield m.group(1), m.group(2), status == "success"


def build_summary(results):
    """Return {(campus, src_dept, dst_dept): {protocol: [total, passed]}}."""
    summary = defaultdict(lambda: {p: [0, 0] for p in PROTOCOLS})

    for result in results:
        if result["test"] not in PROTOCOLS:
            continue
        for source, dest, passed in pairs_from_result(result):
            src = department(source)
            dst = department(dest)
            if not src or not dst:
                continue
            src_campus, src_dept = src
            _, dst_dept = dst
            counts = summary[(src_campus, src_dept, dst_dept)][result["test"]]
            counts[0] += 1
            counts[1] += 1 if passed else 0

    return summary


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


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    with open(input_path) as f:
        results = json.load(f)

    summary = build_summary(results)
    if not summary:
        print("No connectivity test results found.")
        return

    Console().print(render_table(summary))


if __name__ == "__main__":
    main()
