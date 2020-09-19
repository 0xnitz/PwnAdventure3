from struct import unpack


class Packet:
    def __init__(self, payload):
        self.payload = payload[2:]
        self.type = payload[:2]

    def parse_packet(self):
        if self.type == b'mv':
            x, z, y = unpack('fff', self.payload[:12])
            return f'({round(x,2)},{round(y,2)},{round(z,2)})'
        elif self.type == b'jp':
            if self.payload[0]:
                return f'Jump -> ' + Packet(self.payload[1:]).parse_packet()
            return f'EJmp -> ' + Packet(self.payload[1:]).parse_packet()

        return ''
