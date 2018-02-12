#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time
import logging
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
import queue

pjoin, pabspath, pbasename = os.path.join, os.path.abspath, os.path.basename


def get_logger(logfile=None, level=logging.DEBUG):
    logger = logging.getLogger()
    if logfile:
        hdlr = logging.FileHandler(logfile)
        hdlr.setLevel(level=level)
        formatter = logging.Formatter("%(asctime)s[%(levelname)s] %(message)s")
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
    console = logging.StreamHandler()
    console.setLevel(level)
    formatter = logging.Formatter("%(asctime)s[%(levelname)s] %(message)s")
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.setLevel(level)
    return logger

def work(fpath, t, log):
    tt = os.path.getmtime(fpath)
    if tt > t:
        os.utime(fpath, (t, t))
        log.info("[%d] %s, %s", os.getpid(), time.localtime(tt), fpath)
    # else:
    #     log.debug("[%d] no, %d, %s", os.getpid(), tt, fpath)



def main1():
    pp = sys.argv[1]
    log = get_logger(level=logging.DEBUG)
    pool = ThreadPool(10)
    q = queue.Queue()
    i = 0
    total = 0
    try:
        t = time.time()
        print(time.localtime(t))
        for root, dirs, files in os.walk(pp, True):
            for f in files:
                fpath = pjoin(root, f)
                # q.put(pool.apply_async(work, (fpath, t, log)))
                pool.apply_async(work, (fpath, t, log))
                total += 1
        log.info("total=%d, q=%d, t=%d", total, q.qsize(), time.time() - t)
        pool.close()
        pool.join()
        log.info("finish, total=%d, q=%d, t=%d", total, q.qsize(), time.time() - t)
        print(time.localtime())
    except Exception as e:
        log.exception(e)
        pool.terminate()
        raise
    finally:
        pool.join()


def main():
    pp = sys.argv[1]
    log = get_logger(level=logging.DEBUG)
    t = time.time()
    total = 0
    print(time.localtime(t))
    all = []
    for root, dirs, files in os.walk(pp, True):
        for f in files:
            fpath = pjoin(root, f)
            all.append(fpath)
            total += 1

    log.info("total=%d, t=%d", total, time.time() - t)
    print(time.localtime())

if __name__ == "__main__":
    try:
        main1()
    except KeyboardInterrupt as e:
        print('stop by user')
        exit(0)
