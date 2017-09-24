#!/usr/bin/env python
# coding=utf-8

import os
import sys
import zipfile
import datetime
import time
import urllib2
import platform
import signal
import platform
import threading
import subprocess
try:
    reload(sys).setdefaultencoding("utf-8")
except:
    pass


join, abspath, basename = os.path.join, os.path.abspath, os.path.basename


def my_path():
    return os.path.split(os.path.realpath(__file__))[0]

def get_online_time():
    resp = urllib2.urlopen(urllib2.Request("http://www.baidu.com"))
    if resp.code == 200:
        t = resp.headers['Date']
        t = time.strptime(t, "%a, %d %b %Y %H:%M:%S %Z")
        t = datetime.datetime(*t[:6]) + datetime.timedelta(hours=8)
        t = time.mktime(t.timetuple())
        return time.localtime(t)



def get_files(root, files):
    for parent, dirnames, filenames in os.walk(root):
        for filename in filenames:
            files.append(abspath(join(parent, filename)))



def zip_files(root, files, zipName):
    tmp_zip = zipName + "!!!"
    try:
        zf = zipfile.ZipFile(tmp_zip, "w", zipfile.zlib.DEFLATED)
        for f in files:
            print(f)
            zf.write(f, f[len(root):])
        zf.close()
        os.rename(tmp_zip, zipName)
        return files
    except Exception as e:
        os.remove(tmp_zip)
        raise e
    finally:
        pass


def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir):
        os.mkdir(unziptodir, int("0777"))
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')

        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir): os.mkdir(ext_dir, int("0777"))
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()


def is_win32():
    sysstr = platform.system()
    return sysstr.lower() == "windows"


def assure_path(p):
    if os.path.exists(p):
        return True
    fullpath = os.path.abspath(p)
    ptrace = []
    while fullpath != "/" and not os.path.exists(fullpath):
        ptrace.append(fullpath)
        fullpath = os.path.dirname(fullpath)
    ptrace.reverse()
    for d in ptrace:
        os.mkdir(d)
    return os.path.exists(p)


def loop_for_ever():
    while True:
        threading._sleep(1)


class CommandLine(object):
    def __init__(self, cwd, cmd, args=None):
        self.cmd = [cmd]
        if args is not None:
            self.cmd =  self.cmd + args
        self.cwd = cwd if cwd is not '' else None
        self.proc = None
        self.timeout = 10
        self.out_log = []
        self.err_log = []
        # # for popen
        # self.executable = None
        # self.stdin = None
        # self.stdout = None
        # self.stderr = None
        # self.close_fds = False
        # self.shell = False
        # self.cwd = None

    def set_timeout(self, t):
        self.timeout = t

    def execute(self):
        print(self.cmd)
        self.proc = subprocess.Popen(
            self.cmd,
            # shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # bufsize=0,
            cwd=self.cwd,
            close_fds= not is_win32()
        )
        self.proc.wait()
        return self.proc.returncode, self.proc


def newProc(cwd, cmd, args):
    return CommandLine(cwd, cmd, args).execute()


def get_proc_by_name(name):
    try:
        if is_win32():
            p = os.popen('tasklist /FI "IMAGENAME eq %s"' % (name))
            return p.read().count(name) > 0
        for line in os.popen("ps xa"):
            fields = line.split()
            ps_name = fields[4]
            if ps_name == name:
                return True
        return False
    except:
        pass
    return False


def regulate_win32_path(p):
    if is_win32():
        return p.replace('\\', '/')
    return p


def main():
    print(str(get_online_time()))


if __name__ == "__main__":
    main()