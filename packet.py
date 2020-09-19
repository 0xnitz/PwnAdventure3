from struct import unpack

class ParsingException(Exception):
    def __init__(self):
        super().__init__(self)

class Packet:
    def __init__(self, payload, sport):
        self.payload = payload[2:]
        self.type = payload[:2]
        self.associatedPort = sport

    def parse_content(self, type, payload):
        if type == b'mv':
            x, z, y = unpack('fff', payload[:12])
            return f'({round(x,2)}, {round(y,2)}, {round(z,2)})'
        elif type == b'jp':
            if payload[0]:
                return f'Jump git -> ' + Packet(payload[1:], self.associatedPort).parse_packet()
            return f'EJmp -> ' + Packet(payload[1:], self.associatedPort).parse_packet()

        raise ParsingException()


    def parse_packet(self):
        try:
            return f'FROM {self.associatedPort} --> ' + self.parse_content(self.type, self.payload)
        except ParsingException:
            return 'Parse error'

    
