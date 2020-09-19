from scapy.all import sniff, TCP, Raw
from importlib import reload

import packet


def show_pack(pack):
    try:
        if pack.haslayer(Raw) and pack.haslayer(TCP):
            payload = pack[Raw].load
            p = packet.Packet(payload, pack[TCP].sport)
            if p.is_cmd():
                print(f'CMD packet -> {p.exec_cmd()}')
            if len(p.packet_to_str()) > 0:
                print(p.packet_to_str())
                reload(packet)
    except Exception as e:
        print(e)


sniff(prn=show_pack, lfilter=lambda x: x.haslayer(TCP) and (x[TCP].dport == 3000 or x[TCP].sport == 3000))
