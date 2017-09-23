#!/usr/bin/env python
# coding=utf-8

import os
import sys
import SimpleXMLRPCServer
import xmlrpclib
import util
import base64

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
                o1 += line + '\n'
            for line in proc.stderr.readlines():
                o2 += line + '\n'
            o1 = base64.b64encode(o1)
            o2 = base64.b64encode(o2)
            if ret == 0:
                return "ok", cmdline.cmd, o1, o2
            else:
                return "failed", cmdline.cmd, o1, o2
        except Exception as e:
            err = "RPC.StartCmd, exception: %s" % (e)
            sys.stderr.writelines([err])
            return "failed", cmdline.cmd, e.message, err

    def ChkProc(self, cmd):
        cmd = util.regulate_win32_path(cmd)
        print("ChkProc", cmd)
        try:
            found = util.get_proc_by_name(cmd)
        except Exception as e:
            print e.message
            found = None
        o1, o2 = "*", "*"
        return found, cmd, o1, o2


    def PS(self):
        print("ChkProc")
        ret = "ok"
        try:
            ret = os.popen("ps x")
        except Exception as e:
            print e.message
            ret = "failed"
        o1, o2 = "*", "*"
        return ret, "ps", o1, o2


def serve_forever(local_ip="0.0.0.0", local_port=1238):
    server = SimpleXMLRPCServer.SimpleXMLRPCServer((local_ip, local_port))
    try:
        print("start server ...")
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


if __name__ == "__main__":
    ip = "0.0.0.0"
    port = 1238
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    if len(sys.argv) > 2:
        port = sys.argv[2]
    serve_forever(ip, port)
