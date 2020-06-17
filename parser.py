import socket
from datetime import datetime
import dpkt


def format_mac(bmac):
    return ':'.join('{:02x}'.format(x) for x in bmac)


def parse_ethernet(buf):
    # * print MAC Src, MAC Dst, Type
    return ''


def parse_arp(arp: dpkt.arp.ARP):
    # * print Type, MAC Src, MAC Dst, IP Src, IP Dst
    """
    sequenceDiagram
        Note over 1: ARP <br>Type=Request<br>MACSrc=c4:01:32:58:00:00, IPSrc=10.0.0.1<br>MACDst=c4:02:32:6b:00:00, IPDst=10.0.0.2<br>
        2->>1: ARP <br>Type=Reply<br>MACSrc=c4:02:32:6b:00:00, IPSrc=10.0.0.2
    """

    arpreq = 'Note over {}: ARP <br>Type=Request<br>MACSrc={}, IPSrc={}<br>MACDst={}, IPDst={}<br>'
    arpreply = '{}->>{}: ARP <br>Type=Reply<br>MACSrc={}, IPSrc={}'

    if arp.op == 1:
        return arpreq.format(
            socket.inet_ntoa(arp.spa),  # IP Src
            format_mac(arp.sha),  # MAC Src
            socket.inet_ntoa(arp.spa),  # IP Src
            format_mac(arp.tha),  # MAC Dst
            socket.inet_ntoa(arp.tpa),  # IP Dst
        )
    else:
        return arpreply.format(
            socket.inet_ntoa(arp.spa),  # IP Src
            socket.inet_ntoa(arp.tpa),  # IP Dst
            format_mac(arp.sha),
            socket.inet_ntoa(arp.spa),  # IP Src
        )


def parse_icmp(buf: dpkt.icmp.ICMP):
    # * print Type, Code (textual)
    icmp = 'ICMP<br>Type={}<br>Code={}'

    return icmp.format(
        buf.type,
        buf.code)


def parse_ip4(ip: dpkt.ip.IP):
    # * print IP version, IP Src, IP Dst, Proto, TTL, ID
    msg = 'IPv{}<br>IPSrc={}, IPDst={}<br>Protocol={}, TTL={}, ID={}'
    return msg.format(
        ip.v,  # version
        socket.inet_ntoa(ip.src),  # IP Src
        socket.inet_ntoa(ip.dst),  # IP Dst
        ip.p,  # protocol
        ip.ttl,  # TTL
        ip.id,  # ID
    )


def parse_ip6(buf: dpkt.ip6.IP6):
    # * print IP version, IP Src, IP Dst, Proto, TTL, ID
    return ''


def parse_tcp_udp(buf):
    # * print Src Port, Dst Port
    return ''


def parse_http(buf):
    # * Req Line, Status Line, Host
    return ''


if __name__ == "__main__":
    filepath = './examples/arp_pcap.pcap'
    n_pkt = 1

    f = open(filepath, 'rb')
    pcap_f = dpkt.pcap.Reader(f)

    for timestamp, buf in pcap_f:

        eth = dpkt.ethernet.Ethernet(buf)

        if isinstance(eth.data, dpkt.arp.ARP):
            print(parse_arp(eth.data))
        elif isinstance(eth.data, dpkt.icmp.ICMP):
            print(str(datetime.utcfromtimestamp(timestamp)), parse_icmp(eth.data))
        else:
            continue
