#!/usr/bin/env python
# coding=utf-8

import os
import sys
import djm
import time
import initserver
import util
import base64
import chardet

try:
    reload(sys).setdefaultencoding("utf-8")
except:
    pass


pjoin, abspath, basename = os.path.join, os.path.abspath, os.path.basename


VERB = False


CWD_SEQ = []
BIN_SEQ = []

START_SEQ = []
KILL_SEQ = []


def  set_1server(a, b, c):
    return [
               [("127.0.0.1", 1238), "", "ping", "", "www.baidu.com", 0]
           ],\
           []

set_2server_type_1 = set_1server



def get_SEQ():
    global START_SEQ
    global KILL_SEQ
    initserver.check_buildcfg_file()
    host_a = (initserver.get_bind_a(), 1238)
    host_b = (initserver.get_bind_b(), 1238)
    root_path = abspath(pjoin(initserver.PATH_CURR, "../.."))
    if initserver.get_host_type() == "local":
        START_SEQ, KILL_SEQ = set_1server(host_a, host_b, root_path)
    else:
        START_SEQ, KILL_SEQ = set_2server_type_1(host_a, host_b, root_path)


servers = djm.RemoteServers()


def execute_cmd(args):
    # (ip, port), tag, bin, cwd, params, sleep
    host, tag, exe, cwd, params, wait_sec = args
    params = params.strip().split(' ')
    server = servers.get(host[0], host[1])
    ret, raw_cmd, stdoutmsg, stderrmsg = server.StartCmd(exe, params, cwd)
    stdoutmsg = base64.b64decode(stdoutmsg)
    stderrmsg = base64.b64decode(stderrmsg)
    print(host, ret, raw_cmd, wait_sec)
    if VERB:
        print(stderrmsg)
        print(stdoutmsg)
    time.sleep(int(wait_sec))
    return ret == "ok"


def find_proc(args):
    # (ip, port), tag, bin, cwd, params, sleep
    host, tag, exe, cwd, params, wait_sec = args
    params = params.strip().split(' ')
    server = servers.get(host[0], host[1])
    found, raw_cmd, stdoutmsg, stderrmsg = server.ChkProc(exe)
    return found

def start():
    print("============ start ============")
    print("host type is ", initserver.get_host_type())
    for cmd in START_SEQ:
        if not execute_cmd(cmd):
            exit(0)
    print("============ success ============")


def stop():
    print("============ stop ============")
    for cmd in KILL_SEQ:
        execute_cmd(cmd)
        while True:
            if not find_proc(cmd):
                return
            time.sleep(1)
            print("pending proccess %s" % (cmd))
    print("============ finish ============")


if __name__ == "__main__":
    os.chdir(initserver.PATH_CURR)
    get_SEQ()
    func = None
    if sys.argv[1] == "start":
        func = start
    elif sys.argv[1] == "stop":
        func = stop
    elif sys.argv[1] == "test":
        for kk in START_SEQ:
            print(kk)
        for kk in KILL_SEQ:
            print(kk)
    else:
        print("err")

    if len(sys.argv) > 2 and sys.argv[2] == '-v':
        VERB = True
    if func:
        func()
