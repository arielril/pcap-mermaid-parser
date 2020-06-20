import socket
from datetime import datetime
import dpkt

from eth_packet.arp import parse as parseARP
from ip_packet.ip import parseV4 as parseIPv4


def parse_ethernet(buf):
    # * print MAC Src, MAC Dst, Type
    return ''


if __name__ == "__main__":
    filepath = './examples/useful.pcap'
    n_pkt = 6

    f = open(filepath, 'rb')
    pcap_f = dpkt.pcap.Reader(f)

    print('sequenceDiagram')

    count = 0
    for timestamp, buf in pcap_f:
        if count >= n_pkt:
            break

        eth = dpkt.ethernet.Ethernet(buf)

        if isinstance(eth.data, dpkt.ip.IP):
            ip = eth.data

            print(parseIPv4(ip))

        # if isinstance(eth.data, dpkt.arp.ARP):
        #     print('\t', parseARP(eth.data))

        count += 1
