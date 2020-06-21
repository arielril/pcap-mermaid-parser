import sys
import argparse
import socket
import dpkt

from eth_packet.eth import parse as parseETH
from eth_packet.arp import parse as parseARP
from ip_packet.ip import parseV4 as parseIPv4


def build_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='PCAP to Mermaid file parser',
    )

    parser.add_argument(
        'file_path',
        metavar='file_path',
        type=str,
        help='Path for the .pcap file to parse'
    )
    parser.add_argument(
        '-c', '--count',
        metavar='pkt_count',
        type=int,
        help='Number of packets to parse',
        default=999999,
        dest='pkt_count',
    )

    return parser


if __name__ == "__main__":
    parser = build_argparse()
    args = parser.parse_args()

    filepath = args.file_path
    n_packet = args.pkt_count

    try:
        f = open(filepath, 'rb')
    except FileNotFoundError:
        print('Invalid file path')
        sys.exit(1)

    pcap_f = dpkt.pcap.Reader(f)

    result = ['sequenceDiagram']

    count = 0
    for timestamp, buf in pcap_f:
        if count >= n_packet:
            break
        eth = dpkt.ethernet.Ethernet(buf)

        parsed_eth = parseETH(eth)
        eth_msg = '<br>'+parsed_eth

        if isinstance(eth.data, dpkt.ip.IP):
            ip = eth.data
            result.append(parseIPv4(ip)+eth_msg)

        if isinstance(eth.data, dpkt.arp.ARP):
            result.append(parseARP(eth.data)+eth_msg)

        count += 1

    print('\n'.join(result))
