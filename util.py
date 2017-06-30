#!/usr/bin/env python
# coding=utf-8

import os
import sys
import zipfile
import datetime
import time
import urllib2


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



def main():
    print(str(get_online_time()))


if __name__ == "__main__":
    main()