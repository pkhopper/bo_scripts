#!/usr/bin/env python
# coding=gbk

import sys
import shutil
import time
import os
import stat
pabspath = os.path.abspath
pjoin = os.path.join


SERVER_ID = ""
CLIENT_VERSION = ""


HOST   = ""  # for one system
BIND   = ""

HOST_A = ""
HOST_B = ""
BIND_A = ""
BIND_B = ""

TAG_HOST_A = "HOST_A"
TAG_HOST_B = "HOST_B"
TAG_BIND_A = "BIND_A"
TAG_BIND_B = "BIND_B"



TAGS = None

PATH_CURR = os.path.split(os.path.realpath(__file__))[0]
PATH_ROOT = pabspath(pjoin(PATH_CURR, "../../"))
PATH_CFG = pabspath(pjoin(PATH_ROOT, "config"))
PATH_CFGFILE = pabspath(pjoin(PATH_CFG, "buildcfg.txt"))
PATH_1 = [pjoin(PATH_CFG, "app1"), pjoin(PATH_ROOT, "cfg")]
PATH_2 = [pjoin(PATH_CFG, "app2"), pjoin(PATH_ROOT, "cfg")]
PATH_3 = [pjoin(PATH_CFG, "app3"), pjoin(PATH_ROOT, "cfg")]


CFG_FILES = [
    [ PATH_1[0], PATH_1[1], ["f1.txt", "f2-2.txt"]],
    [ PATH_2[0], PATH_2[1], ["3.txt"             ]],
    [ PATH_3[0], PATH_3[1], ["4.txt"             ]],
]


def replace_tag_with_ip():
    all = ""
    for src, dest, files in CFG_FILES:
        for f in files:
            content = ""
            filename = pjoin(src, f)
            with open(filename, "r") as ff:
                content = ff.read()
                for tag, ip in TAGS.items():
                    content = content.replace(tag, ip)
            filename1 = pjoin(dest, f)
            with open(filename1, "w") as ff:
                ff.write(content)
            if filename.endswith('.sh'):
                os.chmod(filename1, stat.S_IRWXG|stat.S_IRWXU)
            all += content

    with open("buidlog.%s" % time.time(), "w") as ff:
        ff.write(all)
    print("build finish")


def backup():
    t = time.time()
    for src, dest, files in CFG_FILES:
        for f in files:
            filename = pjoin(dest, f)
            bakpath = pjoin(dest, "cfgbak")
            bakpath = pabspath(bakpath)
            if not os.path.isdir(bakpath):
                os.mkdir(bakpath)
            bakfile = "%d.%s" % (t, f)
            if os.path.isfile(filename):
                shutil.copy(filename, pjoin(bakpath, bakfile))


def check_buildcfg_file():
    global SERVER_ID
    global CLIENT_VERSION
    global HOST
    global BIND
    global HOST_A
    global HOST_B
    global BIND_A
    global BIND_B
    configs = {}
    if os.path.isfile(PATH_CFGFILE):
        with open(PATH_CFGFILE, "r") as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            lines = [line for line in lines if len(line) != 0]
            lines = [line for line in lines if not line.startswith("#")]
            lines = [line.split('=') for line in lines]
            lines = [[a.strip().lower(), b.strip().lower()] for a, b in lines]
            for a, b in lines:
                configs[a] = b
    if "host" in configs:
        HOST = configs['host']
        print("HOST", HOST)
    if "bind" in configs:
        BIND = configs['bind']
        print("BIND", BIND)
    if "host_a" in configs:
        HOST_A = configs['host_a']
        print("HOST_A", HOST_A)
    if "host_b" in configs:
        HOST_B = configs['host_b']
        print("HOST_B", HOST_B)
    if "bind_a" in configs:
        BIND_A = configs['bind_a']
        print("BIND_A", BIND_A)
    if "bind_b" in configs:
        BIND_B = configs['bind_b']
        print("BIND_B", BIND_B)
    if "server_id" in configs:
        SERVER_ID = configs['server_id']
        print("SERVER_ID", SERVER_ID)
    if "client_version" in configs:
        CLIENT_VERSION = configs['client_version']
        print("CLIENT_VERSION", CLIENT_VERSION)
    print("server type is '%s'" %(get_host_type()) )
    return True


def make_host_list(host=None):
    if host is None:
        host = get_host_type()
    if host == "a":
        set_host_type("a")
        return TAGS_A
    elif host == "b":
        set_host_type("b")
        return TAGS_B
    else:
        set_host_type("local")
        return TAGS_HOST


def set_host_type(t):
    with open("hosttype", "w") as f:
        print("set hosttype to ", t)
        f.write(t)



def get_host_type():
    try:
        with open("hosttype", "r") as f:
            t = f.read()
            return t.strip()
    except:
        pass
    return "unknown"


def get_host_a():
    global  BIND
    global  HOST_A
    t = get_host_type()
    if t == "local":
        return BIND
    elif t == "unknown":
        return BIND
    else:
        return HOST_A


def get_host_b():
    global BIND
    global HOST_B
    t = get_host_type()
    if t is "local":
        return BIND
    elif t is "unknown":
        return BIND
    else:
        return HOST_B


def get_bind_a():
    t = get_host_type()
    if t == "local":
        return BIND
    elif t == "unknown":
        return BIND
    else:
        return BIND_A


def get_bind_b():
    t = get_host_type()
    if t is "local":
        return BIND
    elif t is "unknown":
        return BIND
    else:
        return BIND_B


if __name__ == "__main__":
    if not check_buildcfg_file():
        print("check buildcfg.txt, and set ip with 'ip = ****** '")
        exit(0)
    if len(sys.argv) > 1:
        TAGS = make_host_list(sys.argv[1])
    else:
        TAGS = make_host_list()
    backup()
    replace_tag_with_ip()

