# Automated (AVD) Campus Deployment 


<p align="center">
  <img src='images/MSS-Multi-Campus.png' alt='Arista DC Fabric'/>
</p>

# FABRIC

## Table of Contents

- [Fabric Switches and Management IP](#fabric-switches-and-management-ip)
  - [Fabric Switches with inband Management IP](#fabric-switches-with-inband-management-ip)
- [Fabric Topology](#fabric-topology)
- [Fabric IP Allocation](#fabric-ip-allocation)
  - [Fabric Point-To-Point Links](#fabric-point-to-point-links)
  - [Point-To-Point Links Node Allocation](#point-to-point-links-node-allocation)
  - [Loopback Interfaces (BGP EVPN Peering)](#loopback-interfaces-bgp-evpn-peering)
  - [Loopback0 Interfaces Node Allocation](#loopback0-interfaces-node-allocation)
  - [VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)](#vtep-loopback-vxlan-tunnel-source-interfaces-vteps-only)
  - [VTEP Loopback Node allocation](#vtep-loopback-node-allocation)

## Fabric Switches and Management IP

| POD | Type | Node | Management IP | Platform | Provisioned in CloudVision | Serial Number |
| --- | ---- | ---- | ------------- | -------- | -------------------------- | ------------- |
| FABRIC | l3leaf | c1-borderleaf1 | 192.168.0.107/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c1-borderleaf2 | 192.168.0.108/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c1-leaf1 | 192.168.0.101/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c1-leaf2 | 192.168.0.102/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c1-leaf3 | 192.168.0.103/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c1-leaf4 | 192.168.0.104/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c1-leaf5 | 192.168.0.105/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c1-leaf6 | 192.168.0.106/24 | vEOS-lab | Provisioned | - |
| FABRIC | spine | c1-spine1 | 192.168.0.111/24 | vEOS-lab | Provisioned | - |
| FABRIC | spine | c1-spine2 | 192.168.0.112/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c2-borderleaf1 | 192.168.0.207/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c2-borderleaf2 | 192.168.0.208/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c2-leaf1 | 192.168.0.201/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c2-leaf2 | 192.168.0.202/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c2-leaf3 | 192.168.0.203/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c2-leaf4 | 192.168.0.204/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c2-leaf5 | 192.168.0.205/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c2-leaf6 | 192.168.0.206/24 | vEOS-lab | Provisioned | - |
| FABRIC | spine | c2-spine1 | 192.168.0.113/24 | vEOS-lab | Provisioned | - |
| FABRIC | spine | c2-spine2 | 192.168.0.114/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c3-borderleaf1 | 192.168.0.137/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c3-borderleaf2 | 192.168.0.138/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c3-leaf1 | 192.168.0.131/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c3-leaf2 | 192.168.0.132/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c3-leaf3 | 192.168.0.133/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c3-leaf4 | 192.168.0.134/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c3-leaf5 | 192.168.0.135/24 | vEOS-lab | Provisioned | - |
| FABRIC | l3leaf | c3-leaf6 | 192.168.0.136/24 | vEOS-lab | Provisioned | - |
| FABRIC | spine | c3-spine1 | 192.168.0.115/24 | vEOS-lab | Provisioned | - |
| FABRIC | spine | c3-spine2 | 192.168.0.116/24 | vEOS-lab | Provisioned | - |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

### Fabric Switches with inband Management IP

| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

## Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | --------- | -------------- |
| l3leaf | c1-borderleaf1 | Ethernet1 | spine | c1-spine1 | Ethernet7 |
| l3leaf | c1-borderleaf1 | Ethernet2 | spine | c1-spine2 | Ethernet7 |
| l3leaf | c1-borderleaf1 | Ethernet5 | mlag_peer | c1-borderleaf2 | Ethernet5 |
| l3leaf | c1-borderleaf1 | Ethernet6 | mlag_peer | c1-borderleaf2 | Ethernet6 |
| l3leaf | c1-borderleaf2 | Ethernet1 | spine | c1-spine1 | Ethernet8 |
| l3leaf | c1-borderleaf2 | Ethernet2 | spine | c1-spine2 | Ethernet8 |
| l3leaf | c1-leaf1 | Ethernet1 | spine | c1-spine1 | Ethernet1 |
| l3leaf | c1-leaf1 | Ethernet2 | spine | c1-spine2 | Ethernet1 |
| l3leaf | c1-leaf1 | Ethernet5 | mlag_peer | c1-leaf2 | Ethernet5 |
| l3leaf | c1-leaf1 | Ethernet6 | mlag_peer | c1-leaf2 | Ethernet6 |
| l3leaf | c1-leaf2 | Ethernet1 | spine | c1-spine1 | Ethernet2 |
| l3leaf | c1-leaf2 | Ethernet2 | spine | c1-spine2 | Ethernet2 |
| l3leaf | c1-leaf3 | Ethernet1 | spine | c1-spine1 | Ethernet3 |
| l3leaf | c1-leaf3 | Ethernet2 | spine | c1-spine2 | Ethernet3 |
| l3leaf | c1-leaf3 | Ethernet5 | mlag_peer | c1-leaf4 | Ethernet5 |
| l3leaf | c1-leaf3 | Ethernet6 | mlag_peer | c1-leaf4 | Ethernet6 |
| l3leaf | c1-leaf4 | Ethernet1 | spine | c1-spine1 | Ethernet4 |
| l3leaf | c1-leaf4 | Ethernet2 | spine | c1-spine2 | Ethernet4 |
| l3leaf | c1-leaf5 | Ethernet1 | spine | c1-spine1 | Ethernet5 |
| l3leaf | c1-leaf5 | Ethernet2 | spine | c1-spine2 | Ethernet5 |
| l3leaf | c1-leaf5 | Ethernet5 | mlag_peer | c1-leaf6 | Ethernet5 |
| l3leaf | c1-leaf5 | Ethernet6 | mlag_peer | c1-leaf6 | Ethernet6 |
| l3leaf | c1-leaf6 | Ethernet1 | spine | c1-spine1 | Ethernet6 |
| l3leaf | c1-leaf6 | Ethernet2 | spine | c1-spine2 | Ethernet6 |
| l3leaf | c2-borderleaf1 | Ethernet1 | spine | c2-spine1 | Ethernet7 |
| l3leaf | c2-borderleaf1 | Ethernet2 | spine | c2-spine2 | Ethernet7 |
| l3leaf | c2-borderleaf1 | Ethernet5 | mlag_peer | c2-borderleaf2 | Ethernet5 |
| l3leaf | c2-borderleaf1 | Ethernet6 | mlag_peer | c2-borderleaf2 | Ethernet6 |
| l3leaf | c2-borderleaf2 | Ethernet1 | spine | c2-spine1 | Ethernet8 |
| l3leaf | c2-borderleaf2 | Ethernet2 | spine | c2-spine2 | Ethernet8 |
| l3leaf | c2-leaf1 | Ethernet1 | spine | c2-spine1 | Ethernet1 |
| l3leaf | c2-leaf1 | Ethernet2 | spine | c2-spine2 | Ethernet1 |
| l3leaf | c2-leaf1 | Ethernet5 | mlag_peer | c2-leaf2 | Ethernet5 |
| l3leaf | c2-leaf1 | Ethernet6 | mlag_peer | c2-leaf2 | Ethernet6 |
| l3leaf | c2-leaf2 | Ethernet1 | spine | c2-spine1 | Ethernet2 |
| l3leaf | c2-leaf2 | Ethernet2 | spine | c2-spine2 | Ethernet2 |
| l3leaf | c2-leaf3 | Ethernet1 | spine | c2-spine1 | Ethernet3 |
| l3leaf | c2-leaf3 | Ethernet2 | spine | c2-spine2 | Ethernet3 |
| l3leaf | c2-leaf3 | Ethernet5 | mlag_peer | c2-leaf4 | Ethernet5 |
| l3leaf | c2-leaf3 | Ethernet6 | mlag_peer | c2-leaf4 | Ethernet6 |
| l3leaf | c2-leaf4 | Ethernet1 | spine | c2-spine1 | Ethernet4 |
| l3leaf | c2-leaf4 | Ethernet2 | spine | c2-spine2 | Ethernet4 |
| l3leaf | c2-leaf5 | Ethernet1 | spine | c2-spine1 | Ethernet5 |
| l3leaf | c2-leaf5 | Ethernet2 | spine | c2-spine2 | Ethernet5 |
| l3leaf | c2-leaf5 | Ethernet5 | mlag_peer | c2-leaf6 | Ethernet5 |
| l3leaf | c2-leaf5 | Ethernet6 | mlag_peer | c2-leaf6 | Ethernet6 |
| l3leaf | c2-leaf6 | Ethernet1 | spine | c2-spine1 | Ethernet6 |
| l3leaf | c2-leaf6 | Ethernet2 | spine | c2-spine2 | Ethernet6 |
| l3leaf | c3-borderleaf1 | Ethernet1 | spine | c3-spine1 | Ethernet7 |
| l3leaf | c3-borderleaf1 | Ethernet2 | spine | c3-spine2 | Ethernet7 |
| l3leaf | c3-borderleaf1 | Ethernet5 | mlag_peer | c3-borderleaf2 | Ethernet5 |
| l3leaf | c3-borderleaf1 | Ethernet6 | mlag_peer | c3-borderleaf2 | Ethernet6 |
| l3leaf | c3-borderleaf2 | Ethernet1 | spine | c3-spine1 | Ethernet8 |
| l3leaf | c3-borderleaf2 | Ethernet2 | spine | c3-spine2 | Ethernet8 |
| l3leaf | c3-leaf1 | Ethernet1 | spine | c3-spine1 | Ethernet1 |
| l3leaf | c3-leaf1 | Ethernet2 | spine | c3-spine2 | Ethernet1 |
| l3leaf | c3-leaf1 | Ethernet5 | mlag_peer | c3-leaf2 | Ethernet5 |
| l3leaf | c3-leaf1 | Ethernet6 | mlag_peer | c3-leaf2 | Ethernet6 |
| l3leaf | c3-leaf2 | Ethernet1 | spine | c3-spine1 | Ethernet2 |
| l3leaf | c3-leaf2 | Ethernet2 | spine | c3-spine2 | Ethernet2 |
| l3leaf | c3-leaf3 | Ethernet1 | spine | c3-spine1 | Ethernet3 |
| l3leaf | c3-leaf3 | Ethernet2 | spine | c3-spine2 | Ethernet3 |
| l3leaf | c3-leaf3 | Ethernet5 | mlag_peer | c3-leaf4 | Ethernet5 |
| l3leaf | c3-leaf3 | Ethernet6 | mlag_peer | c3-leaf4 | Ethernet6 |
| l3leaf | c3-leaf4 | Ethernet1 | spine | c3-spine1 | Ethernet4 |
| l3leaf | c3-leaf4 | Ethernet2 | spine | c3-spine2 | Ethernet4 |
| l3leaf | c3-leaf5 | Ethernet1 | spine | c3-spine1 | Ethernet5 |
| l3leaf | c3-leaf5 | Ethernet2 | spine | c3-spine2 | Ethernet5 |
| l3leaf | c3-leaf5 | Ethernet5 | mlag_peer | c3-leaf6 | Ethernet5 |
| l3leaf | c3-leaf5 | Ethernet6 | mlag_peer | c3-leaf6 | Ethernet6 |
| l3leaf | c3-leaf6 | Ethernet1 | spine | c3-spine1 | Ethernet6 |
| l3leaf | c3-leaf6 | Ethernet2 | spine | c3-spine2 | Ethernet6 |

## Fabric IP Allocation

### Fabric Point-To-Point Links

| Uplink IPv4 Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ---------------- | ------------------- | ------------------ | ------------------ |
| 10.10.200.0/22 | 1024 | 32 | 3.13 % |
| 10.20.200.0/22 | 1024 | 32 | 3.13 % |
| 10.30.200.0/22 | 1024 | 32 | 3.13 % |

### Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |
| c1-borderleaf1 | Ethernet1 | 10.10.201.177/31 | c1-spine1 | Ethernet7 | 10.10.201.176/31 |
| c1-borderleaf1 | Ethernet2 | 10.10.201.179/31 | c1-spine2 | Ethernet7 | 10.10.201.178/31 |
| c1-borderleaf2 | Ethernet1 | 10.10.201.181/31 | c1-spine1 | Ethernet8 | 10.10.201.180/31 |
| c1-borderleaf2 | Ethernet2 | 10.10.201.183/31 | c1-spine2 | Ethernet8 | 10.10.201.182/31 |
| c1-leaf1 | Ethernet1 | 10.10.201.153/31 | c1-spine1 | Ethernet1 | 10.10.201.152/31 |
| c1-leaf1 | Ethernet2 | 10.10.201.155/31 | c1-spine2 | Ethernet1 | 10.10.201.154/31 |
| c1-leaf2 | Ethernet1 | 10.10.201.157/31 | c1-spine1 | Ethernet2 | 10.10.201.156/31 |
| c1-leaf2 | Ethernet2 | 10.10.201.159/31 | c1-spine2 | Ethernet2 | 10.10.201.158/31 |
| c1-leaf3 | Ethernet1 | 10.10.201.161/31 | c1-spine1 | Ethernet3 | 10.10.201.160/31 |
| c1-leaf3 | Ethernet2 | 10.10.201.163/31 | c1-spine2 | Ethernet3 | 10.10.201.162/31 |
| c1-leaf4 | Ethernet1 | 10.10.201.165/31 | c1-spine1 | Ethernet4 | 10.10.201.164/31 |
| c1-leaf4 | Ethernet2 | 10.10.201.167/31 | c1-spine2 | Ethernet4 | 10.10.201.166/31 |
| c1-leaf5 | Ethernet1 | 10.10.201.169/31 | c1-spine1 | Ethernet5 | 10.10.201.168/31 |
| c1-leaf5 | Ethernet2 | 10.10.201.171/31 | c1-spine2 | Ethernet5 | 10.10.201.170/31 |
| c1-leaf6 | Ethernet1 | 10.10.201.173/31 | c1-spine1 | Ethernet6 | 10.10.201.172/31 |
| c1-leaf6 | Ethernet2 | 10.10.201.175/31 | c1-spine2 | Ethernet6 | 10.10.201.174/31 |
| c2-borderleaf1 | Ethernet1 | 10.20.201.253/31 | c2-spine1 | Ethernet7 | 10.20.201.252/31 |
| c2-borderleaf1 | Ethernet2 | 10.20.201.255/31 | c2-spine2 | Ethernet7 | 10.20.201.254/31 |
| c2-borderleaf2 | Ethernet1 | 10.20.202.1/31 | c2-spine1 | Ethernet8 | 10.20.202.0/31 |
| c2-borderleaf2 | Ethernet2 | 10.20.202.3/31 | c2-spine2 | Ethernet8 | 10.20.202.2/31 |
| c2-leaf1 | Ethernet1 | 10.20.201.229/31 | c2-spine1 | Ethernet1 | 10.20.201.228/31 |
| c2-leaf1 | Ethernet2 | 10.20.201.231/31 | c2-spine2 | Ethernet1 | 10.20.201.230/31 |
| c2-leaf2 | Ethernet1 | 10.20.201.233/31 | c2-spine1 | Ethernet2 | 10.20.201.232/31 |
| c2-leaf2 | Ethernet2 | 10.20.201.235/31 | c2-spine2 | Ethernet2 | 10.20.201.234/31 |
| c2-leaf3 | Ethernet1 | 10.20.201.237/31 | c2-spine1 | Ethernet3 | 10.20.201.236/31 |
| c2-leaf3 | Ethernet2 | 10.20.201.239/31 | c2-spine2 | Ethernet3 | 10.20.201.238/31 |
| c2-leaf4 | Ethernet1 | 10.20.201.241/31 | c2-spine1 | Ethernet4 | 10.20.201.240/31 |
| c2-leaf4 | Ethernet2 | 10.20.201.243/31 | c2-spine2 | Ethernet4 | 10.20.201.242/31 |
| c2-leaf5 | Ethernet1 | 10.20.201.245/31 | c2-spine1 | Ethernet5 | 10.20.201.244/31 |
| c2-leaf5 | Ethernet2 | 10.20.201.247/31 | c2-spine2 | Ethernet5 | 10.20.201.246/31 |
| c2-leaf6 | Ethernet1 | 10.20.201.249/31 | c2-spine1 | Ethernet6 | 10.20.201.248/31 |
| c2-leaf6 | Ethernet2 | 10.20.201.251/31 | c2-spine2 | Ethernet6 | 10.20.201.250/31 |
| c3-borderleaf1 | Ethernet1 | 10.30.202.37/31 | c3-spine1 | Ethernet7 | 10.30.202.36/31 |
| c3-borderleaf1 | Ethernet2 | 10.30.202.39/31 | c3-spine2 | Ethernet7 | 10.30.202.38/31 |
| c3-borderleaf2 | Ethernet1 | 10.30.202.41/31 | c3-spine1 | Ethernet8 | 10.30.202.40/31 |
| c3-borderleaf2 | Ethernet2 | 10.30.202.43/31 | c3-spine2 | Ethernet8 | 10.30.202.42/31 |
| c3-leaf1 | Ethernet1 | 10.30.202.13/31 | c3-spine1 | Ethernet1 | 10.30.202.12/31 |
| c3-leaf1 | Ethernet2 | 10.30.202.15/31 | c3-spine2 | Ethernet1 | 10.30.202.14/31 |
| c3-leaf2 | Ethernet1 | 10.30.202.17/31 | c3-spine1 | Ethernet2 | 10.30.202.16/31 |
| c3-leaf2 | Ethernet2 | 10.30.202.19/31 | c3-spine2 | Ethernet2 | 10.30.202.18/31 |
| c3-leaf3 | Ethernet1 | 10.30.202.21/31 | c3-spine1 | Ethernet3 | 10.30.202.20/31 |
| c3-leaf3 | Ethernet2 | 10.30.202.23/31 | c3-spine2 | Ethernet3 | 10.30.202.22/31 |
| c3-leaf4 | Ethernet1 | 10.30.202.25/31 | c3-spine1 | Ethernet4 | 10.30.202.24/31 |
| c3-leaf4 | Ethernet2 | 10.30.202.27/31 | c3-spine2 | Ethernet4 | 10.30.202.26/31 |
| c3-leaf5 | Ethernet1 | 10.30.202.29/31 | c3-spine1 | Ethernet5 | 10.30.202.28/31 |
| c3-leaf5 | Ethernet2 | 10.30.202.31/31 | c3-spine2 | Ethernet5 | 10.30.202.30/31 |
| c3-leaf6 | Ethernet1 | 10.30.202.33/31 | c3-spine1 | Ethernet6 | 10.30.202.32/31 |
| c3-leaf6 | Ethernet2 | 10.30.202.35/31 | c3-spine2 | Ethernet6 | 10.30.202.34/31 |

### Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 10.255.10.0/24 | 256 | 10 | 3.91 % |
| 10.255.20.0/24 | 256 | 10 | 3.91 % |
| 10.255.30.0/24 | 256 | 10 | 3.91 % |

### Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| FABRIC | c1-borderleaf1 | 10.255.10.109/32 |
| FABRIC | c1-borderleaf2 | 10.255.10.110/32 |
| FABRIC | c1-leaf1 | 10.255.10.103/32 |
| FABRIC | c1-leaf2 | 10.255.10.104/32 |
| FABRIC | c1-leaf3 | 10.255.10.105/32 |
| FABRIC | c1-leaf4 | 10.255.10.106/32 |
| FABRIC | c1-leaf5 | 10.255.10.107/32 |
| FABRIC | c1-leaf6 | 10.255.10.108/32 |
| FABRIC | c1-spine1 | 10.255.10.100/32 |
| FABRIC | c1-spine2 | 10.255.10.101/32 |
| FABRIC | c2-borderleaf1 | 10.255.20.128/32 |
| FABRIC | c2-borderleaf2 | 10.255.20.129/32 |
| FABRIC | c2-leaf1 | 10.255.20.122/32 |
| FABRIC | c2-leaf2 | 10.255.20.123/32 |
| FABRIC | c2-leaf3 | 10.255.20.124/32 |
| FABRIC | c2-leaf4 | 10.255.20.125/32 |
| FABRIC | c2-leaf5 | 10.255.20.126/32 |
| FABRIC | c2-leaf6 | 10.255.20.127/32 |
| FABRIC | c2-spine1 | 10.255.20.120/32 |
| FABRIC | c2-spine2 | 10.255.20.121/32 |
| FABRIC | c3-borderleaf1 | 10.255.30.138/32 |
| FABRIC | c3-borderleaf2 | 10.255.30.139/32 |
| FABRIC | c3-leaf1 | 10.255.30.132/32 |
| FABRIC | c3-leaf2 | 10.255.30.133/32 |
| FABRIC | c3-leaf3 | 10.255.30.134/32 |
| FABRIC | c3-leaf4 | 10.255.30.135/32 |
| FABRIC | c3-leaf5 | 10.255.30.136/32 |
| FABRIC | c3-leaf6 | 10.255.30.137/32 |
| FABRIC | c3-spine1 | 10.255.30.130/32 |
| FABRIC | c3-spine2 | 10.255.30.131/32 |

### VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------------ | ------------------- | ------------------ | ------------------ |
| 10.255.1.0/24 | 256 | 16 | 6.25 % |
| 10.255.2.0/24 | 256 | 8 | 3.13 % |

### VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
| FABRIC | c1-borderleaf1 | 10.255.1.109/32 |
| FABRIC | c1-borderleaf2 | 10.255.1.109/32 |
| FABRIC | c1-leaf1 | 10.255.1.103/32 |
| FABRIC | c1-leaf2 | 10.255.1.103/32 |
| FABRIC | c1-leaf3 | 10.255.1.105/32 |
| FABRIC | c1-leaf4 | 10.255.1.105/32 |
| FABRIC | c1-leaf5 | 10.255.1.107/32 |
| FABRIC | c1-leaf6 | 10.255.1.107/32 |
| FABRIC | c2-borderleaf1 | 10.255.2.128/32 |
| FABRIC | c2-borderleaf2 | 10.255.2.128/32 |
| FABRIC | c2-leaf1 | 10.255.2.122/32 |
| FABRIC | c2-leaf2 | 10.255.2.122/32 |
| FABRIC | c2-leaf3 | 10.255.2.124/32 |
| FABRIC | c2-leaf4 | 10.255.2.124/32 |
| FABRIC | c2-leaf5 | 10.255.2.126/32 |
| FABRIC | c2-leaf6 | 10.255.2.126/32 |
| FABRIC | c3-borderleaf1 | 10.255.1.138/32 |
| FABRIC | c3-borderleaf2 | 10.255.1.138/32 |
| FABRIC | c3-leaf1 | 10.255.1.132/32 |
| FABRIC | c3-leaf2 | 10.255.1.132/32 |
| FABRIC | c3-leaf3 | 10.255.1.134/32 |
| FABRIC | c3-leaf4 | 10.255.1.134/32 |
| FABRIC | c3-leaf5 | 10.255.1.136/32 |
| FABRIC | c3-leaf6 | 10.255.1.136/32 |
