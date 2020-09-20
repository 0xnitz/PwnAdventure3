from struct import pack, unpack


last_pos = b''
height = 0

CHAT = b'#*'

POSITION = b'mv'
JUMP = b'jp'

WEAPON = b'*i'
FR = b'fr'
RELOAD = b'rl'

HOTBAR_SWITCH = b's='
ITEM_PICKUP = b'ee'
ITEM_SERVER = b'cp'
AREA_CHANGE = b'ch'

ENEMY_UNKNOWN = b'xx'
ENEMY_ATTACK = b'tr'
ENEMY_POS = b'st'
ENEMY_SPAWN = b'mk'

SERVER_SHOT = b'la'
SERVER_POSITION = b'ps'

MANA_REG = b'ma'
HP_REG = b'++'

RESPAWN = b'rs'


class ParsingException(Exception):
    def __init__(self):
        super().__init__(self)


class Packet:
    def __init__(self, payload, sport=0):
        self.payload = payload
        self.type = payload[:2]
        self.sport = sport

    def is_cmd(self):
        return self.type == CHAT and self.sport != 3000

    def exec_cmd(self):
        cmd = self.packet_to_str()[7:]
        packet = b''
        if cmd[:3] == '$tp':
            x, y, z = [float(x) for x in cmd.split()[1:]]
            packet = last_pos
            return packet[:2] + pack('fff', x, z, y) + packet[14:]
        #elif cmd[:5] == 'hover':
        #    global height
        #    height = [float(x) for x in cmd.split()[1:]]

        return packet

    def packet_to_str(self):
        if self.type == POSITION:
            global last_pos
            last_pos = self.payload
            x, z, y = unpack('fff', self.payload[2:14])
            return ''
            return f'[Pos] ({round(x,2)},{round(y,2)},{round(z,2)})'
        elif self.type == JUMP:
            return f'[Jump] {self.payload[2]}'
        elif self.type == WEAPON:
            weapon_name = self.payload[4:4+unpack('H', self.payload[2:4])[0]]
            cam_x, cam_y, cam_z = unpack('fff', self.payload[4+len(weapon_name.decode()):
                                                             4+len(weapon_name.decode())+12])

            return f'[Weapon] {weapon_name.decode()} [Aim] ' \
                   f'({round(cam_x, 2)},{round(cam_y, 2)},{round(cam_z, 2)}) ' +\
                   Packet(self.payload[4+len(weapon_name.decode())+12:]).packet_to_str()
        elif self.type == HOTBAR_SWITCH:
            return f'[Hotbar] {self.payload[2]}'
        elif self.type == ITEM_PICKUP:
            return f'[Item]'
        elif self.type == RELOAD:
            if self.payload[2:4] == b'mv':
                return f'[Reload]'
            else:
                return f'<- [Reload]'
        elif self.type == SERVER_POSITION:
            return ''
            return f'<- [Pos]'
        elif self.type == HP_REG:
            return ''
            return f'<- [HP Reg]'
        elif self.type == MANA_REG:
            return ''
            return f'<- [Mana Reg]'
        elif self.type == ENEMY_ATTACK:
            return f'<- [Enemey ATK]'
        elif self.type == ENEMY_POS:
            return f'<- [Enemy Pos]'
        elif self.type == SERVER_SHOT:
            return f'<- [Shot]'
        elif self.type == ENEMY_UNKNOWN:
            return f'<- [Enemy ?]'
        elif self.type == FR:
            return f'[fr] {self.payload[2]}' + Packet(self.payload[3:]).packet_to_str()
        elif self.type == ENEMY_SPAWN:
            name_length = unpack('H', self.payload[11:13])[0]
            return f'<- [Enemy] {self.payload[13:13+name_length].decode()}'
        elif self.type == ITEM_SERVER:
            item_name_length = unpack('H', self.payload[2:4])[0]
            return f'<- [Item] {self.payload[4:4+item_name_length].decode()}'
        elif self.type == AREA_CHANGE:
            area_length = unpack('H', self.payload[2:4])[0]
            return f'<- [Area] {self.payload[4:4+area_length].decode()}'
        elif self.type == RESPAWN:
            return f'[RESPAWN]'
        elif self.type == CHAT:
            if self.sport != 3000:
                message_length = unpack('H', self.payload[2:4])[0]
                return f'[Chat] {self.payload[4:4+message_length].decode()}'
            else:
                message_length = unpack('H', self.payload[6:8])[0]
                return f'<- [Chat] {self.payload[8:8+message_length].decode()}'
        elif self.type == b'\x00\x00':
            return ''
            return f'[ACK]'
        elif len(self.payload) == 0:
            return ''

        return self.payload
