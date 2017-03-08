#!/usr/bin/env python
# coding: utf-8

import optparse
import os

# Optparse简介
def main1():
    p = optparse.OptionParser()
    p.add_option('--sysadmin', '-s', default="Sukai")
    options, argument = p.parse_args()
    print "Hello, %s" % options.sysadmin


# 非选项使用模式
def main2():
    p = optparse.OptionParser(description="Python 'ls' command clone",
                              prog="pyls",
                              version="0.1",
                              usage="%prog [directory]")
    options, arguments = p.parse_args()
    if len(arguments) == 1:
        path = arguments[0]
        for filename in os.listdir(path):
            print filename
    else:
        p.print_help()

if __name__ == "__main__":
    #main1()
    main2()
