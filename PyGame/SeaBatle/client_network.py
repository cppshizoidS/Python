import socket
import json
import pickle

from conf import HOST, PORT


class NetworkClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = HOST
        self.port = PORT
        self.addr = (self.server, self.port)
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(16384).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(16384))
        except socket.error as e:
            print(e)
            return None

    def init_ships_server(self, ships, game_field):
        data = {
            'command': 'init_ships',
            'ships': ships,
            'game_field': game_field
        }
        return self.send(data)

    def is_opponent_ready(self):
        data = {
            'command': 'is_opponent_ready',
        }
        return self.send(data)

    def send_hit(self, x, y):
        data = {
            'command': 'send_hit',
            'x': x,
            'y': y,
        }
        return self.send(data)

    def get_fields(self):
        data = {
            'command': 'get_fields',
        }
        return self.send(data)

    def is_my_turn(self):
        data = {
            'command': 'is_my_turn'
        }
        return self.send(data)

