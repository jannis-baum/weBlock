#!/usr/bin/python3

import socket

def recv_full_page(conn):
    header = conn.recv(4).decode('utf-8')
    while header[-4:] != '\r\n\r\n':
        header += conn.recv(1).decode('utf-8')
    
    lines = header.split('\r\n')
    for l in lines:
        if 'Content-Length' in l:
            content_len = int(l.split(': ')[1])
    document = b''
    while len(document) < content_len:
        document += conn.recv(1)
    document = document.decode('utf-8')
    
    return document

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s.bind(('', 6969))
s.listen(1)

while True:
    c, addr = s.accept()
    document = recv_full_page(c)
    print(document)
    c.send('response'.encode('utf-8'))
    c.close()

