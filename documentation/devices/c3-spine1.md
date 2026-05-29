# c3-spine1

## Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
- [Authentication](#authentication)
  - [Enable Password](#enable-password)
- [Spanning Tree](#spanning-tree)
  - [Spanning Tree Summary](#spanning-tree-summary)
  - [Spanning Tree Device Configuration](#spanning-tree-device-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Device Configuration](#internal-vlan-allocation-policy-device-configuration)
- [Interfaces](#interfaces)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Loopback Interfaces](#loopback-interfaces)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
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
| Management1 | OOB_MANAGEMENT | oob | default | 192.168.0.115/24 | - |

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
   ip address 192.168.0.115/24
```

## Authentication

### Enable Password

Enable password has been disabled

## Spanning Tree

### Spanning Tree Summary

STP mode: **none**

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode none
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

## Interfaces

### Ethernet Interfaces

#### Ethernet Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Channel Group | IP Address | VRF | MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | ------------- | ---------- | --- | --- | -------- | ------ | ------- |
| Ethernet1 | P2P_c3-leaf1_Ethernet1 | - | 10.255.202.12/31 | default | 1550 | False | - | - |
| Ethernet2 | P2P_c3-leaf2_Ethernet1 | - | 10.255.202.16/31 | default | 1550 | False | - | - |
| Ethernet3 | P2P_c3-leaf3_Ethernet1 | - | 10.255.202.20/31 | default | 1550 | False | - | - |
| Ethernet4 | P2P_c3-leaf4_Ethernet1 | - | 10.255.202.24/31 | default | 1550 | False | - | - |
| Ethernet5 | P2P_c3-leaf5_Ethernet1 | - | 10.255.202.28/31 | default | 1550 | False | - | - |
| Ethernet6 | P2P_c3-leaf6_Ethernet1 | - | 10.255.202.32/31 | default | 1550 | False | - | - |
| Ethernet7 | P2P_c3-borderleaf1_Ethernet1 | - | 10.255.202.36/31 | default | 1550 | False | - | - |
| Ethernet8 | P2P_c3-borderleaf2_Ethernet1 | - | 10.255.202.40/31 | default | 1550 | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_c3-leaf1_Ethernet1
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.202.12/31
!
interface Ethernet2
   description P2P_c3-leaf2_Ethernet1
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.202.16/31
!
interface Ethernet3
   description P2P_c3-leaf3_Ethernet1
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.202.20/31
!
interface Ethernet4
   description P2P_c3-leaf4_Ethernet1
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.202.24/31
!
interface Ethernet5
   description P2P_c3-leaf5_Ethernet1
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.202.28/31
!
interface Ethernet6
   description P2P_c3-leaf6_Ethernet1
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.202.32/31
!
interface Ethernet7
   description P2P_c3-borderleaf1_Ethernet1
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.202.36/31
!
interface Ethernet8
   description P2P_c3-borderleaf2_Ethernet1
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.202.40/31
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | ROUTER_ID | default | 10.255.0.130/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | ROUTER_ID | default | - |

#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description ROUTER_ID
   no shutdown
   ip address 10.255.0.130/32
```

## Routing

### Service Routing Protocols Model

Multi agent routing protocol model enabled

```eos
!
service routing protocols model multi-agent
```

### IP Routing

#### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | True |

#### IP Routing Device Configuration

```eos
!
ip routing
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| default | false |

### Router BGP

ASN Notation: asplain

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65030 | 10.255.0.130 |

| BGP Tuning |
| ---------- |
| no bgp default ipv4-unicast |
| maximum-paths 4 |

#### Router BGP Peer Groups

##### EVPN-OVERLAY-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | evpn |
| Next-hop unchanged | True |
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

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive | TTL Max Hops |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- | ------------ |
| 10.255.0.132 | 65231 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.133 | 65231 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.134 | 65233 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.135 | 65233 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.136 | 65235 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.137 | 65235 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.138 | 65320 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.139 | 65320 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.202.13 | 65231 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.202.17 | 65231 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.202.21 | 65233 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.202.25 | 65233 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.202.29 | 65235 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.202.33 | 65235 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.202.37 | 65320 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.202.41 | 65320 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |

#### Router BGP EVPN Address Family

##### EVPN Peer Groups

| Peer Group | Activate | Route-map In | Route-map Out | Peer-tag In | Peer-tag Out | Encapsulation | Next-hop-self Source Interface |
| ---------- | -------- | ------------ | ------------- | ----------- | ------------ | ------------- | ------------------------------ |
| EVPN-OVERLAY-PEERS | True | - | - | - | - | default | - |

#### Router BGP Device Configuration

```eos
!
router bgp 65030
   router-id 10.255.0.130
   no bgp default ipv4-unicast
   maximum-paths 4
   neighbor EVPN-OVERLAY-PEERS peer group
   neighbor EVPN-OVERLAY-PEERS next-hop-unchanged
   neighbor EVPN-OVERLAY-PEERS update-source Loopback0
   neighbor EVPN-OVERLAY-PEERS bfd
   neighbor EVPN-OVERLAY-PEERS ebgp-multihop 3
   neighbor EVPN-OVERLAY-PEERS send-community
   neighbor EVPN-OVERLAY-PEERS maximum-routes 0
   neighbor IPv4-UNDERLAY-PEERS peer group
   neighbor IPv4-UNDERLAY-PEERS send-community
   neighbor IPv4-UNDERLAY-PEERS maximum-routes 256000
   neighbor 10.255.0.132 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.132 remote-as 65231
   neighbor 10.255.0.132 description c3-leaf1_Loopback0
   neighbor 10.255.0.133 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.133 remote-as 65231
   neighbor 10.255.0.133 description c3-leaf2_Loopback0
   neighbor 10.255.0.134 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.134 remote-as 65233
   neighbor 10.255.0.134 description c3-leaf3_Loopback0
   neighbor 10.255.0.135 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.135 remote-as 65233
   neighbor 10.255.0.135 description c3-leaf4_Loopback0
   neighbor 10.255.0.136 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.136 remote-as 65235
   neighbor 10.255.0.136 description c3-leaf5_Loopback0
   neighbor 10.255.0.137 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.137 remote-as 65235
   neighbor 10.255.0.137 description c3-leaf6_Loopback0
   neighbor 10.255.0.138 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.138 remote-as 65320
   neighbor 10.255.0.138 description c3-borderleaf1_Loopback0
   neighbor 10.255.0.139 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.139 remote-as 65320
   neighbor 10.255.0.139 description c3-borderleaf2_Loopback0
   neighbor 10.255.202.13 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.202.13 remote-as 65231
   neighbor 10.255.202.13 description c3-leaf1_Ethernet1
   neighbor 10.255.202.17 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.202.17 remote-as 65231
   neighbor 10.255.202.17 description c3-leaf2_Ethernet1
   neighbor 10.255.202.21 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.202.21 remote-as 65233
   neighbor 10.255.202.21 description c3-leaf3_Ethernet1
   neighbor 10.255.202.25 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.202.25 remote-as 65233
   neighbor 10.255.202.25 description c3-leaf4_Ethernet1
   neighbor 10.255.202.29 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.202.29 remote-as 65235
   neighbor 10.255.202.29 description c3-leaf5_Ethernet1
   neighbor 10.255.202.33 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.202.33 remote-as 65235
   neighbor 10.255.202.33 description c3-leaf6_Ethernet1
   neighbor 10.255.202.37 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.202.37 remote-as 65320
   neighbor 10.255.202.37 description c3-borderleaf1_Ethernet1
   neighbor 10.255.202.41 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.202.41 remote-as 65320
   neighbor 10.255.202.41 description c3-borderleaf2_Ethernet1
   redistribute connected route-map RM-CONN-2-BGP
   !
   address-family evpn
      neighbor EVPN-OVERLAY-PEERS activate
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS activate
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

## Filters

### Prefix-lists

#### Prefix-lists Summary

##### PL-LOOPBACKS-EVPN-OVERLAY

| Sequence | Action |
| -------- | ------ |
| 10 | permit 10.255.0.0/24 eq 32 |

#### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 10.255.0.0/24 eq 32
```

### Route-maps

#### Route-maps Summary

##### RM-CONN-2-BGP

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY | - | - | - |

#### Route-maps Device Configuration

```eos
!
route-map RM-CONN-2-BGP permit 10
   match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY
```

## VRF Instances

### VRF Instances Summary

| VRF Name | IP Routing |
| -------- | ---------- |

### VRF Instances Device Configuration

```eos
```
