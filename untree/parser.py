

from dataclasses import dataclass
import re
from typing import List

from enum import Enum

class ParseError(Exception):
    pass

class Filetype(Enum):
    file = 0
    directory = 1

@dataclass
class Data():
    filename: str
    filetype: Filetype


class Parser():

    def __init__(self):
        self.lines:List[str] | None = None
        self.line_index: int = 0
        self.max_lines:int | None = None
        self.indent_width: int | None = None

    def load(self, content:str):
        self.lines = [line for line in content.split('\n') if line.strip()]
        self.line_index = 0
        self.max_lines = len(self.lines)

    def parse(self):
            
        prev_data = None

        while not self.end_of_lines():

            data, depth = self.get_next_line()

            if prev_data:

                # if we've done at least one node so far and the global depth of this
                # entry is 0, we have an error. can't have two root nodes.

                if depth == 0:
                    raise ParseError('Parse Error: two root directories detected.')
                
                indent = depth - depth

                if indent > 1:
                    # can't have more than 1 indent
                    raise ParseError('Parse Error: expected a single indent.')
                    
                yield data, indent

            else:
                yield data, 0


            prev_data = data
    

    # designed to be run on first indented line, aka line #1
    def parse_indent_width(self, line:str) -> int:
        
        parts = line.rsplit(' ', maxsplit=1)

        return (0
                if len(parts) < 2
                else len(parts[0]) + 1
        )

    def parse_depth(self, line:str, indent_width:int=4) -> int:
        
        # distance from start to filename / indent_width
        
        entry_name = line.rsplit(sep=' ', maxsplit=1)[-1]
        indent = len(line) - len(entry_name)

        return indent // indent_width

    def parse_type(self, line:str) -> Filetype:
        return Filetype.directory if line.endswith('/') else Filetype.file

    def parse_filename(self, line:str) -> str:
        return line.rsplit(sep=' ', maxsplit=1)[-1].rstrip('/')

    def end_of_lines(self) -> bool:

        if self.max_lines is None:
            return True
        
        return self.line_index >= self.max_lines
    
    def get_next_line(self):

        if not self.lines:
            raise ValueError('no lines!')
        
        line:str = self.lines[self.line_index]

        # since we require a root, line #2 should tell us the indent width
        if self.line_index == 1:
            self.indent_width = self.parse_indent_width(line)

        filename = self.parse_filename(line)
        filetype = self.parse_type(line)   
        depth = (0 if self.indent_width is None 
                   else self.parse_depth(line, indent_width = self.indent_width))


        self.line_index += 1
        
        return Data(filename=filename, filetype=filetype), depth
