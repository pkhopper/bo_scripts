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


class LinePair:
    def __init__(self, k, v, l, p):
        self.key_ = k
        self.val_ = v
        self.line_ = l
        self.parent = p
    def __str__(self):
        ss = "(%s, %s)" % (self.key_, self.val_)
        return ss


class Mode:
    def __init__(self):
        self.tag_ = None
        self.begin_ = None
        self.end_ = None
        self.parent = None
        self.lines_ = {}
    def __str__(self):
        ss = self.tag_
        ss += ":"
        for k, v in self.lines_.items():
            ss += str(v)
        return ss



class DJConfig:
    def __init__(self):
        self.f_ = ""
        self.content_ = ""
        self.all_ = []
        self.lines_ = []
        self.modes_ = {}

    def load(self, name):
        with open(name, "r") as f:
            self.loads(f.read())

    def loads(self, content):
        self.content_ = content
        self.all_ = self.content_.split('\n')
        self.lines_ = [(x, self.all_[x]) for x in xrange(len(self.all_))]
        self.lines_ = [(x, line.strip()) for x, line in self.lines_ if not line.strip().startswith("//")]
        self.lines_ = [(x, line) for x, line in self.lines_ if len(line) != 0]
        self.parse()

    def parse(self):
        currMode = None
        for x, line in self.lines_:
            if currMode is None:
                currMode = Mode()
                currMode.tag_ = line
            elif currMode.begin_ is None:
                assert(line == "{")
                currMode.begin_ = x
            elif line == "}":
                currMode.end_ = x
                self.modes_[currMode.tag_] = currMode
                currMode = None
            else:
                k, v = line.split('=')
                k = k.strip()
                v = v.strip()
                currMode.lines_[k] = LinePair(k, v, x, currMode)

    def set_val(self, m, k, v):
        currMode = self.modes_[m]
        kv = currMode.lines_[k]
        kv.val_ = v
        self.all_[kv.line_] = "\t%s = %s" % (k, v)
        pass

    def __str__(self):
        ss = ""
        for k, v in self.modes_.items():
            ss += str(v)
        return  ss


if __name__ == "__main__":
    ss = """
    aaa
    {
       bbb = ccccc // asdfapozxn;l

       dddd = eee // asdfapozxn;l

       fff = kkkk
    }
    bbb
    {
       bbb = ccccc // asdfapozxn;l

       dddd = eee // asdfapozxn;l

       fff = kkkk
    }
    cccc
    {
       bbb = ccccc // asdfapozxn;l

       dddd = eee // asdfapozxn;l

       fff = kkkk
    }
    """
    cfg = DJConfig()
    cfg.loads(ss)
    print cfg
    cfg.set_val("cccc", "dddd", "asdfa")
    print cfg

