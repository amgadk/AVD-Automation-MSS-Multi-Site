# borderleaf1

## Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
- [Authentication](#authentication)
  - [Enable Password](#enable-password)
- [MLAG](#mlag)
  - [MLAG Summary](#mlag-summary)
  - [MLAG Device Configuration](#mlag-device-configuration)
- [Spanning Tree](#spanning-tree)
  - [Spanning Tree Summary](#spanning-tree-summary)
  - [Spanning Tree Device Configuration](#spanning-tree-device-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Device Configuration](#internal-vlan-allocation-policy-device-configuration)
- [VLANs](#vlans)
  - [VLANs Summary](#vlans-summary)
  - [VLANs Device Configuration](#vlans-device-configuration)
- [Interfaces](#interfaces)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Port-Channel Interfaces](#port-channel-interfaces)
  - [Loopback Interfaces](#loopback-interfaces)
  - [VLAN Interfaces](#vlan-interfaces)
  - [VXLAN Interface](#vxlan-interface)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [Virtual Router MAC Address](#virtual-router-mac-address)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Static Routes](#static-routes)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
- [Multicast](#multicast)
  - [IP IGMP Snooping](#ip-igmp-snooping)
- [Filters](#filters)
  - [Prefix-lists](#prefix-lists)
  - [Route-maps](#route-maps)
- [VRF Instances](#vrf-instances)
  - [VRF Instances Summary](#vrf-instances-summary)
  - [VRF Instances Device Configuration](#vrf-instances-device-configuration)

## Management

### Management Interfaces

#### Management Interfaces Summary

##### IPv4

| Management Interface | Description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management1 | OOB_MANAGEMENT | oob | default | 192.168.0.107/24 | - |

##### IPv6

| Management Interface | Description | Type | VRF | IPv6 Address | IPv6 Gateway |
| -------------------- | ----------- | ---- | --- | ------------ | ------------ |
| Management1 | OOB_MANAGEMENT | oob | default | - | - |

#### Management Interfaces Device Configuration

```eos
!
interface Management1
   description OOB_MANAGEMENT
   no shutdown
   ip address 192.168.0.107/24
```

## Authentication

### Enable Password

Enable password has been disabled

## MLAG

### MLAG Summary

| Domain-id | Local-interface | Peer-address | Peer-link |
| --------- | --------------- | ------------ | --------- |
| borderleafs | Vlan4094 | 10.255.252.217 | Port-Channel5 |

Dual primary detection is disabled.

### MLAG Device Configuration

```eos
!
mlag configuration
   domain-id borderleafs
   local-interface Vlan4094
   peer-address 10.255.252.217
   peer-link Port-Channel5
   reload-delay mlag 300
   reload-delay non-mlag 330
```

## Spanning Tree

### Spanning Tree Summary

STP mode: **mstp**

#### MSTP Instance and Priority

| Instance(s) | Priority |
| -------- | -------- |
| 0 | 16384 |

#### Global Spanning-Tree Settings

- Spanning Tree disabled for VLANs: **4093-4094**

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode mstp
no spanning-tree vlan-id 4093-4094
spanning-tree mst 0 priority 16384
```

## Internal VLAN Allocation Policy

### Internal VLAN Allocation Policy Summary

| Policy Allocation | Range Beginning | Range Ending |
| ----------------- | --------------- | ------------ |
| ascending | 1006 | 1199 |

### Internal VLAN Allocation Policy Device Configuration

```eos
!
vlan internal order ascending range 1006 1199
```

## VLANs

### VLANs Summary

| VLAN ID | Name | Trunk Groups |
| ------- | ---- | ------------ |
| 20 | Internal | - |
| 101 | STAFF_NW | - |
| 201 | MEDIA_NW | - |
| 301 | IOT_NW | - |
| 401 | SALES_NW | - |
| 3777 | MLAG_L3_VRF_VRF-C | MLAG |
| 3888 | MLAG_L3_VRF_VRF-S | MLAG |
| 4093 | MLAG_L3 | MLAG |
| 4094 | MLAG | MLAG |

### VLANs Device Configuration

```eos
!
vlan 20
   name Internal
!
vlan 101
   name STAFF_NW
!
vlan 201
   name MEDIA_NW
!
vlan 301
   name IOT_NW
!
vlan 401
   name SALES_NW
!
vlan 3777
   name MLAG_L3_VRF_VRF-C
   trunk group MLAG
!
vlan 3888
   name MLAG_L3_VRF_VRF-S
   trunk group MLAG
!
vlan 4093
   name MLAG_L3
   trunk group MLAG
!
vlan 4094
   name MLAG
   trunk group MLAG
```

## Interfaces

### Ethernet Interfaces

#### Ethernet Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |
| Ethernet5 | MLAG_borderleaf2_Ethernet5 | *trunk | *- | *- | *MLAG | 5 |
| Ethernet6 | MLAG_borderleaf2_Ethernet6 | *trunk | *- | *- | *MLAG | 5 |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Channel Group | IP Address | VRF | MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | ------------- | ---------- | --- | --- | -------- | ------ | ------- |
| Ethernet1 | P2P_spine1_Ethernet7 | - | 10.255.201.177/31 | default | 1550 | False | - | - |
| Ethernet2 | P2P_spine2_Ethernet7 | - | 10.255.201.179/31 | default | 1550 | False | - | - |
| Ethernet11 | Firewall-1-LAN2 | - | 10.255.255.199/31 | VRF-S | - | False | - | - |
| Ethernet12 | Firewall-1-LAN3 | - | 10.255.255.201/31 | VRF-C | - | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_spine1_Ethernet7
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.201.177/31
!
interface Ethernet2
   description P2P_spine2_Ethernet7
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.201.179/31
!
interface Ethernet5
   description MLAG_borderleaf2_Ethernet5
   no shutdown
   channel-group 5 mode active
!
interface Ethernet6
   description MLAG_borderleaf2_Ethernet6
   no shutdown
   channel-group 5 mode active
!
interface Ethernet11
   description Firewall-1-LAN2
   no shutdown
   no switchport
   vrf VRF-S
   ip address 10.255.255.199/31
!
interface Ethernet12
   description Firewall-1-LAN3
   no shutdown
   no switchport
   vrf VRF-C
   ip address 10.255.255.201/31
```

### Port-Channel Interfaces

#### Port-Channel Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | --------------------- | ------------------ | ------- | -------- |
| Port-Channel5 | MLAG_borderleaf2_Port-Channel5 | trunk | - | - | MLAG | - | - | - | - |

#### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel5
   description MLAG_borderleaf2_Port-Channel5
   no shutdown
   switchport mode trunk
   switchport trunk group MLAG
   switchport
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | ROUTER_ID | default | 10.255.0.109/32 |
| Loopback1 | VXLAN_TUNNEL_SOURCE | default | 10.255.1.109/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | ROUTER_ID | default | - |
| Loopback1 | VXLAN_TUNNEL_SOURCE | default | - |

#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description ROUTER_ID
   no shutdown
   ip address 10.255.0.109/32
!
interface Loopback1
   description VXLAN_TUNNEL_SOURCE
   no shutdown
   ip address 10.255.1.109/32
```

### VLAN Interfaces

#### VLAN Interfaces Summary

| Interface | Description | VRF | MTU | Shutdown |
| --------- | ----------- | --- | --- | -------- |
| Vlan20 | Internal | VRF-S | - | False |
| Vlan101 | STAFF_NW | VRF-C | - | False |
| Vlan201 | MEDIA_NW | VRF-C | - | False |
| Vlan301 | IOT_NW | VRF-C | - | False |
| Vlan401 | SALES_NW | VRF-C | - | False |
| Vlan3777 | MLAG_L3_VRF_VRF-C | VRF-C | 1550 | False |
| Vlan3888 | MLAG_L3_VRF_VRF-S | VRF-S | 1550 | False |
| Vlan4093 | MLAG_L3 | default | 1550 | False |
| Vlan4094 | MLAG | default | 1550 | False |

##### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ------ | ------- |
| Vlan20 | VRF-S | - | 10.1.20.1/24 | - | - | - |
| Vlan101 | VRF-C | 172.16.11.1/24 | - | 172.16.11.254 | - | - |
| Vlan201 | VRF-C | 172.16.21.1/24 | - | 172.16.21.254 | - | - |
| Vlan301 | VRF-C | 172.16.31.1/24 | - | 172.16.31.254 | - | - |
| Vlan401 | VRF-C | 172.16.41.1/24 | - | 172.16.41.254 | - | - |
| Vlan3777 | VRF-C | 10.255.251.216/31 | - | - | - | - |
| Vlan3888 | VRF-S | 10.255.251.216/31 | - | - | - | - |
| Vlan4093 | default | 10.255.251.216/31 | - | - | - | - |
| Vlan4094 | default | 10.255.252.216/31 | - | - | - | - |

#### VLAN Interfaces Device Configuration

```eos
!
interface Vlan20
   description Internal
   no shutdown
   vrf VRF-S
   ip address virtual 10.1.20.1/24
!
interface Vlan101
   description STAFF_NW
   no shutdown
   vrf VRF-C
   ip address 172.16.11.1/24
   ip virtual-router address 172.16.11.254
!
interface Vlan201
   description MEDIA_NW
   no shutdown
   vrf VRF-C
   ip address 172.16.21.1/24
   ip virtual-router address 172.16.21.254
!
interface Vlan301
   description IOT_NW
   no shutdown
   vrf VRF-C
   ip address 172.16.31.1/24
   ip virtual-router address 172.16.31.254
!
interface Vlan401
   description SALES_NW
   no shutdown
   vrf VRF-C
   ip address 172.16.41.1/24
   ip virtual-router address 172.16.41.254
!
interface Vlan3777
   description MLAG_L3_VRF_VRF-C
   no shutdown
   mtu 1550
   vrf VRF-C
   ip address 10.255.251.216/31
!
interface Vlan3888
   description MLAG_L3_VRF_VRF-S
   no shutdown
   mtu 1550
   vrf VRF-S
   ip address 10.255.251.216/31
!
interface Vlan4093
   description MLAG_L3
   no shutdown
   mtu 1550
   ip address 10.255.251.216/31
!
interface Vlan4094
   description MLAG
   no shutdown
   mtu 1550
   no autostate
   ip address 10.255.252.216/31
```

### VXLAN Interface

#### VXLAN Interface Summary

| Setting | Value |
| ------- | ----- |
| Source Interface | Loopback1 |
| UDP port | 4789 |
| EVPN MLAG Shared Router MAC | mlag-system-id |

##### VLAN to VNI, Flood List and Multicast Group Mappings

| VLAN | VNI | Flood List | Multicast Group |
| ---- | --- | ---------- | --------------- |
| 20 | 2020 | - | - |
| 101 | 2101 | - | - |
| 201 | 2201 | - | - |
| 301 | 2301 | - | - |
| 401 | 2401 | - | - |

##### VRF to VNI and Multicast Group Mappings

| VRF | VNI | Overlay Multicast Group to Encap Mappings |
| --- | --- | ----------------------------------------- |
| VRF-C | 7777 | - |
| VRF-S | 8888 | - |

#### VXLAN Interface Device Configuration

```eos
!
interface Vxlan1
   description borderleaf1_VTEP
   vxlan source-interface Loopback1
   vxlan virtual-router encapsulation mac-address mlag-system-id
   vxlan udp-port 4789
   vxlan vlan 20 vni 2020
   vxlan vlan 101 vni 2101
   vxlan vlan 201 vni 2201
   vxlan vlan 301 vni 2301
   vxlan vlan 401 vni 2401
   vxlan vrf VRF-C vni 7777
   vxlan vrf VRF-S vni 8888
```

## Routing

### Service Routing Protocols Model

Multi agent routing protocol model enabled

```eos
!
service routing protocols model multi-agent
```

### Virtual Router MAC Address

#### Virtual Router MAC Address Summary

Virtual Router MAC Address: 00:1c:73:00:00:99

#### Virtual Router MAC Address Device Configuration

```eos
!
ip virtual-router mac-address 00:1c:73:00:00:99
```

### IP Routing

#### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | True |
| VRF-C | True |
| VRF-S | True |

#### IP Routing Device Configuration

```eos
!
ip routing
ip routing vrf VRF-C
ip routing vrf VRF-S
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| default | false |
| VRF-C | false |
| VRF-S | false |

### Static Routes

#### Static Routes Summary

| VRF | Destination Prefix | Next Hop IP | Exit interface | Administrative Distance | Tag | Route Name | Metric |
| --- | ------------------ | ----------- | -------------- | ----------------------- | --- | ---------- | ------ |
| VRF-S | 0.0.0.0/0 | 10.255.255.198 | - | 1 | - | to_FW-1 | - |

#### Static Routes Device Configuration

```eos
!
ip route vrf VRF-S 0.0.0.0/0 10.255.255.198 name to_FW-1
```

### Router BGP

ASN Notation: asplain

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65300 | 10.255.0.109 |

| BGP Tuning |
| ---------- |
| no bgp default ipv4-unicast |
| maximum-paths 4 |

#### Router BGP Peer Groups

##### EVPN-OVERLAY-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | evpn |
| Source | Loopback0 |
| BFD | True |
| Ebgp multihop | 3 |
| Send community | all |
| Maximum routes | 0 (no limit) |

##### IPv4-UNDERLAY-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Send community | all |
| Maximum routes | 256000 |

##### MLAG-IPv4-UNDERLAY-PEER

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Remote AS | 65300 |
| Next-hop self | True |
| Send community | all |
| Maximum routes | 256000 |

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive | TTL Max Hops |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- | ------------ |
| 10.255.0.100 | 65000 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.101 | 65000 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.201.176 | 65000 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.201.178 | 65000 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.251.217 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | default | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - | - |
| 10.255.251.217 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | VRF-C | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - | - |
| 10.255.251.217 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | VRF-S | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - | - |

#### Router BGP EVPN Address Family

##### EVPN Peer Groups

| Peer Group | Activate | Route-map In | Route-map Out | Peer-tag In | Peer-tag Out | Encapsulation | Next-hop-self Source Interface |
| ---------- | -------- | ------------ | ------------- | ----------- | ------------ | ------------- | ------------------------------ |
| EVPN-OVERLAY-PEERS | True | - | - | - | - | default | - |

#### Router BGP VLANs

| VLAN | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute |
| ---- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ |
| 20 | 10.255.0.109:2020 | 2020:2020 | - | - | learned |
| 101 | 10.255.0.109:2101 | 2101:2101 | - | - | learned |
| 201 | 10.255.0.109:2201 | 2201:2201 | - | - | learned |
| 301 | 10.255.0.109:2301 | 2301:2301 | - | - | learned |
| 401 | 10.255.0.109:2401 | 2401:2401 | - | - | learned |

#### Router BGP VRFs

| VRF | Route-Distinguisher | Redistribute | Graceful Restart |
| --- | ------------------- | ------------ | ---------------- |
| VRF-C | 10.255.0.109:7777 | connected | - |
| VRF-S | 10.255.0.109:8888 | connected<br>static | - |

#### Router BGP Device Configuration

```eos
!
router bgp 65300
   router-id 10.255.0.109
   no bgp default ipv4-unicast
   maximum-paths 4
   neighbor EVPN-OVERLAY-PEERS peer group
   neighbor EVPN-OVERLAY-PEERS update-source Loopback0
   neighbor EVPN-OVERLAY-PEERS bfd
   neighbor EVPN-OVERLAY-PEERS ebgp-multihop 3
   neighbor EVPN-OVERLAY-PEERS send-community
   neighbor EVPN-OVERLAY-PEERS maximum-routes 0
   neighbor IPv4-UNDERLAY-PEERS peer group
   neighbor IPv4-UNDERLAY-PEERS send-community
   neighbor IPv4-UNDERLAY-PEERS maximum-routes 256000
   neighbor MLAG-IPv4-UNDERLAY-PEER peer group
   neighbor MLAG-IPv4-UNDERLAY-PEER remote-as 65300
   neighbor MLAG-IPv4-UNDERLAY-PEER next-hop-self
   neighbor MLAG-IPv4-UNDERLAY-PEER description borderleaf2
   neighbor MLAG-IPv4-UNDERLAY-PEER route-map RM-MLAG-PEER-IN in
   neighbor MLAG-IPv4-UNDERLAY-PEER send-community
   neighbor MLAG-IPv4-UNDERLAY-PEER maximum-routes 256000
   neighbor 10.255.0.100 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.100 remote-as 65000
   neighbor 10.255.0.100 description spine1_Loopback0
   neighbor 10.255.0.101 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.101 remote-as 65000
   neighbor 10.255.0.101 description spine2_Loopback0
   neighbor 10.255.201.176 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.201.176 remote-as 65000
   neighbor 10.255.201.176 description spine1_Ethernet7
   neighbor 10.255.201.178 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.201.178 remote-as 65000
   neighbor 10.255.201.178 description spine2_Ethernet7
   neighbor 10.255.251.217 peer group MLAG-IPv4-UNDERLAY-PEER
   neighbor 10.255.251.217 description borderleaf2_Vlan4093
   redistribute connected route-map RM-CONN-2-BGP
   !
   vlan 20
      rd 10.255.0.109:2020
      route-target both 2020:2020
      redistribute learned
   !
   vlan 101
      rd 10.255.0.109:2101
      route-target both 2101:2101
      redistribute learned
   !
   vlan 201
      rd 10.255.0.109:2201
      route-target both 2201:2201
      redistribute learned
   !
   vlan 301
      rd 10.255.0.109:2301
      route-target both 2301:2301
      redistribute learned
   !
   vlan 401
      rd 10.255.0.109:2401
      route-target both 2401:2401
      redistribute learned
   !
   address-family evpn
      neighbor EVPN-OVERLAY-PEERS activate
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS activate
      neighbor MLAG-IPv4-UNDERLAY-PEER activate
   !
   vrf VRF-C
      rd 10.255.0.109:7777
      route-target import evpn 7777:7777
      route-target export evpn 7777:7777
      router-id 10.255.0.109
      neighbor 10.255.251.217 peer group MLAG-IPv4-UNDERLAY-PEER
      neighbor 10.255.251.217 description borderleaf2_Vlan3777
      redistribute connected route-map RM-CONN-2-BGP-VRFS
   !
   vrf VRF-S
      rd 10.255.0.109:8888
      route-target import evpn 8888:8888
      route-target export evpn 8888:8888
      router-id 10.255.0.109
      neighbor 10.255.251.217 peer group MLAG-IPv4-UNDERLAY-PEER
      neighbor 10.255.251.217 description borderleaf2_Vlan3888
      redistribute connected route-map RM-CONN-2-BGP-VRFS
      redistribute static
```

## BFD

### Router BFD

#### Router BFD Multihop Summary

| Interval | Minimum RX | Multiplier |
| -------- | ---------- | ---------- |
| 300 | 300 | 3 |

#### Router BFD Device Configuration

```eos
!
router bfd
   multihop interval 300 min-rx 300 multiplier 3
```

## Multicast

### IP IGMP Snooping

#### IP IGMP Snooping Summary

| IGMP Snooping | Fast Leave | Interface Restart Query | Proxy | Restart Query Interval | Robustness Variable |
| ------------- | ---------- | ----------------------- | ----- | ---------------------- | ------------------- |
| Enabled | - | - | - | - | - |

#### IP IGMP Snooping Device Configuration

```eos
```

## Filters

### Prefix-lists

#### Prefix-lists Summary

##### PL-LOOPBACKS-EVPN-OVERLAY

| Sequence | Action |
| -------- | ------ |
| 10 | permit 10.255.0.0/24 eq 32 |
| 20 | permit 10.255.1.0/24 eq 32 |

##### PL-MLAG-PEER-VRFS

| Sequence | Action |
| -------- | ------ |
| 10 | permit 10.255.251.216/31 |

#### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 10.255.0.0/24 eq 32
   seq 20 permit 10.255.1.0/24 eq 32
!
ip prefix-list PL-MLAG-PEER-VRFS
   seq 10 permit 10.255.251.216/31
```

### Route-maps

#### Route-maps Summary

##### RM-CONN-2-BGP

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY | - | - | - |

##### RM-CONN-2-BGP-VRFS

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | deny | ip address prefix-list PL-MLAG-PEER-VRFS | - | - | - |
| 20 | permit | - | - | - | - |

##### RM-MLAG-PEER-IN

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | - | origin incomplete | - | - |

#### Route-maps Device Configuration

```eos
!
route-map RM-CONN-2-BGP permit 10
   match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY
!
route-map RM-CONN-2-BGP-VRFS deny 10
   match ip address prefix-list PL-MLAG-PEER-VRFS
!
route-map RM-CONN-2-BGP-VRFS permit 20
!
route-map RM-MLAG-PEER-IN permit 10
   description Make routes learned over MLAG Peer-link less preferred on spines to ensure optimal routing
   set origin incomplete
```

## VRF Instances

### VRF Instances Summary

| VRF Name | IP Routing |
| -------- | ---------- |
| VRF-C | enabled |
| VRF-S | enabled |

### VRF Instances Device Configuration

```eos
!
vrf instance VRF-C
!
vrf instance VRF-S
```
