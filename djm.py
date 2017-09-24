#!/usr/bin/env python
# coding=utf-8

import os
import sys
import SimpleXMLRPCServer
import xmlrpclib
import util
import base64
import getopt

try:
    reload(sys).setdefaultencoding("utf-8")
except:
    pass

join, abspath, basename = os.path.join, os.path.abspath, os.path.basename



class RPC:
    def StartCmd(self, cmd, param, cwd):
        cmd = util.regulate_win32_path(cmd)
        cwd = util.regulate_win32_path(cwd)
        print("StartCmd", cmd, param, cwd)
        cmdline = util.CommandLine(cwd, cmd, param)
        try:
            ret, proc = cmdline.execute()
            o1, o2 = "", ""
            for line in proc.stdout.readlines():
                o1 += line
            for line in proc.stderr.readlines():
                o2 += line
            print(o1)
            print(o2)
            o1 = base64.b64encode(o1)
            o2 = base64.b64encode(o2)
            if ret == 0:
                return "ok", cmdline.cmd, o1, o2
            else:
                return "failed", cmdline.cmd, o1, o2
        except Exception as e:
            err = "RPC.StartCmd, exception: %s" % (e)
            sys.stderr.writelines([err])
            return "Exception", cmdline.cmd, "", base64.b64encode(err)

    def ChkProc(self, cmd):
        err = ""
        cmd = util.regulate_win32_path(cmd)
        print("ChkProc", cmd)
        try:
            found = util.get_proc_by_name(cmd)
        except Exception as e:
            err = "RPC.ChkProc, exception: %s" % (e)
            sys.stderr.writelines([err])
            found = None
        return found, cmd, "", base64.b64encode(err)


    def PS(self):
        print("ChkProc")
        try:
            ret = os.popen("ps x")
            return ret, "ps", "", ""
        except Exception as e:
            err = "RPC.PS, exception: %s" % (e)
            sys.stderr.writelines([err])
            ret = "failed"
            return ret, "ps", "exception", base64.b32encode(err)


def serve_forever(local_ip="0.0.0.0", local_port=1238):
    server = SimpleXMLRPCServer.SimpleXMLRPCServer((local_ip, local_port))
    try:
        print("djm server listen at %s:%d" % (local_ip, local_port))
        rpc = RPC()
        server.register_instance(rpc)
        server.serve_forever()
    except Exception as e:
        server.server_close()
        raise e
    print("stop server ...")


class RemoteServers:
    def __init__(self):
        self.servers = {}

    def get(self, ip, port):
        url = r"http://%s:%s" % (ip, port)
        if url in self.servers:
            return self.servers[url]
        else:
            self.servers[url] = xmlrpclib.ServerProxy(url)
            return self.servers[url]


def test(local_ip="0.0.0.0", local_port=1238):
    servers = RemoteServers()
    client = servers.get(local_ip, local_port)
    while True:
        cmd = raw_input()
        rst = client.StartCmd(cmd, [], "")
        rst[2] = base64.b64decode(rst[2])
        print(rst[2])
        client.PS()



if __name__ == "__main__":
    ip = "0.0.0.0"
    port = 1238
    run = serve_forever
    options, args = getopt.getopt(sys.argv[1:], "csp:i:", ["help", "ip=", "port="])
    for name, value in options:
        if name in ("-i"):
            ip = value
        elif name in ("-p"):
            port = int(value)
        elif name in ("-c"):
            run = test
    run(ip, port)

