#!/usr/bin/env python

from typing import TextIO
from parser import Parser

'''

superdir.py

superdir.py [options] -s schema_file
tree -F --noreport . | superdir.py [options]

spec: exactly 'tree -F --noreport'

re: tutorial: 
- packaging cli app
- tree data structure
- piped input
- performance (streams, generators, etc)
- imperative version, vs OOP version

'''

import fileinput, sys

    
def read_from_pipe():
    return ''.join(line for line in fileinput.input())

def read_from_filepath(filepath:str):
    with open(filepath) as f:
        content = f.read()
    return content

def get_lines(f:TextIO):
    return [line.rstrip('\n)') for line in f.readlines() if line.strip()]

def help():
    print("[ tree -F <dir>| ] superdir [[options] -s <schema file>]")

def main():

    cli_args = sys.argv[1:]  # oversimplified arg handling
    is_from_filepath = len(cli_args) > 0
    is_from_pipe = sys.__stdin__ and sys.__stdin__.isatty()
    
    if (is_from_filepath):
        filepath = cli_args[0]
        with open(filepath, 'r') as f:
            lines = get_lines(f)
            parser = Parser(lines)
            parser.parse()

    elif is_from_pipe:
        lines = read_from_pipe()
    else:
        help()
main()
