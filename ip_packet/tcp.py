from dpkt import http, tcp, dpkt

from .util import *


def parse_http_req(tcp_data: bytes) -> str:
    """
        Parse a HTTP Request packet from a .pcap file

        tcp_data: data from a TCP packet
    """
    msg = 'HTTP [op=Req method={} host={} uri={} v={}]'

    http_r = http.Request(tcp_data)

    method = http_r.method
    uri = http_r.uri
    version = http_r.version
    host = http_r.headers['host']

    return msg.format(method, host, uri, version)


def parse_http_res(tcp_data: bytes) -> str:
    """
        Parse a HTTP Request packet from a .pcap file

        tcp_data: data from a TCP packet
    """
    try:
        msg = 'HTTP [op=Resp v={} status_code={} status_msg={}]'
        http_r = http.Response(tcp_data)

        version = http_r.version
        status_code = http_r.status
        status_msg = http_r.reason

    except dpkt.UnpackError:
        return ''
    else:
        return msg.format(version, status_code, status_msg)


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

    if s_proto == 'HTTP' and len(tcp_p.data) > 0:
        res.append(parse_http_res(tcp_p.data))

    res.append(msg.format(tcp_p.sport, tcp_p.dport))
    return '<br>'.join(res)
