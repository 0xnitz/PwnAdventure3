from scapy.all import sniff, TCP, Raw
from importlib import reload
from sys import argv

import packet

targetPort = ''

if len(argv) > 1:
    targetPort = int(argv[1])


def show_pack(pack, port=''):
    try:
        if pack.haslayer(Raw) and pack.haslayer(TCP):
            payload = pack[Raw].load
            p = packet.Packet(payload)
            if len(p.parse_packet()) > 0:
                print(p.parse_packet())
                reload(packet)
    except Exception as e:
        print(e)


sniff(prn=show_pack, lfilter=lambda x: x.haslayer(TCP) and (x[TCP].dport == 3000 or x[TCP].sport == 3000))
