import socket
from dpkt import ip

ip_proto_map = {
    1: 'ICMP',
    6: 'TCP',
    17: 'UDP',
    43: 'IPv6-Route',
    44: 'IPv6-Frag',
    58: 'IPv6-ICMP',
    59: 'IPv6-NoNxt',
    60: 'IPv6-Opts',
}

tcp_port_map = {
    20: 'FTP-Data',
    21: 'FTP',
    22: 'SSH',
    23: 'telnet',
    25: 'SMTP',
    43: 'whois',
    53: 'DNS',
    80: 'HTTP',
    143: 'IMAP',
    179: 'BGP',
    443: 'HTTP',
    465: 'SMTPS',
    3306: 'MySQL'
}

udp_port_map = {
    7: 'echo',
    53: 'DNS',
    67: 'DHCPc',
    68: 'DHCPs',
    138: 'netbios',
    161: 'snmp',
    5353: 'mDNS',
}


def get_ip_srcdst(buf: ip.IP):
    ip_src = socket.inet_ntoa(buf.src)
    ip_dst = socket.inet_ntoa(buf.dst)
    return (ip_src, ip_dst)


def get_ip_protocol(proto: int) -> str:
    if proto in ip_proto_map.keys():
        return ip_proto_map[proto]
    return ''


def get_udp_protocol(port: int) -> str:
    if port in udp_port_map.keys():
        return udp_port_map[port]
    return ''


def get_tcp_protocol(port: int) -> str:
    if port in tcp_port_map.keys():
        return tcp_port_map[port]
    return ''