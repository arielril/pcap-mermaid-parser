import socket
from dpkt import ethernet

from .util import *


def parse(eth: ethernet.Ethernet) -> str:
    """
        Parse an Ethernet packet from a .pcap file

        eth: dpkt.ethernet.Ethernet instance
    """
    msg = 'ETH [src={} dst={} type={}]'

    src = format_mac(eth.src)
    dst = format_mac(eth.dst)
    tp = '0x{:04x}'.format(eth.type)

    return msg.format(src, dst, tp)
