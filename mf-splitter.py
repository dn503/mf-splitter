#!/usr/bin/python
# -*- coding: utf-8 -*-

# Unofficial Minifantasy sprite splitter and organizer by dn503 (Python is not my main language - so be kind)
# Apache License 2.0 - see accompanying file

from pathlib import Path
import sys, getopt, os

def getfilesrecursive(dir, ext):
    files = []
    dot_ext = "." + ext.lower()
    for it in os.scandir(dir):
        if it.is_file:
            if it.path.lower().endswith(dot_ext):
                files.append(it.path)
            elif it.is_dir():
                files += getfilesrecursive(it.path, ext)
    return files

def print_usage():
    print('splitter.py -i <inputdir>')

def main(argv):
    input_path = ''
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'hi:',
                ['input_path='])
    except getopt.GetoptError as err:
        print(err)
        print_usage()
        sys.exit(2)
    for (opt, arg) in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ('-i', '--input_path'):
            input_path = arg
    if input_path == '':
        print_usage()
        sys.exit(2)
        
    if not os.path.exists(input_path):
        print("supplied input_path (" + input_path + ") does not exist!")
        sys.exit(2)
        
    if not os.path.isdir(input_path):
        print("supplied input_path (" + input_path + ") is not a directory!")
        sys.exit(2)

    files = getfilesrecursive(input_path, "png")
    print(files)

if __name__ == '__main__':
    main(sys.argv)
