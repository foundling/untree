#!/usr/bin/env python

from untree.parser import Parser
from untree.tree import Node, walk_tree, print_node


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

    
def read_from_pipe() -> str:
    return ''.join(line for line in fileinput.input())

def read_from_filepath(filepath:str) -> str:
    
    with open(filepath) as f:
        content = f.read()
    return content

def help():
    print("[ tree -F <dir>| ] untree [[options] -s <schema file>]")

def main():

    cli_args = sys.argv[1:]  # oversimplified arg handling
    is_from_filepath = len(cli_args) > 0
    # is_from_pipe = sys.__stdin__ and not sys.__stdin__.isatty()

    tree_text : str | None = None

    if (is_from_filepath):
        with open(cli_args[0], 'r') as f:
            tree_text = f.read()
    else:
        tree_text = read_from_pipe()

    tree = Node()
    parser = Parser()
    parser.load(tree_text)

    current_node = tree
    for line_data in parser.parse():
    
        node = Node(line_data)
        current_node.add_node(node)
        current_node = node

    

    walk_tree(tree, print_node) 