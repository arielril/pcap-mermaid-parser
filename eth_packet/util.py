def format_mac(b_mac: bytearray):
    return ':'.join('{:02x}'.format(x) for x in b_mac)
