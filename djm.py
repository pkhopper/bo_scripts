#!/usr/bin/env python
# coding=utf-8

import os
import sys
import SimpleXMLRPCServer
import xmlrpclib
import util
import time

try:
    reload(sys).setdefaultencoding("utf-8")
except:
    pass

join, abspath, basename = os.path.join, os.path.abspath, os.path.basename


####################################################################### 可编辑区域开始

BO_ROOT="~/bo"
# LS_ROOT="~/bo/linuxserver"
LOCAL_IP="127.0.0.1"
LOCAL_PORT=1238
REMOTE_PORT=1239

####################################################################### 可编辑区域结束

def parse_cfg(cfg):
    with open(cfg, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line.split(',') for line in lines if not line.startswith('#')]
        lines = [[l.strip() for l in line] for line in lines]
        return lines


class RPC:
    def StartCmd(self, cmd, param, cwd):
        print("StartCmd", cmd, param, cwd)
        ret = "ok"
        cmdline = util.CommandLine(cwd, cmd, param)
        try:
            cmdline.execute()
        except Exception as e:
            ret = e.message
        if cmdline.proc:
            o1, o2 = cmdline.proc.stdout.read(), cmdline.proc.stderr.read()
            return ret, cmdline.cmd, o1, o2
        else:
            return ret, cmdline.cmd, "", ""



def server(local_ip="localhost", local_port=8088):
    server = SimpleXMLRPCServer.SimpleXMLRPCServer((local_ip, local_port))
    try:
        print("start server ...")
        print("Listening on port %s:%d" % (local_ip, local_port))
        rpc = RPC()
        server.register_instance(rpc)
        server.serve_forever()
    except Exception as e:
        server.server_close()
        print("stop server ...")
        raise e


def client(cfg=None, url=r"http://localhost:8088"):
    print("start client ...")
    server = xmlrpclib.ServerProxy(url)
    lines = parse_cfg(cfg)
    if lines is None:
        print("failed on read config file, ", cfg)
        return
    rst_seq = []
    for ip, port, cmd, cwd, wait_sec in lines:
        cmd = cmd.split(' ')
        ret, raw_cmd, stdoutmsg, stderrmsg = server.StartCmd(cmd[0], cmd[1:], cwd)
        print(ret, raw_cmd, stdoutmsg, stderrmsg)
        rst_seq.append([ret, raw_cmd])
        if ret != "ok":
            if cfg is "start":
                return
        time.sleep(int(wait_sec))
    print("command sequence finished")
    print(rst_seq)


def dbg_interface(url=r"http://localhost:8088"):
    print("start client ...")
    server = xmlrpclib.ServerProxy(url)
    ip, port, cmd, cwd, wait_sec = "", "", "", "", 1
    while True:
        print("==========================")
        cmd = raw_input()
        cmd = cmd.split(' ')
        ret, raw_cmd, stdoutmsg, stderrmsg = server.StartCmd(cmd[0], cmd[1:], cwd)
        if ret != "ok":
            print(stderrmsg)
        else:
            print(stdoutmsg)
        print("==========================")



def main():

    print(sys.argv)
    if sys.argv[1] == "server":
        server()
    elif sys.argv[1] == "client":
        client(cfg=sys.argv[2])
    else:
        dbg_interface()


if __name__ == "__main__":
    try:
        print("start .....")
        main ()
    except KeyboardInterrupt as e:
        print('stop by user')
    print("stop .....")
    exit (0)
