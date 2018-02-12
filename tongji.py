#!/usr/bin/env python
# coding=utf-8

import os
import sys
import re

try:
    reload(sys).setdefaultencoding("utf-8")
except:
    pass


join, abspath, basename = os.path.join, os.path.abspath, os.path.basename


def load(ppp):
    line_num = 0
    total = 0
    sum = 0
    with open(ppp, "r") as f:
        reg = re.compile("\[(\d+),(\d+)\]")
        while True:
            lines = f.readlines(1000)
            if len(lines) == 0:
                break
            for line in lines:
                line_num += 1
                if line.find("UpdateGSSCharacterData") < 0:
                    continue
                m = reg.findall(line)
                if len(m) == 0:
                    continue
                a = int(m[0][0])
                b = int(m[0][1])
                sum += a + b
                total += 1
    print(sum, total, sum / total)



def load1(ppp):
    total = 0
    sum = 0
    with open(ppp, "r") as f:
        reg = re.compile("\[(\d+),(\d+)\]")
        while True:
            lines = f.readlines(1000)
            if len(lines) == 0:
                break
            for line in lines:
                rr = line.find(r"GetCharacterFullData")
                if rr < 0:
                    continue
                m = reg.findall(line)
                if len(m) == 0:
                    continue
                a = int(m[0][0])
                b = int(m[0][1])
                sum += a + b
                total += 1
    print(sum, total, sum / total)


def main():

    ss = r"F:\bug\djdsz-801-2017-10-17\djdsz-801-2017-10-17\nml\nml-2017-10-17"
    load(ss)

if __name__ == "__main__":
    main()
