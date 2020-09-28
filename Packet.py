class Packet:
    def __init__(self, src_ip, dst_ip, orig_ip_bytes, proto, resp_pkts, resp_ip_bytes):
        self.src = src_ip
        self.dst = dst_ip
        self.orig_ip_bytes = orig_ip_bytes
        self.orig_pkts = 0
        self.src_port = 0
        self.dst_port = 0
        self.resp_pkts = resp_pkts
        self.resp_ip_bytes = resp_ip_bytes
        self.proto = proto
