from typing import List

import untree.parser as Parser


class Node():
    # Forward References: https://peps.python.org/pep-0484/#forward-references\
    # Forward references bug with union syntax: https://bugs.python.org/issue45857

    def __init__(self, filetype:Parser.Filetype, filename:str, parent: 'None | Node' = None):
        self.children:List[Node] = []
        self.filetype = filetype
        self.filename = filename
        self.parent = parent

    def add_node(self, node:'Node') -> None:
        self.children.append(node)

class Tree():

    def __init__(self):
        self.root: None | Node = None
        self.current_node: None | Node = self.root

    def add_node(self, entry:Parser.Entry) -> None:

        # empty tree
        if not (self.root and self.current_node):
            self.root = Node(entry.filetype, entry.filename)
            self.current = self.root

        # tree with existing nodes
        else:
            node = Node(entry.filetype, entry.filename)
            self.current_node.add_node(node)