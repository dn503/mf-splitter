#!/usr/bin/python
# -*- coding: utf-8 -*-

# Unofficial Minifantasy sprite splitter and organizer by dn503 (Python is not my main language - so be kind)
# Apache License 2.0 - see accompanying file

import sys, getopt

def usage():
    print('splitter.py -i <inputdir>')

def main(argv):
    inputdir = ''
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'hi:',
                ['inputdir='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for (opt, arg) in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ('-i', '--inputdir'):
            inputdir = arg
    if inputdir == '':
        usage()
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv)

