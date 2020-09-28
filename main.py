import json
import time

from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP, UDP, ICMP
from confluent_kafka import Producer
from Packet import Packet

##################################

KAFKA_BROKER_URL = 'localhost:9092'
KAFKA_GROUP_ID = 'demo'
KAFKA_TOPIC = 'demo'
PCAP_FILE = 'data/1.pcap'


##################################

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


def packet_create(ether_pkt):
    ip_pkt = ether_pkt[IP]
    pkt = Packet(ip_pkt.src, ip_pkt.dst, ip_pkt.len, ip_pkt.proto)

    if ip_pkt.proto == 6:
        layer = ip_pkt[TCP]
    elif ip_pkt.proto == 17:
        layer = ip_pkt[UDP]
    else:
        layer = ip_pkt[ICMP]
        pkt.resp_ip_bytes = layer

    pkt.src_port = layer.sport
    pkt.dst_port = layer.dport

    return pkt


if __name__ == '__main__':
    print('Opening {}...'.format(PCAP_FILE))
    conf = {'bootstrap.servers': KAFKA_BROKER_URL}
    producer = Producer(conf)

    for (pkt_data, pkt_metadata,) in RawPcapReader(PCAP_FILE):
        ether_pkt = Ether(pkt_data)

        if 'type' not in ether_pkt.fields:
            continue

        if ether_pkt.type != 0x0800:
            continue

        print(pkt_metadata)

        pkt = packet_create(ether_pkt)

        producer.produce(KAFKA_TOPIC, key=KAFKA_GROUP_ID, value=json.dumps(pkt.__dict__), callback=acked)

        producer.poll(1)
        time.sleep(1)
