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
    reload(sys).setdefaultencoding("utr-8")
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
    def __init__(self, pwd, cmd, args):
        self.cmd = [cmd] + args
        self.proc = None
        self.timeout = 10

    def set_timeout(self, t):
        self.timeout = t

    def execute(self):
        print(self.cmd, )
        self.proc = subprocess.Popen(
            self.cmd,
            stdout=sys.stdout,
            stderr=sys.stderr,
            bufsize=0,
        )
        self.proc.wait()
        if self.proc.returncode != 0:
            raise Exception("[err] ret=%d, %s" % (self.proc.returncode, self.cmd))
        return self.proc


def newProc(pwd, cmd, args):
    return CommandLine(pwd, cmd, args).execute()



def main():
    print(str(get_online_time()))


if __name__ == "__main__":
    main()