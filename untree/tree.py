from collections.abc import Callable
from typing import List

import untree.parser as Parser

class NodeError(Exception):

    def __init__(self, message:str):
        raise Exception(f"Node Error: {message}")

class Node():
    # Forward References: https://peps.python.org/pep-0484/#forward-references\
    # Forward references bug with union syntax: https://bugs.python.org/issue45857

    def __init__(self, data: Parser.Data | None = None):
        self.children:List[Node] = []
        self.parent: 'Node | None' = None
        self.data = data

    def __repr__(self):
        return str(self.__dict__)
    
    def print_node(self):
        if self.data is not None:
            print(f'{self.data.absolute_depth * '----'}{self.data.filename} ({self.data.filetype.name[0]})')

    def find_ancestor(self, num_ancestors:int) -> 'Node':
        
        n = num_ancestors
        current_node = self

        while n > 0:
            if current_node.parent is None:
                raise NodeError('Found an unexpected null parent when calling find_ancestor.')
            
            n -= 1
            current_node = current_node.parent

        return current_node

    def add_node(self, node:'Node') -> None:

        if node.data is None:
            raise NodeError('Adding node with null data.')

        # schema line 1        
        if node.data.relative_depth is None:
            self.children.append(node)
            node.parent = self

        # schema lines 2 through the end
        # if it's an indent, we add to children
        elif node.data.relative_depth > 0:
            self.children.append(node)
            node.parent = self

        # if no indent, we add current node to children of parent, bc it's a sibling.
        elif node.data.relative_depth == 0:

            if self.parent is None:
                raise NodeError('Unexpectedly null parent.')
            
            self.parent.children.append(node)
            node.parent = self.parent

        # it's a dedent, aka ancestor
        else:
            parent = self.find_ancestor(abs(node.data.relative_depth))
            parent.children.append(node)
            node.parent = parent

def walk_tree(node: Node, callback: Callable[[Node], None] = lambda x: None):
    
    callback(node)

    if len(node.children) > 0:
        for child in node.children:
            walk_tree(child, callback)

def print_node(n:Node):
    n.print_node()

