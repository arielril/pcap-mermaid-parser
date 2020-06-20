from dpkt import ip, tcp, udp, icmp, http, dns, dhcp
import socket

from .util import *


def parse_icmp(icmp_p: icmp.ICMP) -> str:
    """
        Parse an ICMP packet from a .pcap file

        icmp_p: dpkt.icmp.ICMP instance
    """
    # * print Type, Code (textual)

    icmp = 'ICMP [tp={} | code={}]'

    return icmp.format(icmp_p.type, icmp_p.code)


def parse_ip4(ip: ip.IP) -> str:
    """
        Parse an IP packet from a .pcap file

        ip: dpkt.ip.IP instance
    """

    # * print IP version, IP Src, IP Dst, Proto, TTL, ID
    msg = 'IP [v={} ip_src={}, ip_dst={} proto={} ttl={} id={}]'

    return msg.format(
        ip.v,  # version
        socket.inet_ntoa(ip.src),  # IP Src
        socket.inet_ntoa(ip.dst),  # IP Dst
        get_ip_protocol(ip.p),  # protocol
        ip.ttl,  # TTL
        ip.id,  # ID
    )


# def parse_ip6(buf: ip6.IP6) -> str:
#     # * print IP version, IP Src, IP Dst, Proto, TTL, ID
#     return ''

def parse_http_req(tcp_data) -> str:
    msg = 'HTTP [op=Req method={} uri={}]'

    http_r = http.Request(tcp_data)

    method = http_r.method
    uri = http_r.uri

    return msg.format(method, uri)


def parse_tcp(tcp_p: tcp.TCP) -> str:
    """
        Parse a TCP packet from a .pcap file

        tcp_p: dpkt.tcp.TCP instance
    """
    res = []

    # * print Src Port, Dst Port
    msg = 'TCP [s_port={} d_port={}]'

    s_proto = get_tcp_protocol(tcp_p.sport)
    d_proto = get_tcp_protocol(tcp_p.dport)

    if d_proto == 'HTTP' and len(tcp_p.data) > 0:
        res.append(parse_http_req(tcp_p.data))

    res.append(msg.format(tcp_p.sport, tcp_p.dport))
    return '<br>'.join(res)


def parse_dns(udp_data) -> str:
    dns_p = dns.DNS(udp_data)

    msg_q = 'DNS [op=Query ...]'
    msg_r = 'DNS [op={} type={} name={} addr={}]'

    msg = msg_q if dns_p.qr == dns.DNS_Q else msg_r

    op = 'Query' if dns_p.qr == dns.DNS_Q else 'Response'
    aa = ''
    name = ''
    tp = ''
    addr = ''

    if dns_p.rcode == dns.DNS_RCODE_NOERR and len(dns_p.an) >= 1:
        ans = dns_p.an[0]

        if ans.type == dns.DNS_CNAME:
            name = ans.cname
            tp = 'CNAME'
        if ans.type == dns.DNS_A:
            name = ans.name
            addr = socket.inet_ntoa(ans.ip)
            tp = 'A'
        if ans.type == dns.DNS_PTR:
            name = ans.ptrname
            tp = 'PTR'

    return msg.format(op, tp, name, addr)


def parse_dhcp(udp_data) -> str:
    dhcp_p = dhcp.DHCP(udp_data)

    msg = 'DHCP [op={} ciaddr={} siaddr={}]'

    op = ''
    ciaddr = dhcp_p.ciaddr
    siaddr = dhcp_p.siaddr

    if dhcp_p.op == dhcp.DHCP_OP_REQUEST:
        op = 'Req'
    else:
        op = 'Rep'

    return msg.format(op, ciaddr, siaddr)


def parse_udp(udp_p: udp.UDP) -> iter:
    """
        Parse an UDP packet from a .pcap file

        udp_p: dpkt.udp.UDP instance
    """
    res = []

    # * print Src Port, Dst Port
    udp_msg = 'UDP [s_port={}  d_port={}]'

    s_port = udp_p.sport
    proto_sport = get_udp_protocol(s_port)
    d_port = udp_p.dport
    proto_dport = get_udp_protocol(d_port)

    if proto_sport == 'DNS' or proto_dport == 'DNS':
        res.append(parse_dns(udp_p.data))

    dhcp_possible = ['DHCPc', 'DHCPs']
    if proto_sport in dhcp_possible or proto_dport in dhcp_possible:
        res.append(parse_dhcp(udp_p.data))

    res.append(
        udp_msg.format(s_port, d_port),
    )

    return '<br>'.join(res)


def parseV4(ip_p: ip.IP) -> str:
    res = []

    (ip_src, ip_dst) = get_ip_srcdst(ip_p)
    msg_to = '{}->>{}:'.format(ip_src, ip_dst)

    res_p_str = '\t{} {}'

    if isinstance(ip_p.data, icmp.ICMP):
        res.append(parse_icmp(ip_p.data))

    if isinstance(ip_p.data, tcp.TCP):
        # if isinstance(ip_p.data, http.Message):
        #     res.append(
        #         res_p_str.format(msg_to, parse_http(ip_p.data)),
        #     )

        res.append(parse_tcp(ip_p.data))

    if isinstance(ip_p.data, udp.UDP):
        res.append(parse_udp(ip_p.data))

    res.append(parse_ip4(ip_p))

    return res_p_str.format(msg_to, '<br>'.join(res))
