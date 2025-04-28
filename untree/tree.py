from collections.abc import Callable
from typing import List

import untree.parser as Parser


class Node():
    # Forward References: https://peps.python.org/pep-0484/#forward-references\
    # Forward references bug with union syntax: https://bugs.python.org/issue45857

    def __init__(self, data: Parser.Data, parent: 'None | Node' = None):
        self.children:List[Node] = []
        self.parent = parent
        self.data = data

    def __repr__(self):
        return str(self.__dict__)
    
    def print_node(self):
        print(f'{self.data.absolute_depth * '----'}{self.data.filename} ({self.data.filetype.name[0]})')

class Tree():

    def __init__(self):
        self.root: None | Node = None
        self.last_node_added: None | Node = None

    def find_ancestor(self, num_ancestors: int) -> 'Node | None':

        if not self.last_node_added:
            return None
        
        node = self.last_node_added

        while num_ancestors >= 0:
            p = node.parent.data.filename
            node = node.parent
            num_ancestors -= 1

        return node


    def add_node(self, data:Parser.Data) -> None:

        node = Node(data)

        # empty tree
        if not (self.last_node_added):
            self.root = node

        # tree with existing nodes
        else:

            # if it's an indent, we add current node as child of prev.
            if node.data.relative_depth > 0:
                self.last_node_added.children.append(node)
                node.parent = self.last_node_added

            # if no indent, we add current node to children of parent, bc it's a sibling.
            elif node.data.relative_depth == 0:
                if self.last_node_added.parent:
                    self.last_node_added.parent.children.append(node)
                    node.parent = self.last_node_added.parent

            else:
                parent = self.find_ancestor(abs(node.data.relative_depth))
    
                if parent:
                    parent.children.append(node)
        

        self.last_node_added = node



    def walk(self, node: Node | None = None, callback: Callable[[Node], None] = lambda x: None):
        
        if self.root is None:
            return
        
        if node is None:            
            node = self.root

        callback(node)

        if len(node.children) > 0:
            for child in node.children:
                self.walk(child, callback)


def print_node(n:Node):
    n.print_node()

