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

    msg = ''
    if arp.op == 1:
        msg = 'Note over {}: ARP <br>Type=Request<br>MACSrc={}, IPSrc={}<br>MACDst={}, IPDst={}<br>'
    else:
        msg = 'Note over {}: ARP <br>Type=Reply<br>MACSrc={}, IPSrc={}<br>MACDst={}, IPDst={}<br>'
    return msg.format(
        socket.inet_ntoa(arp.spa),  # IP Src
        format_mac(arp.sha),  # MAC Src
        socket.inet_ntoa(arp.spa),  # IP Src
        format_mac(arp.tha),  # MAC Dst
        socket.inet_ntoa(arp.tpa),  # IP Dst
    )


def parse_icmp(buf: dpkt.icmp.ICMP):
    # * print Type, Code (textual)
    icmp = 'ICMP<br>Type={}<br>Code={}'

    return icmp.format(
        buf.type,
        buf.code)


def get_str_protocol(p: int) -> str:
    if p == 1:
        return 'ICMP'
    elif p == 6:
        return 'TCP'
    elif p == 17:
        return 'UDP'
    elif p == 43:
        return 'IPv6-Route'
    elif p == 44:
        return 'IPv6-Frag'
    elif p == 58:
        return 'IPv6-ICMP'
    elif p == 59:
        return 'IPv6-NoNxt'
    elif p == 60:
        return 'IPv6-Opts'
    return ''


def parse_ip4(ip: dpkt.ip.IP):
    # * print IP version, IP Src, IP Dst, Proto, TTL, ID
    msg = 'IPv{}<br>IPSrc={}, IPDst={}<br>Protocol={}, TTL={}, ID={}'
    return msg.format(
        ip.v,  # version
        socket.inet_ntoa(ip.src),  # IP Src
        socket.inet_ntoa(ip.dst),  # IP Dst
        get_str_protocol(ip.p),  # protocol
        ip.ttl,  # TTL
        ip.id,  # ID
    )


def parse_ip6(buf: dpkt.ip6.IP6):
    # * print IP version, IP Src, IP Dst, Proto, TTL, ID
    return ''


def parse_tcp_udp(buf: dpkt.udp.UDP):
    # * print Src Port, Dst Port
    msg = 'TCP/UDP<br>SrcPort={}, DstPort={}'
    return msg.format(
        buf.sport,
        buf.dport,
    )


def parse_http(buf: dpkt.http):
    # * Req Line, Status Line, Host
    return ''


def get_ip_srcdst(buf: dpkt.ip.IP):
    ip_src = socket.inet_ntoa(buf.src)
    ip_dst = socket.inet_ntoa(buf.dst)
    return (ip_src, ip_dst)


if __name__ == "__main__":
    filepath = './examples/useful.pcap'
    n_pkt = 1

    f = open(filepath, 'rb')
    pcap_f = dpkt.pcap.Reader(f)
    count = 0

    print('sequenceDiagram')
    for timestamp, buf in pcap_f:
        if count >= n_pkt:
            break

        eth = dpkt.ethernet.Ethernet(buf)

        ip_src = None
        ip_dst = None

        msg = ''
        if isinstance(eth.data, dpkt.ip.IP):
            (ip_src, ip_dst) = get_ip_srcdst(eth.data)
            msg = '{}->>{}:'.format(ip_src, ip_dst)
            # print('\t', msg)

        if isinstance(eth.data, dpkt.arp.ARP):
            print('\t', msg, parse_arp(eth.data))
        if isinstance(eth.data, dpkt.icmp.ICMP):
            print('\t', msg, parse_icmp(eth.data))
        if isinstance(eth.data, dpkt.tcp.TCP):
            print('\t', msg, parse_tcp_udp(eth.data))
        if isinstance(eth.data, dpkt.udp.UDP):
            print('\t', msg, parse_tcp_udp(eth.data))
        if isinstance(eth.data, dpkt.ip.IP):
            print('\t', msg, parse_ip4(eth.data))
        if isinstance(eth.data, dpkt.http.Message):
            print('\t', msg, parse_http(eth.data))
        if not isinstance(eth.data, (dpkt.arp.ARP, dpkt.icmp.ICMP, dpkt.tcp.TCP, dpkt.udp.UDP, dpkt.ip.IP, dpkt.http.Message)):
            # print('invlid', eth)
            continue
        # count += 1
