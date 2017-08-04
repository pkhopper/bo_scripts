#!/usr/bin/env python
# coding=utf-8

import os
import sys
import SimpleXMLRPCServer
import xmlrpclib
import util

try:
    reload(sys).setdefaultencoding("utr-8")
except:
    pass

join, abspath, basename = os.path.join, os.path.abspath, os.path.basename


####################################################################### 可编辑区域开始

BO_ROOT="~/bo"
# LS_ROOT="~/bo/linuxserver"
LOCAL_IP="127.0.0.1"
LOCAL_PORT=1238
REMOTE_PORT=1239

# ip, port, cmd, params, sleepSeconds
START_SERVER_SEQ = [
    [LOCAL_IP, LOCAL_PORT, "ping"    , ["127.0.0.1"], 3],
    [LOCAL_IP, LOCAL_PORT, "ping"    , ["127.0.0.1"], 3],
    [LOCAL_IP, LOCAL_PORT, "ps"    , ["x", "a", "u"], 3],
]

STOP_SERVER_SEQ = [
    [LOCAL_IP, LOCAL_PORT, "sayHello", ["param"], 3],
    [LOCAL_IP, LOCAL_PORT, "sayWorld", ["param"], 3],
    [LOCAL_IP, LOCAL_PORT, "StartCmd", ["param"], 3],
    [LOCAL_IP, LOCAL_PORT, "StopCmd" , ["param"], 3],
    [LOCAL_IP, LOCAL_PORT, "CheckCmd", ["param"], 3],
]

####################################################################### 可编辑区域结束


class RPC:
    def sayHello(self, p1):
        return "hello %s" % (p1)
    def sayWorld(self):
        return "world"
    def StartCmd(self, cmd, params, work_dir):
        print("StartCmd", cmd, params, work_dir)
        try:
            util.newProc(work_dir, cmd, params)

        except Exception as e:
            return e.message
        return "ok"
    def StopCmd(self, cmd):
        print("StopCmd", cmd)
        return "ok"
    def CheckCmd(self, cmd):
        print("CheckCmd", cmd)
        return "ok"



def server(local_ip="localhost", local_port=8088):
    server = SimpleXMLRPCServer.SimpleXMLRPCServer((local_ip, local_port))
    try:
        print("start server ...")
        print("Listening on port 8088")
        rpc = RPC()
        server.register_instance(rpc)
        server.serve_forever()
    except Exception as e:
        server.server_close()
        print("stop server ...")
        raise e


def client(cmds, url=r"http://localhost:8088"):
    print("start client ...")
    server = xmlrpclib.ServerProxy(url)
    for ip, port, cmd, params, pwd in START_SERVER_SEQ:
        ret = server.StartCmd(cmd, params, pwd)
        print(ret, cmd, params, pwd)
        if ret != "ok":
            print(ret)
            return
    print("command sequence finished")


def main():
    print(sys.argv)
    if sys.argv[1] == "server":
        server()
    else:
        cmds = [
            "server.sayHello",
            "server.sayWorld",
            "server.StartCmd",
            "server.StopCmd",
            "server.CheckCmd",
        ]
        client(cmds=cmds)


if __name__ == "__main__":
    try:
        print("start .....")
        main ()
    except KeyboardInterrupt as e:
        print('stop by user')
    print("stop .....")
    exit (0)
