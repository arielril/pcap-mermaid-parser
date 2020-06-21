from dpkt import dns, udp, dhcp

from .util import *


def parse_dns(udp_data: bytes) -> str:
    """
        Parse a DNS packet from a .pcap file

        udp_data: data from an UDP packet
    """
    dns_p = dns.DNS(udp_data)

    msg_q = 'DNS [op={} name={}{}{}]'
    msg_r = 'DNS [op={} name={} type={} addr={}]'

    msg = msg_q if dns_p.qr == dns.DNS_Q else msg_r

    op = 'Query' if dns_p.qr == dns.DNS_Q else 'Response'
    aa = ''
    name = ''
    tp = ''
    addr = ''

    if dns_p.qr == dns.DNS_Q:
        name = dns_p.qd[0].name

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

    return msg.format(op, name, tp, addr)


def parse_dhcp(udp_data) -> str:
    """
        Parse a DHCP packet from a .pcap file

        udp_data: data from an UDP packet
    """
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
