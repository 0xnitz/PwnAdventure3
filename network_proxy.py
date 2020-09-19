from scapy.all import sniff, TCP, Raw
from importlib import reload
import packet


def show_pack(pack):
    try:
        reload(packet)
        if pack.haslayer(Raw):
            #print(pack[Raw].load)
            payload = pack[Raw].load
            p = packet.Packet(payload)
            if len(p.parse_packet()) > 0:
                print(p.parse_packet())
    except Exception as e:
        print(e)


sniff(prn=show_pack, lfilter=lambda x: x.haslayer(TCP) and (x[TCP].dport == 3000 or x[TCP].sport == 3000))
