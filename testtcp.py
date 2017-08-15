#coding=utf-8


import time
import socket
import os
import sys


HOST = ""
PORT = 3006

class CONN:
    def __init__(self):
        self.sock = None

    def conn(self, ip, port):
        try:
            self.sock = socket.socket()
            self.sock.connect((ip, port))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    HOST = sys.argv[1]
    PORT = int(intsys.argv[2])
    conns = []
    while True:
        conn = CONN()
        conn.conn(HOST, PORT)
        conns.append(conn)
        time.sleep(1)
        print(len(conns))

