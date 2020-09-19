from scapy.all import sniff, TCP, Raw
import packet
import importlib

def show_pack(pack):
    if pack.haslayer(Raw):
        #print(pack[Raw].load)
        payload = pack[Raw].load
        p = packet.Packet(payload)
        if len(p.parse_packet()) > 0:
            print(p.parse_packet())
            importlib.reload(packet)


sniff(prn=show_pack, lfilter=lambda x: x.haslayer(TCP) and x[TCP].dport == 3000)
