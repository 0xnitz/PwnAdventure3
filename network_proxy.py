from scapy.all import sniff, TCP, Raw
import packet
import importlib
import sys

targetPort = ''

if len(sys.argv) > 1:
    targetPort = int(sys.argv[1])

def show_pack(pack, port=''):
    if pack.haslayer(Raw) and pack.haslayer(TCP):
        if targetPort != '' and pack[TCP].sport != targetPort:
            return

        payload = pack[Raw].load
        p = packet.Packet(payload, pack[TCP].sport)
        if len(p.parse_packet()) > 0:
            print(p.parse_packet())
            importlib.reload(packet)


sniff(prn=show_pack, lfilter=lambda x: x.haslayer(TCP) and x[TCP].dport == 3000)
