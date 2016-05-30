#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
update.py

Author: Jason liu
Date: 2016-02-23
"""
import getopt
import sys

from core import parse_whitelist
from core import parse_blacklist


def usage():
    print '''
Usage:update.py [-Options]
Options:
    -w or --whitelist: update whitelist
    -b or --blacklist: update blacklist
    -a or --all: update all
    -h or --help: help
Example:
    eg1:  update.py -w
    eg2:  update.py --all
    '''
try:
    opts, args = getopt.getopt(
        sys.argv[1:], 'hwba', ['help', 'whitelist', 'blacklist', 'all'])
except getopt.GetoptError:
    print 'Request parameters missing!'
    print 'Try \'update --help\' for more information.'
    sys.exit()
else:
    for op, value in opts:
        if op in ('-w', '--whitelist'):
            parse_whitelist.run()
        elif op in ('-b', '--blacklist'):
            parse_blacklist.run()
        elif op in ('-a', '--all'):
            parse_whitelist.run()
            parse_blacklist.run()
        elif op in ('-h','--help'):
            usage()
            sys.exit()
