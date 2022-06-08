import socket
from typing import List

# requires flask and gevent
from flask import Flask, request
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


def get_data(address: str, port: int) -> List[str]:

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client.sendto(bytes([
        0x01, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x17,
        0x6B, 0x00, 0xFF, 0xFF,
        0x00, 0xFE, 0xFE, 0xFE,
        0xFE, 0xFD, 0xFD, 0xFD,
        0xFD, 0x12, 0x34, 0x56,
        0x78, 0xAD, 0xDE, 0x22,
        0x23, 0x9A, 0xC7, 0xBD,
        0x0F
    ]), (address, port))

    rec = client.recvfrom(1024)

    client.close()

    data = [v.decode('utf8') for v in rec[0].split(b";")[1:]]

    return data


@app.route('/', methods=['GET'])
def get_motd():
    server = request.args.get('server')
    port = request.args.get('port')
    if not server or not port:
        return 'Missing server or port'
    data = get_data(
        server, int(port))
    return {
        'server': server,
        'port': port,
        'data': {
            'server_name': data[0],
            'version_code': data[1],
            'version_name': data[2],
            'current_players': data[3],
            'max_players': data[4],
            'unknown_1': data[5],
            'level_name': data[6],
            'gamemode': data[7],
            'difficulty': data[8],
            'ipv4_port': data[9],
            'ipv6_port': data[10],
        }
    }


http_server = WSGIServer(('127.0.0.1', 1919), app)
http_server.serve_forever()
