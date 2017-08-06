#!/usr/bin/python3
# send messages to socketserver on raspi to change relay state
# 8/5/17
# updated 8/5/17

import socket
from datetime import datetime


def encode_now():
    now = datetime.now().strftime("%H:%M:%S")
    now += '\r\n'
    return now.encode()


def raw_client(hostport):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(hostport)
    msg = encode_now()
    client.sendall(msg)
    rcv = client.recv(1024).decode().strip()
    client.close()

    return (msg.decode().strip(), rcv)


def context_client(hostport):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(hostport)
        msg = encode_now()
        client.sendall(msg)

    return (msg.decode().strip())


if __name__ == '__main__':
    hostport = ('', 9999)

    package = context_client(hostport)
    print('sent: {}\nreceived: {}'.format(*package))
