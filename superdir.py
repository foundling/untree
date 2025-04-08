#!/usr/bin/env python

from typing import List
from enum import Enum

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

class ChildType(Enum):
    File = 'File'
    Directory = 'Directory'

def read_from_pipe():
    return ''.join(line for line in fileinput.input())

def read_from_filepath(filepath:str):
    with open(filepath) as f:
        content = f.read()
    return content

def is_root(line:str):
    line = line.rstrip('\n')

def parse_indent_width(line:str):
    prefix, _ = line.split(' ')
    return len(prefix) + 1 # include space we split on

def parse_depth(line:str, indent_width:int=4):
    # distance from start to filename / indent_width
    entry_name = line.rsplit(sep=' ', maxsplit=1)[-1]
    indent = len(line) - len(entry_name) 
    return indent // indent_width

def parse_type(line:str):
    return 'dir' if line.endswith('/') else 'file'

def parse_name(line:str):
    return line.rsplit(sep=' ', maxsplit=1)[-1]

def parse_lines(lines:List[str]):
    # from line, parse: depth, type, and name from line
    root, children = lines[0], lines[1:]

    indent_width = parse_indent_width(children[0])


    for child in children:
        child_type = parse_type(child)
        child_depth = parse_depth(child, indent_width=indent_width)
        child_name = parse_name(child)
        print(child_type, child_depth, child_name)

def main():

    cli_args = sys.argv[1:]
    is_from_filepath = len(cli_args) > 0
    #is_from_pipe = sys.__stdin__ and sys.__stdin__.isatty()
    
    if (is_from_filepath):
        filepath = cli_args[0]
        with open(filepath, 'r') as f:
            lines = [line.rstrip('\n)') for line in f.readlines() if line.strip()]
            print('\n'.join(lines))
            parse_lines(lines)
        
    else:
        raise NotImplementedError


main()
