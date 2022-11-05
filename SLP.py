import json
import socket
import struct

TIMEOUT_SEC = 10.0

class server:
    def __init__(self, host: str, port: int = 25565):
        self._host = host
        self._port = int(port)
        self._Reinit()

    def _Reinit(self):
        self._available = False
        self._num_players_online = 0
        self._player_names_sample = frozenset()

    def Update(self):
        self._Reinit()

        try: json_dict = GetJson(self._host, port=self._port)
        except (socket.error, ValueError) as e: return self

        try:
            self._num_players_online = json_dict['players']['online']

            if self._num_players_online:
                self._player_names_sample = frozenset(
                    player_data['name'] for player_data in json_dict['players']['sample']
                )
                    
            self._available = True
            return [(self._player_names_sample), json_dict]
        except KeyError as e: return self

    @property
    def available(self): return self._available

    @property
    def num_players_online(self): return self._num_players_online

    @property
    def player_names_sample(self): return self._player_names_sample


def GetJson(host: str, port: int = 25565):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT_SEC)
    s.connect((host, port))

    s.send(_PackData(b'\x00\x00' + _PackData(host.encode('utf8')) + _PackPort(port) + b'\x01'))
    s.send(_PackData(b'\x00'))

    unused_packet_len = _UnpackVarint(s)
    unused_packet_id = _UnpackVarint(s)
    expected_response_len = _UnpackVarint(s)

    data = b''
    while len(data) < expected_response_len: data += s.recv(1024)

    s.close()

    return json.loads(data.decode('utf8'))

def _UnpackVarint(s):
    num = 0
    for i in range(5):
        next_byte = ord(s.recv(1))
        num |= (next_byte & 0x7F) << 7*i
        if not next_byte & 0x80: break
    return num

def _PackVarint(num):
    remainder = num
    packed = b''
    while True:
        next_byte = remainder & 0x7F
        remainder >>= 7
        packed += struct.pack('B', next_byte | (0x80 if remainder > 0 else 0))
        if remainder == 0: break

    return packed

def _PackData(data_str): return _PackVarint(len(data_str)) + data_str
def _PackPort(port_num): return struct.pack('>H', port_num)
