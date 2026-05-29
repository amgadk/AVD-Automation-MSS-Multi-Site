# spine2

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
| Management1 | OOB_MANAGEMENT | oob | default | 192.168.0.112/24 | - |

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
   ip address 192.168.0.112/24
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
| Ethernet1 | P2P_leaf1_Ethernet2 | - | 10.255.201.154/31 | default | 1550 | False | - | - |
| Ethernet2 | P2P_leaf2_Ethernet2 | - | 10.255.201.158/31 | default | 1550 | False | - | - |
| Ethernet3 | P2P_leaf3_Ethernet2 | - | 10.255.201.162/31 | default | 1550 | False | - | - |
| Ethernet4 | P2P_leaf4_Ethernet2 | - | 10.255.201.166/31 | default | 1550 | False | - | - |
| Ethernet5 | P2P_leaf5_Ethernet2 | - | 10.255.201.170/31 | default | 1550 | False | - | - |
| Ethernet6 | P2P_leaf6_Ethernet2 | - | 10.255.201.174/31 | default | 1550 | False | - | - |
| Ethernet7 | P2P_borderleaf1_Ethernet2 | - | 10.255.201.178/31 | default | 1550 | False | - | - |
| Ethernet8 | P2P_borderleaf2_Ethernet2 | - | 10.255.201.182/31 | default | 1550 | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_leaf1_Ethernet2
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.201.154/31
!
interface Ethernet2
   description P2P_leaf2_Ethernet2
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.201.158/31
!
interface Ethernet3
   description P2P_leaf3_Ethernet2
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.201.162/31
!
interface Ethernet4
   description P2P_leaf4_Ethernet2
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.201.166/31
!
interface Ethernet5
   description P2P_leaf5_Ethernet2
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.201.170/31
!
interface Ethernet6
   description P2P_leaf6_Ethernet2
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.201.174/31
!
interface Ethernet7
   description P2P_borderleaf1_Ethernet2
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.201.178/31
!
interface Ethernet8
   description P2P_borderleaf2_Ethernet2
   no shutdown
   mtu 1550
   no switchport
   ip address 10.255.201.182/31
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | ROUTER_ID | default | 10.255.0.101/32 |

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
   ip address 10.255.0.101/32
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
| 65000 | 10.255.0.101 |

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
| 10.255.0.103 | 65202 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.104 | 65202 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.105 | 65204 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.106 | 65204 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.107 | 65206 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.108 | 65206 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.109 | 65300 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.0.110 | 65300 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.255.201.155 | 65202 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.201.159 | 65202 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.201.163 | 65204 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.201.167 | 65204 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.201.171 | 65206 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.201.175 | 65206 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.201.179 | 65300 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.255.201.183 | 65300 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |

#### Router BGP EVPN Address Family

##### EVPN Peer Groups

| Peer Group | Activate | Route-map In | Route-map Out | Peer-tag In | Peer-tag Out | Encapsulation | Next-hop-self Source Interface |
| ---------- | -------- | ------------ | ------------- | ----------- | ------------ | ------------- | ------------------------------ |
| EVPN-OVERLAY-PEERS | True | - | - | - | - | default | - |

#### Router BGP Device Configuration

```eos
!
router bgp 65000
   router-id 10.255.0.101
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
   neighbor 10.255.0.103 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.103 remote-as 65202
   neighbor 10.255.0.103 description leaf1_Loopback0
   neighbor 10.255.0.104 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.104 remote-as 65202
   neighbor 10.255.0.104 description leaf2_Loopback0
   neighbor 10.255.0.105 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.105 remote-as 65204
   neighbor 10.255.0.105 description leaf3_Loopback0
   neighbor 10.255.0.106 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.106 remote-as 65204
   neighbor 10.255.0.106 description leaf4_Loopback0
   neighbor 10.255.0.107 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.107 remote-as 65206
   neighbor 10.255.0.107 description leaf5_Loopback0
   neighbor 10.255.0.108 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.108 remote-as 65206
   neighbor 10.255.0.108 description leaf6_Loopback0
   neighbor 10.255.0.109 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.109 remote-as 65300
   neighbor 10.255.0.109 description borderleaf1_Loopback0
   neighbor 10.255.0.110 peer group EVPN-OVERLAY-PEERS
   neighbor 10.255.0.110 remote-as 65300
   neighbor 10.255.0.110 description borderleaf2_Loopback0
   neighbor 10.255.201.155 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.201.155 remote-as 65202
   neighbor 10.255.201.155 description leaf1_Ethernet2
   neighbor 10.255.201.159 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.201.159 remote-as 65202
   neighbor 10.255.201.159 description leaf2_Ethernet2
   neighbor 10.255.201.163 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.201.163 remote-as 65204
   neighbor 10.255.201.163 description leaf3_Ethernet2
   neighbor 10.255.201.167 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.201.167 remote-as 65204
   neighbor 10.255.201.167 description leaf4_Ethernet2
   neighbor 10.255.201.171 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.201.171 remote-as 65206
   neighbor 10.255.201.171 description leaf5_Ethernet2
   neighbor 10.255.201.175 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.201.175 remote-as 65206
   neighbor 10.255.201.175 description leaf6_Ethernet2
   neighbor 10.255.201.179 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.201.179 remote-as 65300
   neighbor 10.255.201.179 description borderleaf1_Ethernet2
   neighbor 10.255.201.183 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.255.201.183 remote-as 65300
   neighbor 10.255.201.183 description borderleaf2_Ethernet2
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
