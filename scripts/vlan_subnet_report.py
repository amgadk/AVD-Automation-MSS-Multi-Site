#!/usr/bin/env python3
"""
Reads AVD structured configs and produces a CSV of all user VLANs
with their subnets per campus across the entire fabric.
"""

import csv
import glob
import ipaddress
import os
import sys

import yaml

STRUCTURED_CONFIGS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "intended", "structured_configs"
)
OUTPUT_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "reports", "vlan_subnet_report.csv"
)

# VLANs above this ID are infrastructure VLANs (MLAG, etc.)
MAX_USER_VLAN = 4000


def campus_from_hostname(hostname):
    """Derive campus name from device hostname (e.g. c1-leaf1 -> CAMPUS1)."""
    prefix = hostname.split("-")[0].lower()
    mapping = {"c1": "CAMPUS1", "c2": "CAMPUS2", "c3": "CAMPUS3"}
    return mapping.get(prefix, prefix.upper())


def network_from_address(ip_with_prefix):
    """Return the network address string (e.g. 172.16.11.1/24 -> 172.16.11.0/24)."""
    return str(ipaddress.ip_interface(ip_with_prefix).network)


def collect_vlan_data(configs_dir):
    """
    Returns a dict keyed by (vlan_id, campus) with values:
    { "name": str, "subnet": str, "gateway": str }
    """
    data = {}

    for filepath in sorted(glob.glob(os.path.join(configs_dir, "*.yml"))):
        hostname = os.path.splitext(os.path.basename(filepath))[0]
        campus = campus_from_hostname(hostname)

        with open(filepath) as f:
            config = yaml.safe_load(f)

        for iface in config.get("vlan_interfaces", []):
            name = iface.get("name", "")
            if not name.startswith("Vlan"):
                continue

            vlan_id = int(name.replace("Vlan", ""))
            if vlan_id >= MAX_USER_VLAN:
                continue

            ip_address = iface.get("ip_address")
            if not ip_address:
                continue

            subnet = network_from_address(ip_address)
            gateways = iface.get("ip_virtual_router_addresses", [])
            gateway = gateways[0] if gateways else ""
            vlan_name = iface.get("description", "")

            # Skip infrastructure SVIs (MLAG iBGP peering, etc.)
            if not gateways:
                continue

            key = (vlan_id, campus)
            if key not in data:
                data[key] = {
                    "vlan_name": vlan_name,
                    "subnet": subnet,
                    "gateway": gateway,
                }

    return data


def write_csv(data, output_path):
    rows = sorted(data.items(), key=lambda x: (x[0][0], x[0][1]))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["VLAN ID", "VLAN Name", "Campus", "Subnet", "Gateway"])
        for (vlan_id, campus), info in rows:
            writer.writerow([
                vlan_id,
                info["vlan_name"],
                campus,
                info["subnet"],
                info["gateway"],
            ])

    return len(rows)


def main():
    if not os.path.isdir(STRUCTURED_CONFIGS_DIR):
        print(f"ERROR: structured configs directory not found: {STRUCTURED_CONFIGS_DIR}")
        sys.exit(1)

    data = collect_vlan_data(STRUCTURED_CONFIGS_DIR)
    row_count = write_csv(data, OUTPUT_CSV)
    print(f"Written {row_count} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
