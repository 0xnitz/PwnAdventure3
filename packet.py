from struct import unpack


class ParsingException(Exception):
    def __init__(self):
        super().__init__(self)


class Packet:
    def __init__(self, payload):
        self.payload = payload
        self.type = payload[:2]

    def parse_content(self):
        if self.type == b'mv':
            x, z, y = unpack('fff', self.payload[2:14])
            return f'[Pos] ({round(x,2)},{round(y,2)},{round(z,2)})'
        elif self.type == b'jp':
            if self.payload[2]:
                return f'[Jump] ' + Packet(self.payload[3:]).parse_packet()
            return f'[Jump] ' + Packet(self.payload[3:]).parse_packet()
        elif self.type == b'*i':
            weapon_name = self.payload[4:4+unpack('H', self.payload[2:4])[0]]
            cam_x, cam_y, cam_z = unpack('fff', self.payload[4+len(weapon_name.decode()):
                                                             4+len(weapon_name.decode())+12])

            return f'[Weapon] {weapon_name.decode()} [Aim] ' \
                   f'({round(cam_x, 2)},{round(cam_y, 2)},{round(cam_z, 2)}) ' +\
                   Packet(self.payload[4+len(weapon_name.decode())+12:]).parse_packet()
        elif self.type == b's=':
            return f'[Hotbar] {self.payload[2]}'
        elif self.type == b'ee':
            return f'[Item]'

        return self.payload

    def parse_packet(self):
        try:
            return self.parse_content()
        except ParsingException:
            return 'Parse error'
