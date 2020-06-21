# PCAP to Mermaid file parser

## Description
Parser for `.pcap` files to [Mermaid](https://mermaid-js.github.io/mermaid/#/) representation. This parser reads a `.pcap` file and outputs a Mermaid [Sequence Diagram](https://mermaid-js.github.io/mermaid/#/sequenceDiagram) in the stdout of the console.

## Usage

```sh
$ python3 parser.py -h

usage: parser.py [-h] [-c pkt_count] file_path

PCAP to Mermaid file parser

positional arguments:
  file_path             Path for the .pcap file to parse

optional arguments:
  -h, --help            show this help message and exit
  -c pkt_count, --count pkt_count
                        Number of packets to parse
```

### Dependencies
- Python >= 3
- DPKT >= 1.9.2

To install the dependencies for this project you can run this command:

```sh
$ pip3 install -r dependencies.txt
```

## Protocols
Supported protocols and values that are shown in the sequence diagram.

### Data Link Layer (OSI L2)
- [Ethernet](https://en.wikipedia.org/wiki/Ethernet)
  - MAC Src
  - MAC Dest
  - Type
- [ARP](https://en.wikipedia.org/wiki/Address_Resolution_Protocol)
  - Type
  - MAC Src
  - MAC Dest
  - IP Src
  - IP Dest

### Network Layer (OSI L3)
- [IP](https://en.wikipedia.org/wiki/Internet_Protocol)
  - Version
  - IP Src
  - IP Dest
  - Protocol
  - TTL
  - Identification (ID)
- [ICMP](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol)
  - Type
  - Code

### Transport Layer (OSI L4)
- [TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
  - Port Src
  - Port Dest
- [UDP](https://en.wikipedia.org/wiki/User_Datagram_Protocol)
  - Port Src
  - Port Dest

### Application Layer (OSI L7)
- [DHCP](https://en.wikipedia.org/wiki/DHCP)
  - Operation
  - Client IP Address
  - Your IP Address
  - Server IP Address
  - Gateway IP Address
  - Client Hardware Address
- [DNS](https://en.wikipedia.org/wiki/DNS)
  - Operation
  - Name
  - Type 
  - Address
- [HTTP](https://en.wikipedia.org/wiki/HTTP)
  - Request
    - Method
    - Host
    - URI
    - Version
  - Response
    - Version
    - Status Code
    - Status Message


## Examples

### Arp Request/Reply
```sh
$ python3 parser.py examples/arp.pcap
```

```mermaid
sequenceDiagram
	Note over 10.0.0.1: ARP [tp=Req m_src=c4:01:32:58:00:00 ip_src=10.0.0.1 m_dst=c4:02:32:6b:00:00 ip_dst=10.0.0.2]<br>ETH [src=c4:01:32:58:00:00 dst=c4:02:32:6b:00:00 type=0x0806]
	10.0.0.2->>10.0.0.1: ARP [tp=Rep m_src=c4:02:32:6b:00:00 ip_src=10.0.0.2 m_dst=c4:01:32:58:00:00 ip_dst=10.0.0.1]<br>ETH [src=c4:02:32:6b:00:00 dst=c4:01:32:58:00:00 type=0x0806]
```

### Ping with Fragmented Packets
```sh
$ python3 parser.py examples/frag-ping.pcap
```

```mermaid
sequenceDiagram
	192.168.0.107->>104.18.21.134: ICMP [tp=8 code=0 desc=Echo request]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=104.18.21.134 proto=ICMP ttl=64 id=45989]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>104.18.21.134: IP [v=4 ip_src=192.168.0.107, ip_dst=104.18.21.134 proto=ICMP ttl=64 id=45989]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	104.18.21.134->>192.168.0.107: ICMP [tp=0 code=0 desc=Echo reply]<br>IP [v=4 ip_src=104.18.21.134, ip_dst=192.168.0.107 proto=ICMP ttl=52 id=34070]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	104.18.21.134->>192.168.0.107: IP [v=4 ip_src=104.18.21.134, ip_dst=192.168.0.107 proto=ICMP ttl=52 id=34070]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>104.18.21.134: ICMP [tp=8 code=0 desc=Echo request]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=104.18.21.134 proto=ICMP ttl=64 id=46291]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>104.18.21.134: IP [v=4 ip_src=192.168.0.107, ip_dst=104.18.21.134 proto=ICMP ttl=64 id=46291]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	104.18.21.134->>192.168.0.107: ICMP [tp=0 code=0 desc=Echo reply]<br>IP [v=4 ip_src=104.18.21.134, ip_dst=192.168.0.107 proto=ICMP ttl=52 id=34476]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	104.18.21.134->>192.168.0.107: IP [v=4 ip_src=104.18.21.134, ip_dst=192.168.0.107 proto=ICMP ttl=52 id=34476]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>104.18.21.134: ICMP [tp=8 code=0 desc=Echo request]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=104.18.21.134 proto=ICMP ttl=64 id=26348]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>104.18.21.134: IP [v=4 ip_src=192.168.0.107, ip_dst=104.18.21.134 proto=ICMP ttl=64 id=26348]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	104.18.21.134->>192.168.0.107: ICMP [tp=0 code=0 desc=Echo reply]<br>IP [v=4 ip_src=104.18.21.134, ip_dst=192.168.0.107 proto=ICMP ttl=52 id=34901]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	104.18.21.134->>192.168.0.107: IP [v=4 ip_src=104.18.21.134, ip_dst=192.168.0.107 proto=ICMP ttl=52 id=34901]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>104.18.21.134: ICMP [tp=8 code=0 desc=Echo request]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=104.18.21.134 proto=ICMP ttl=64 id=61276]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>104.18.21.134: IP [v=4 ip_src=192.168.0.107, ip_dst=104.18.21.134 proto=ICMP ttl=64 id=61276]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	104.18.21.134->>192.168.0.107: ICMP [tp=0 code=0 desc=Echo reply]<br>IP [v=4 ip_src=104.18.21.134, ip_dst=192.168.0.107 proto=ICMP ttl=52 id=35206]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	104.18.21.134->>192.168.0.107: IP [v=4 ip_src=104.18.21.134, ip_dst=192.168.0.107 proto=ICMP ttl=52 id=35206]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>104.18.21.134: ICMP [tp=8 code=0 desc=Echo request]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=104.18.21.134 proto=ICMP ttl=64 id=31888]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>104.18.21.134: IP [v=4 ip_src=192.168.0.107, ip_dst=104.18.21.134 proto=ICMP ttl=64 id=31888]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	104.18.21.134->>192.168.0.107: ICMP [tp=0 code=0 desc=Echo reply]<br>IP [v=4 ip_src=104.18.21.134, ip_dst=192.168.0.107 proto=ICMP ttl=52 id=35355]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	104.18.21.134->>192.168.0.107: IP [v=4 ip_src=104.18.21.134, ip_dst=192.168.0.107 proto=ICMP ttl=52 id=35355]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
```

### HTTP Request with DNS Resolution 
> HTTP Request: curl ipinfo.io

```sh
$ python3 parser.py examples/ipinfo-http.pcap
```

```mermaid
sequenceDiagram
	192.168.0.107->>8.8.8.8: DNS [op=Query name=ipinfo.io]<br>UDP [s_port=65137  d_port=53]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=8.8.8.8 proto=UDP ttl=255 id=50449]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	8.8.8.8->>192.168.0.107: DNS [op=Response name=ipinfo.io type=A addr=216.239.38.21]<br>UDP [s_port=53  d_port=65137]<br>IP [v=4 ip_src=8.8.8.8, ip_dst=192.168.0.107 proto=UDP ttl=113 id=59243]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>216.239.38.21: TCP [s_port=50302 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=216.239.38.21 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	216.239.38.21->>192.168.0.107: TCP [s_port=80 d_port=50302]<br>IP [v=4 ip_src=216.239.38.21, ip_dst=192.168.0.107 proto=TCP ttl=113 id=4896]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>216.239.38.21: TCP [s_port=50302 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=216.239.38.21 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>216.239.38.21: HTTP [op=Req method=GET host=ipinfo.io uri=/ v=1.1]<br>TCP [s_port=50302 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=216.239.38.21 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	216.239.38.21->>192.168.0.107: TCP [s_port=80 d_port=50302]<br>IP [v=4 ip_src=216.239.38.21, ip_dst=192.168.0.107 proto=TCP ttl=113 id=4932]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	216.239.38.21->>192.168.0.107: HTTP [op=Resp v=1.1 status_code=200 status_msg=OK]<br>TCP [s_port=80 d_port=50302]<br>IP [v=4 ip_src=216.239.38.21, ip_dst=192.168.0.107 proto=TCP ttl=113 id=5024]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>216.239.38.21: TCP [s_port=50302 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=216.239.38.21 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>216.239.38.21: TCP [s_port=50302 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=216.239.38.21 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	216.239.38.21->>192.168.0.107: TCP [s_port=80 d_port=50302]<br>IP [v=4 ip_src=216.239.38.21, ip_dst=192.168.0.107 proto=TCP ttl=113 id=5044]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>216.239.38.21: TCP [s_port=50302 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=216.239.38.21 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
```

### DHCP Example
```sh
$ python3 parser.py examples/dhcp.pcap
```

```mermaid
sequenceDiagram
	0.0.0.0->>255.255.255.255: DHCP [op=Req ciaddr=0.0.0.0 yiaddr=0.0.0.0 siaddr=0.0.0.0 giaddr=0.0.0.0 chaddr=00:0b:82:01:fc:42]<br>UDP [s_port=68  d_port=67]<br>IP [v=4 ip_src=0.0.0.0, ip_dst=255.255.255.255 proto=UDP ttl=250 id=43062]<br>ETH [src=00:0b:82:01:fc:42 dst=ff:ff:ff:ff:ff:ff type=0x0800]
	192.168.0.1->>192.168.0.10: DHCP [op=Rep ciaddr=0.0.0.0 yiaddr=192.168.0.10 siaddr=192.168.0.1 giaddr=0.0.0.0 chaddr=00:0b:82:01:fc:42]<br>UDP [s_port=67  d_port=68]<br>IP [v=4 ip_src=192.168.0.1, ip_dst=192.168.0.10 proto=UDP ttl=128 id=1093]<br>ETH [src=00:08:74:ad:f1:9b dst=00:0b:82:01:fc:42 type=0x0800]
	0.0.0.0->>255.255.255.255: DHCP [op=Req ciaddr=0.0.0.0 yiaddr=0.0.0.0 siaddr=0.0.0.0 giaddr=0.0.0.0 chaddr=00:0b:82:01:fc:42]<br>UDP [s_port=68  d_port=67]<br>IP [v=4 ip_src=0.0.0.0, ip_dst=255.255.255.255 proto=UDP ttl=250 id=43063]<br>ETH [src=00:0b:82:01:fc:42 dst=ff:ff:ff:ff:ff:ff type=0x0800]
	192.168.0.1->>192.168.0.10: DHCP [op=Rep ciaddr=0.0.0.0 yiaddr=192.168.0.10 siaddr=0.0.0.0 giaddr=0.0.0.0 chaddr=00:0b:82:01:fc:42]<br>UDP [s_port=67  d_port=68]<br>IP [v=4 ip_src=192.168.0.1, ip_dst=192.168.0.10 proto=UDP ttl=128 id=1094]<br>ETH [src=00:08:74:ad:f1:9b dst=00:0b:82:01:fc:42 type=0x0800]
```

### Complete execution of almost all protocols
```sh
$ python3 parser.py examples/complete-flow.pcap
```

```mermaid
sequenceDiagram
	192.168.0.107->>8.8.8.8: DNS [op=Query name=www.google.com]<br>UDP [s_port=62095  d_port=53]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=8.8.8.8 proto=UDP ttl=255 id=28331]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	8.8.8.8->>192.168.0.107: DNS [op=Response name=www.google.com type=A addr=172.217.28.4]<br>UDP [s_port=53  d_port=62095]<br>IP [v=4 ip_src=8.8.8.8, ip_dst=192.168.0.107 proto=UDP ttl=116 id=55868]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>172.217.28.4: TCP [s_port=49821 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=172.217.28.4 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	172.217.28.4->>192.168.0.107: TCP [s_port=80 d_port=49821]<br>IP [v=4 ip_src=172.217.28.4, ip_dst=192.168.0.107 proto=TCP ttl=112 id=45353]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>172.217.28.4: TCP [s_port=49821 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=172.217.28.4 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>172.217.28.4: HTTP [op=Req method=GET host=www.google.com uri=/ v=1.1]<br>TCP [s_port=49821 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=172.217.28.4 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	172.217.28.4->>192.168.0.107: TCP [s_port=80 d_port=49821]<br>IP [v=4 ip_src=172.217.28.4, ip_dst=192.168.0.107 proto=TCP ttl=112 id=45376]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	172.217.28.4->>192.168.0.107: <br>TCP [s_port=80 d_port=49821]<br>IP [v=4 ip_src=172.217.28.4, ip_dst=192.168.0.107 proto=TCP ttl=113 id=45447]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	172.217.28.4->>192.168.0.107: <br>TCP [s_port=80 d_port=49821]<br>IP [v=4 ip_src=172.217.28.4, ip_dst=192.168.0.107 proto=TCP ttl=113 id=45448]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	172.217.28.4->>192.168.0.107: <br>TCP [s_port=80 d_port=49821]<br>IP [v=4 ip_src=172.217.28.4, ip_dst=192.168.0.107 proto=TCP ttl=113 id=45450]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	172.217.28.4->>192.168.0.107: <br>TCP [s_port=80 d_port=49821]<br>IP [v=4 ip_src=172.217.28.4, ip_dst=192.168.0.107 proto=TCP ttl=113 id=45451]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>172.217.28.4: TCP [s_port=49821 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=172.217.28.4 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>172.217.28.4: TCP [s_port=49821 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=172.217.28.4 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>172.217.28.4: TCP [s_port=49821 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=172.217.28.4 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	172.217.28.4->>192.168.0.107: <br>TCP [s_port=80 d_port=49821]<br>IP [v=4 ip_src=172.217.28.4, ip_dst=192.168.0.107 proto=TCP ttl=113 id=45508]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>172.217.28.4: TCP [s_port=49821 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=172.217.28.4 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>172.217.28.4: TCP [s_port=49821 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=172.217.28.4 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>172.217.28.4: TCP [s_port=49821 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=172.217.28.4 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	172.217.28.4->>192.168.0.107: TCP [s_port=80 d_port=49821]<br>IP [v=4 ip_src=172.217.28.4, ip_dst=192.168.0.107 proto=TCP ttl=113 id=45599]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>172.217.28.4: TCP [s_port=49821 d_port=80]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=172.217.28.4 proto=TCP ttl=64 id=0]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	192.168.0.107->>8.8.8.8: DNS [op=Query name=www.asseponto.com.br]<br>UDP [s_port=49574  d_port=53]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=8.8.8.8 proto=UDP ttl=255 id=46376]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	8.8.8.8->>192.168.0.107: DNS [op=Response name=www.asseponto.com.br type=A addr=200.98.136.201]<br>UDP [s_port=53  d_port=49574]<br>IP [v=4 ip_src=8.8.8.8, ip_dst=192.168.0.107 proto=UDP ttl=112 id=56255]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>200.98.136.201: ICMP [tp=8 code=0 desc=Echo request]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=200.98.136.201 proto=ICMP ttl=64 id=11938]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	200.98.136.201->>192.168.0.107: ICMP [tp=0 code=0 desc=Echo reply]<br>IP [v=4 ip_src=200.98.136.201, ip_dst=192.168.0.107 proto=ICMP ttl=109 id=15866]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	192.168.0.107->>200.98.136.201: ICMP [tp=8 code=0 desc=Echo request]<br>IP [v=4 ip_src=192.168.0.107, ip_dst=200.98.136.201 proto=ICMP ttl=64 id=32757]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0800]
	200.98.136.201->>192.168.0.107: ICMP [tp=0 code=0 desc=Echo reply]<br>IP [v=4 ip_src=200.98.136.201, ip_dst=192.168.0.107 proto=ICMP ttl=109 id=15867]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0800]
	Note over 192.168.0.1: ARP [tp=Req m_src=1c:3b:f3:3c:04:26 ip_src=192.168.0.1 m_dst=00:00:00:00:00:00 ip_dst=192.168.0.107]<br>ETH [src=1c:3b:f3:3c:04:26 dst=a4:83:e7:17:09:33 type=0x0806]
	192.168.0.107->>192.168.0.1: ARP [tp=Rep m_src=a4:83:e7:17:09:33 ip_src=192.168.0.107 m_dst=1c:3b:f3:3c:04:26 ip_dst=192.168.0.1]<br>ETH [src=a4:83:e7:17:09:33 dst=1c:3b:f3:3c:04:26 type=0x0806]
```

## Resources
Here is a list of resources used to build this parser. Not all of the resources are being used in the final version, they were used for knowledge before I started to develop this parser.

- [Mermaid Diagrams](https://mermaid-js.github.io/mermaid/#/flowchart)
- [DPKT Python](https://dpkt.readthedocs.io/en/latest/index.html). Tutorial [example](https://jon.oberheide.org/blog/2008/10/15/dpkt-tutorial-2-parsing-a-pcap-file/). Program [example](https://chains.readthedocs.io/en/latest/)
- [cheatsheet dpkt](https://engineering-notebook.readthedocs.io/en/latest/engineering/dpkt.html)
- [DPKT User Doc](http://www.commercialventvac.com/dpkt.html#mozTocId319619)
- [DPKT User Examples](https://github.com/jeffsilverm/dpkt_doc)
- [WinPcap in your programs](https://www.winpcap.org/docs/docs_412/html/group__wpcapsamps.html). Pcap file parser in c/c++
- [PcapPlusPlus](https://pcapplusplus.github.io/docs/tutorials/intro). Pcap tutorial in c++
- [Reading Pcap files with Scapy](https://incognitjoe.github.io/reading-pcap-with-scapy.html). Pcap parsing with [scapy](https://scapy.readthedocs.io/en/latest/introduction.html)
- [How to capture and analyze packets with tcpdum](https://www.linuxtechi.com/capture-analyze-packets-tcpdump-command-linux/)
- [pcap-ct](https://pypi.org/project/pcap-ct/)
- [pypcap](https://github.com/pynetwork/pypcap)
- [sample](https://wiki.wireshark.org/SampleCaptures) captures wireshark

## Roadmap
- [ ] Add live presentation after parsing the .pcap file
- [ ] Add support fore more protocols
- [ ] Add filters for the parsing like [tcpdump filters](https://www.tcpdump.org/manpages/pcap-filter.7.html)
- [ ] Add colored visual representation of the request and responses for each protocol
- [ ] Add live packet capture and parsing of packets
