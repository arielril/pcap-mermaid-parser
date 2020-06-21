from dpkt import ip, tcp, udp, icmp, http, dns, dhcp
import socket

from .tcp import *
from .udp import *
from .util import *


def parse_icmp(icmp_p: icmp.ICMP) -> str:
    """
        Parse an ICMP packet from a .pcap file

        icmp_p: dpkt.icmp.ICMP instance
    """
    # * print Type, Code (textual)

    icmp = 'ICMP [tp={} code={} desc={}]'
    desc = get_icmp_description(icmp_p.type, icmp_p.code)

    return icmp.format(icmp_p.type, icmp_p.code, desc)


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


def parseV4(ip_p: ip.IP) -> str:
    res = []

    (ip_src, ip_dst) = get_ip_srcdst(ip_p)
    msg_to = '{}->>{}:'.format(ip_src, ip_dst)

    res_p_str = '\t{} {}'

    if isinstance(ip_p.data, icmp.ICMP):
        res.append(parse_icmp(ip_p.data))

    if isinstance(ip_p.data, tcp.TCP):
        res.append(parse_tcp(ip_p.data))

    if isinstance(ip_p.data, udp.UDP):
        res.append(parse_udp(ip_p.data))

    res.append(parse_ip4(ip_p))

    return res_p_str.format(msg_to, '<br>'.join(res))
