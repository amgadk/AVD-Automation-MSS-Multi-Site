#!/usr/bin/env python3
"""
Reads AVD structured configs and produces:
  - a CSV of all user VLANs with their subnets per campus
  - a Group_Inputs YAML for upload to the management system
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
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
OUTPUT_CSV = os.path.join(REPORTS_DIR, "vlan_subnet_report.csv")
OUTPUT_YAML = os.path.join(REPORTS_DIR, "Group_Inputs_MSS Service.yaml")

MAX_USER_VLAN = 4000
POLICY_ID_BASE = 256


def campus_from_hostname(hostname):
    """Derive campus name from device hostname prefix (e.g. c1-leaf1 -> CAMPUS1)."""
    prefix = hostname.split("-")[0].lower()
    if prefix.startswith("c") and prefix[1:].isdigit():
        return f"CAMPUS{prefix[1:]}"
    return prefix.upper()


def network_from_address(ip_with_prefix):
    """Return the network address string (e.g. 172.16.11.1/24 -> 172.16.11.0/24)."""
    return str(ipaddress.ip_interface(ip_with_prefix).network)


def collect_vlan_data(configs_dir):
    """
    Returns a dict keyed by (vlan_id, campus) with values:
    { "vlan_name": str, "subnet": str, "gateway": str }
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
            vrf = iface.get("vrf", "")

            # Skip infrastructure SVIs (MLAG iBGP peering, etc.)
            if not gateways:
                continue

            key = (vlan_id, campus)
            if key not in data:
                data[key] = {
                    "vlan_name": vlan_name,
                    "subnet": subnet,
                    "gateway": gateway,
                    "vrf": vrf,
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


def group_name(vlan_name):
    """Convert e.g. STAFF_NW -> Staff_NW for static group names."""
    parts = vlan_name.split("_", 1)
    return parts[0].capitalize() + ("_" + parts[1] if len(parts) > 1 else "")


def campus_display(campus):
    """Convert e.g. CAMPUS1 -> Campus1 for policy and domain names."""
    return campus[0] + campus[1:].lower()


def build_yaml_structure(data):
    campuses = sorted(set(campus for (_, campus) in data.keys()))
    vrfs = sorted(set(info["vrf"] for info in data.values() if info["vrf"]))
    primary_vrf = vrfs[0] if vrfs else "default"

    # Group subnets by vlan_name across all campuses
    groups = {}
    for (vlan_id, _), info in data.items():
        name = group_name(info["vlan_name"])
        if name not in groups:
            groups[name] = {"vlan_id": vlan_id, "subnets": []}
        groups[name]["subnets"].append(info["subnet"])

    static_groups = [
        {
            "membership": {"members": sorted(entry["subnets"])},
            "name": name,
        }
        for name, entry in sorted(groups.items(), key=lambda x: x[1]["vlan_id"])
    ]

    hidden_policy_id_mapper = []
    policies = []
    security_domains = []

    for idx, campus in enumerate(campuses):
        display = campus_display(campus)
        policy_name = f"{display}-Policy-1"

        hidden_policy_id_mapper.append({
            "hiddenPolicyId": POLICY_ID_BASE + idx,
            "hiddenPolicyName": policy_name,
        })
        policies.append({"name": policy_name, "policyRules": []})
        security_domains.append({
            "inputs": {
                "securityDomain": {
                    "domainPolicies": [{"name": policy_name, "vrf": primary_vrf}]
                }
            },
            "tags": {"query": f"security-domain:{display}"},
        })

    return {
        "path": [],
        "inputs": {
            "hiddenDeviceMapper": [],
            "hiddenIntersectedGroupsMapper": [],
            "hiddenPolicyIdMapper": hidden_policy_id_mapper,
            "hiddenVrfMapper": [{"vrfKey": idx, "vrfName": vrf} for idx, vrf in enumerate(vrfs)],
            "policies": policies,
            "securityDomains": security_domains,
            "staticGroups": static_groups,
        },
    }


def write_yaml(data, output_path):
    yaml_data = build_yaml_structure(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
    return len(yaml_data["inputs"]["staticGroups"])


def main():
    if not os.path.isdir(STRUCTURED_CONFIGS_DIR):
        print(f"ERROR: structured configs directory not found: {STRUCTURED_CONFIGS_DIR}")
        sys.exit(1)

    data = collect_vlan_data(STRUCTURED_CONFIGS_DIR)

    row_count = write_csv(data, OUTPUT_CSV)
    print(f"Written {row_count} rows to {OUTPUT_CSV}")

    group_count = write_yaml(data, OUTPUT_YAML)
    print(f"Written {group_count} groups to {OUTPUT_YAML}")


if __name__ == "__main__":
    main()
