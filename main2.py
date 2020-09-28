from scapy.compat import raw
from scapy.layers.l2 import Ether
from scapy.layers.netflow import netflowv9_defragment, NetflowSession
from scapy.sendrecv import sniff
from scapy.utils import rdpcap, RawPcapReader, PcapReader

PCAP_FILE = 'data/1.pcap'
if __name__ == '__main__':
    x = PcapReader(PCAP_FILE).read_all(1000)
    pkt = Ether(x[0])  # will loose the defragmentation
    pkt = netflowv9_defragment(pkt)[0]


