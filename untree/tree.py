from collections.abc import Callable
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
    
    def __repr__(self):
        return str(self.__dict__)

class Tree():

    def __init__(self):
        self.root: None | Node = None
        self.current_node: None | Node = self.root


    @staticmethod
    def print_node(node: Node | None) -> None:
        print(node.__dict__)

    def find_ancestor(self, num_ancestors: int) -> 'Node | None':

        if not self.current_node:
            return None
        
        node = self.current_node

        while num_ancestors > 0:
            node = self.current_node.parent
            num_ancestors -= 1

        return node

    def walk(self, node: Node | None, callback: Callable[[Node | None], None] | None = None):
        
        if callback is None:
            callback = Tree.print_node

        if self.root is None:
            return
               
        if node is None:
            node = self.root

        callback(node)

        if node.children and len(node.children) > 0:
            for child in node.children:
                self.walk(child, callback)

    def add_node(self, entry:Parser.Entry, indent: int) -> None:

        # empty tree
        if not (self.root and self.current_node):
            self.root = Node(entry.filetype, entry.filename)
            self.current_node = self.root

        # tree with existing nodes
        else:
            node = Node(entry.filetype, entry.filename)

            if indent > 0:
                self.current_node.children.append(node)

            elif indent == 0:
                if self.current_node.parent:
                    self.current_node.parent.children.append(node)

            else:
                parent = self.find_ancestor(abs(indent))
    
                if parent:
                    parent.children.append(node)
