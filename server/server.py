#!/usr/bin/python3

import socket, re
from bs4 import BeautifulSoup

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


def normalize_text(text):
    return ''.join([character for character in text.lower() if character not in ['.', ',', '?', ';', '"', '#', '\'', '!', '‘', '’', '“', '”', '…', ':', '\n', '  ']])


def censor_document_test(document):
    parts = document.split('</head>')
    document = parts[0] + '</head>U R fucked m8' + parts[1]
    return document


def censor_guardian(document):
    soup = BeautifulSoup(document, features="lxml")
    
    textp = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p'])
    
    full_text = [text.text for text in textp]
    full_text = ' '.join(full_text)
    return full_text
        

with open('testhtml.html', 'r') as fp:
    document = fp.read()

text = censor_guardian(document)
print(normalize_text(text))


'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s.bind(('', 6969))
s.listen(1)

while True:
    c, addr = s.accept()
    document = recv_full_page(c)
    with open('html.html', 'w') as fp:
        fp.write(document)
    #print(document)
    response = censor_guardian(document)
    c.send(response.encode('utf-8'))
    c.close()
'''