#!/usr/bin/env python
# coding=utf-8

# 在 python 2.x 下用 python 3 的 print
from __future__ import print_function

import socket
import sys
import os
import time
import getopt
try:
    reload (sys).setdefaultencoding ("utf8")
except:
    pass


class Server:
    def __init__(self):
        self.ip = ""
        self.port = 0
        self.fileName = ""
        self.timeout = 5
        self.startAt = 0
        self.sock = None
        self.conn = None
        self.peer = None
        self.dataBuffer = bytes()

    def serve_once(self, ip, port, handle):
        try:
            self.ip = ip
            self.port = port
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.ip, self.port))
            self.sock.listen(5)
            print("listen at ", self.ip, ":", self.port)
            self.conn, self.peer = self.sock.accept ()
            print("connected by ", self.peer)
            self.startAt = time.time()
            self.recv(handle)
            print("")
            print("finish")
            self.sock.close()
        except Exception as e:
            print(e)
            self.close()

    def recv(self, handle):
        begin = time.time()
        print('Connected by ', self.peer, ' at ', time.localtime(begin))
        recv_len = 0
        while True:
            # if you got some data, then break after wait sec
            if time.time() - begin > self.timeout:
                break
            try:
                data = self.conn.recv (50*1024*1024)
                if data:
                    recv_len += len(data)
                    handle(data, recv_len)
                    # print("\rsize=%d, %dM" % (len(self.dataBuffer), len(self.dataBuffer)/(1024*1024)), end='')
                    begin = time.time()
                else:
                    break
            except socket.error as e:
                if not e.errno == 11:
                    raise e

    def close(self):
        if self.sock:
            self.sock.close()



class Client:
    def __init__(self):
        self.ip = ""
        self.port = 0
        self.timeout = 30
        self.startAt = 0
        self.sock = None
        self.dataBuffer = bytes()

    def connect(self, ip, port):
        try:
            self.ip = ip
            self.port = port
            self.sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            ret = self.sock.connect_ex((self.ip, self.port))
            if ret == 0:
                print("connected")
            return True
        except Exception as e:
            print(e)
            self.close()
        return False

    def send(self, data, total):
        data_send = 0
        try:
            data_send += self.sock.send (data)
            if len (data) == data_send:
                print("\rsend %s            " % (len (data)), end='')
            else:
                print("err, send ", data_send)
                raise "err, send %d" % (data_send)
        except OSError as e:
            print(e)
            self.close()

    def close(self):
        if self.sock:
            self.sock.close()


class handle_data:
    def __init__(self, name):
        self.name = name
        self.file = None

    def __del__(self):
        if self.file:
            self.file.close()

    def __call__(self, data, recv_len):
        if not self.file:
            self.file = open(self.name, "wb")
            if self.file is None:
                return
        self.file.write(data)
        print("\rsize=%d, %dM" % (recv_len, recv_len / (1024 * 1024)), end='')


def server(ip, port, fileName, force):
    if os.path.exists(fileName):
        print("file exist ", fileName)
        if not force:
            return
    s = Server()
    handle = handle_data(fileName)
    s.serve_once(ip, port, handle)


def client(ip, port, fileName):
    if not os.path.exists (fileName):
        print("file not exist ", fileName)
        return
    client = Client ()
    if not client.connect(ip, port):
        print("err, not connected")
        return
    total = os.path.getsize(fileName)
    curr_size = 0
    with open(fileName, "rb") as f:
        while True:
            data = f.read()
            if data:
                client.send(data, total)
                curr_size += len(data)
            else:
                break
    if curr_size != total:
        print("err, file=%s, len=%d" % (fileName, curr_size))
    print("")
    print("finish")


def print_usage(optArray):
    print("""
    transfer
    """, optArray)


def main():
    global CONFIG
    optArray = [
        "client",
        "server",
        "force",
        "ip=",
        "port=",
        "file=",
    ]
    PARAM = {}
    for cmd in optArray:
        if cmd.endswith ('='):
            PARAM[cmd.replace ('=', '')] = None
        else:
            PARAM[cmd] = False
    check = lambda x: x in PARAM and PARAM[x]

    try:
        opts, args = getopt.getopt (sys.argv[1:], "hic:", optArray)
    except getopt.GetoptError as e:
        print(e)
        print_usage (optArray)
        return
    if len (opts) == 0:
        print_usage (optArray)
        return
    for opt, arg in opts:
        if arg is not "":
            PARAM[opt.replace ('-', '')] = arg
        else:
            PARAM[opt.replace ('-', '')] = True

    if check ("client"):
        client (PARAM["ip"], int(PARAM["port"]), PARAM["file"])

    if check ("server"):
        server(PARAM["ip"], int(PARAM["port"]), PARAM["file"], PARAM["force"])


if __name__ == "__main__":
    try:
        main ()
    except KeyboardInterrupt as e:
        print('stop by user')
    exit (0)

