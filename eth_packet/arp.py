import socket
from dpkt import arp

from .util import *


def parse(arp_p: arp.ARP) -> str:
    """
        Parse an ARP packet from a .pcap file

        arp_p: dpkt.arp.ARP instance
    """
    # * print Type, MAC Src, MAC Dst, IP Src, IP Dst

    msg = ''
    format_opts = []

    a_type = 'Req' if arp_p.op == 1 else 'Rep'
    ip_src = socket.inet_ntoa(arp_p.spa)
    mac_src = format_mac(arp_p.sha)
    ip_dst = socket.inet_ntoa(arp_p.tpa)
    mac_dst = format_mac(arp_p.tha)

    if arp_p.op == 1:
        msg = 'Note over {}: ARP [tp={} m_src={} ip_src={} m_dst={} ip_dst={}]'
        format_opts = [ip_src, a_type, mac_src, ip_src, mac_dst, ip_dst]
    else:
        msg = '{}->>{}: ARP [tp={} m_src={} ip_src={} m_dst={} ip_dst={}]'
        format_opts = [ip_src, ip_dst, a_type,
                       mac_src, ip_src, mac_dst, ip_dst]

    return '\t'+msg.format(*format_opts)
