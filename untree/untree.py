#!/usr/bin/env python

from typing import TextIO
from untree.parser import Parser
from untree.tree import Tree

'''

untree.py

untree.py [options] -s schema_file -o output_dir
tree -F --noreport . | untree.py [options]

schema file spec: exactly 'tree --charset ascii -F --noreport <directory name>'

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
    print("[ tree -F <dir>| ] untree [[options] -s <schema file>]")

def main():

    print('untree')
    cli_args = sys.argv[1:]  # oversimplified arg handling
    is_from_filepath = len(cli_args) > 0
    is_from_pipe = sys.__stdin__ and not sys.__stdin__.isatty()
    

    tree_text : str | None = None

    if (is_from_filepath):
        with open(cli_args[0], 'r') as f:
            tree_text = f.read()
    elif is_from_pipe:
        tree_text = read_from_pipe()

    else:
        help()

    if tree_text is not None:
        parser = Parser()
        parser.parse(tree_text)

        while not parser.end_of_lines():
            line_record = parser.get_next_line()
            print(line_record)