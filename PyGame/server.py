import socket
from _thread import *
import threading as thr
import json
from conf import HOST, PORT
import pickle
import math

from pprint import pprint


class Server:
    def __init__(self):
        self.HOST = HOST
        self.PORT = int(PORT)
        self.server_socket = socket.socket()

        self.connected = {}
        self.winner = None
        try:
            self.server_socket.bind((self.HOST, self.PORT))

            print('Waiting for a Connection..')
            self.server_socket.listen(2)  # listen for 2 clients
            while True:
                client, address = self.server_socket.accept()
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                self.connected[address[1]] = {
                    'ready': False,
                    'field': [[{'x': col, 'y': row, 'colored': False, 'hit': False} for col in range(10)] for row in
                              range(10)],
                    'enemy_fields': [[{'x': col, 'y': row, 'colored': False, 'hit': False} for col in range(10)] for row
                                     in range(10)],
                    'move': False
                }
                start_new_thread(self.threaded_client, (client, thr.current_thread().ident, address[1],))
                print(self.connected)
            self.server_socket.close()
        except socket.error as e:
            print(str(e))

    def reinit(self):
        pass

    def handle_data(self, data, port):
        if 'command' not in data:
            raise Exception('there is no command')

        if data['command'] == 'reinit':
            self.reinit()
            return {'result': True}

        if data['command'] == 'init_ships':
            self.connected[port]['field'] = data['game_field']
            self.connected[port]['ready'] = True

            players_ready = True
            for player_port in self.connected:
                if not self.connected[player_port]['ready']:
                    players_ready = False

            if not players_ready:
                self.connected[port]['move'] = True

            if players_ready:
                print('Players are ready')
                return {'result': True, 'waiting': False}
            else:
                return {'result': True, 'waiting': True}

        if data['command'] == 'is_opponent_ready':
            players_ready = True
            for player_port in self.connected:
                if not self.connected[player_port]['ready']:
                    players_ready = False

            if players_ready:
                print('Players are ready')
                return {'result': True, 'waiting': False}
            else:
                return {'result': True, 'waiting': True}

        if data['command'] == 'send_hit':
            end_game = False
            target_player = [self.connected[p] for p in self.connected if p != port][0]
            if self.connected[port]['move']:
                x_new = data['x']
                y_new = data['y']
                print('SEND HIT', x_new, y_new)
                hit = False
                for x, col in enumerate(target_player['field']):
                    for y, cell in enumerate(col):
                        if x_new == x and y_new == y:
                            if cell['colored']:
                                hit = True
                                cell['hit'] = True
                            else:
                                cell['hit'] = True

                for x, col in enumerate(self.connected[port]['enemy_fields']):
                    for y, cell in enumerate(col):
                        if x_new == x and y_new == y:
                            print(cell)
                            cell['colored'] = True
                            cell['hit'] = hit

                if not hit:
                    print('MISS')
                    self.connected[port]['move'] = False
                    target_player['move'] = True

                counter = 0
                for x, col in enumerate(target_player['field']):
                    for y, cell in enumerate(col):
                        if cell['hit']:
                            counter += 1
                if counter == 20:
                    self.winner = port
                    end_game = True

                return {'result': True, 'hit': hit, 'end_game': end_game}

            return {'result': False, 'end_game': end_game}

        if data['command'] == 'get_fields':
            target_player = {}
            try:
                target_player = [self.connected[p] for p in self.connected if p != port][0]
            except:
                target_player = {
                    'ready': False,
                    'ships': [],
                    'field': [[{'x': col, 'y': row, 'colored': False} for col in range(10)] for row in range(10)]
                }
            winner = None
            if self.winner is not None:
                winner = self.winner == port

            return {
                'result': True,
                'field': self.connected[port]['field'],
                'enemy_field': self.connected[port]['enemy_fields'],
                'winner': winner,
            }

        if data['command'] == 'is_my_turn':
            return {'status': True, 'move': self.connected[port]['move']}

    def threaded_client(self, connection, thread_id, port):
        connection.send(str(thread_id).encode())
        while True:
            raw_data = connection.recv(16384)
            if not raw_data:
                print('Disconnect')
                del self.connected[port]
                print(self.connected)
                break
            data = pickle.loads(raw_data)
            res = self.handle_data(data, port)
            connection.sendall(pickle.dumps(res))
        connection.close()


if __name__ == '__main__':
    server = Server()
