import socket
from dpkt import arp

from .util import *


def parse(arp_p: arp.ARP) -> str:
    """
        Parse an ARP packet from a .pcap file

        arp_p: dpkt.arp.ARP instance
    """
    # * print Type, MAC Src, MAC Dst, IP Src, IP Dst

    msg = 'Note over {}: ARP [tp={} | m_src={}, ip_src={} | m_dst={}, ip_dst={}]'
    a_type = 'Req' if arp_p.op == 1 else 'Rep'

    return msg.format(
        socket.inet_ntoa(arp_p.spa),  # IP Src
        a_type,
        format_mac(arp_p.sha),  # MAC Src
        socket.inet_ntoa(arp_p.spa),  # IP Src
        format_mac(arp_p.tha),  # MAC Dst
        socket.inet_ntoa(arp_p.tpa),  # IP Dst
    )
