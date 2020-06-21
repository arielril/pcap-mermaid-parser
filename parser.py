import socket
import dpkt

from eth_packet.eth import parse as parseETH
from eth_packet.arp import parse as parseARP
from ip_packet.ip import parseV4 as parseIPv4


if __name__ == "__main__":
    filepath = './examples/arp_pcap.pcap'
    n_packet = 20

    f = open(filepath, 'rb')
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
