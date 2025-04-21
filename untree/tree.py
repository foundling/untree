from enum import Enum
from dataclasses import dataclass
from typing import List

class NodeType(Enum):
    File = 'File'
    Directory = 'Directory'

@dataclass
class Node():
    # Forward References: https://peps.python.org/pep-0484/#forward-references\
    # Forward references bug with union syntax: https://bugs.python.org/issue45857
    filetype:NodeType
    parent: "None | Node"
    children: List['Node']

    def add_node(self, node:'Node') -> None:
        self.children.append(node)

class Tree():
    def __init__(self):
        self.root = None

    def add_node(self, node:Node) -> None:
        raise NotImplementedError
