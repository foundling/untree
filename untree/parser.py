from dataclasses import dataclass
from typing import List

from untree.tree import Tree


@dataclass
class Parser():

    lines:List[str]
    tree:Tree = Tree(None)

    def parse(self):
        pass

    def is_root(self, line:str):
        line = line.rstrip('\n')

    def parse_indent_width(self, line:str):
        prefix, _ = line.split(' ')
        return len(prefix) + 1 # include space we split on

    def parse_depth(self, line:str, indent_width:int=4):
        # distance from start to filename / indent_width
        entry_name = line.rsplit(sep=' ', maxsplit=1)[-1]
        indent = len(line) - len(entry_name) 
        return indent // indent_width

    def parse_type(self, line:str):
        return 'dir' if line.endswith('/') else 'file'

    def parse_name(self, line:str):
        return line.rsplit(sep=' ', maxsplit=1)[-1]

    def parse_lines(self, lines:List[str]):
        # from line, parse: depth, type, and name from line
        root, children = lines[0], lines[1:]

        indent_width = self.parse_indent_width(children[0])

        for child in children:
            child_type = self.parse_type(child)
            child_depth = self.parse_depth(child, indent_width=indent_width)
            child_name = self.parse_name(child)
            print(child_type, child_depth, child_name)
