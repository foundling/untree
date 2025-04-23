#!/usr/bin/env python

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
    is_from_pipe = sys.__stdin__ and not sys.__stdin__.isatty()
    

    tree_text : str | None = None

    if (is_from_filepath):
        with open(cli_args[0], 'r') as f:
            tree_text = f.read()
    elif is_from_pipe:
        tree_text = read_from_pipe()

    else:
        help()

    if tree_text is None:
        return


    tree = Tree()
    parser = Parser()
    parser.init(tree_text)

    # TODO:
    # + move the lines iteration into parser.parse method
    # + that exposes a callback parameter we can use to build our tree when 
    #   an entry is produced.
    prev_entry = None
    while not parser.end_of_lines():
        entry = parser.get_next_line()

        if prev_entry:

            # if we've done at least one node so far and the global depth of this
            # entry is 0, we have an error. can't have two root nodes.

            if entry.depth == 0:
                raise ValueError('Parse Error: two root directories detected.')
            
            indent = entry.depth - prev_entry.depth

            if indent > 1:
                # can't have more than 1 indent
                raise ValueError('Parse Error: expected a single indent.')
                
            tree.add_node(entry, indent=indent)
        else:
            tree.add_node(entry, indent=0)

        prev_entry = entry
    


    tree.walk(None)
