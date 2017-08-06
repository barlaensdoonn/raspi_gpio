#!/usr/bin/python3
# send messages to socketserver on raspi to change relay state
# 8/5/17
# updated 8/5/17

import socket


def encode_on():
    return 'on\r\n'.encode()


def encode_off():
    return 'off\r\n'.encode()


def raw_client(hostport, state):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(hostport)
    client.sendall(state)
    # rcv = client.recv(1024).decode().strip()
    client.close()

    return state.decode().strip()


def context_client(hostport, state):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(hostport)
        client.sendall(state)

    return state.decode().strip()


if __name__ == '__main__':
    hostport = ('192.168.1.149', 9999)

    msg = context_client(hostport, encode_on())
    print('sent: {}'.format(msg))
