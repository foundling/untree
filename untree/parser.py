


from dataclasses import dataclass
from typing import List

from enum import Enum

class Filetype(Enum):
    file = 0
    directory = 1

@dataclass
class FileRecord():
    depth: int
    filename: str
    filetype: Filetype

@dataclass
class Parser():

    lines:List[str] | None = None
    line_index: int = 0
    max_lines:int | None = None
    indent_width: int = 0

    def parse(self, content:str):
        self.lines = [line for line in content.split('\n') if line.strip()]
        self.line_index = 0
        self.max_lines = len(self.lines)


    def parse_indent_width(self, line:str) -> int:
        prefix, _ = line.split(' ')
        return len(prefix) + 1 # include space we split on

    def parse_depth(self, line:str, indent_width:int=4) -> int:
        # distance from start to filename / indent_width
        entry_name = line.rsplit(sep=' ', maxsplit=1)[-1]
        indent = len(line) - len(entry_name) 
        return indent // indent_width

    def parse_type(self, line:str) -> Filetype:
        return Filetype.directory if line.endswith('/') else Filetype.file

    def parse_filename(self, line:str) -> str:
        return line.rsplit(sep=' ', maxsplit=1)[-1]

    def end_of_lines(self) -> bool:

        if self.max_lines is None:
            return True
        
        return self.line_index >= self.max_lines
    
    def get_next_line(self):

        if not self.lines:
            raise ValueError('no lines!')
        
        # from line, parse: depth, type, and name from line
        line:str = self.lines[self.line_index]
        self.line_index += 1

        if self.line_index == 0:
            self.indent_width = self.parse_indent_width(line)

        filename = self.parse_filename(line)
        depth = self.parse_depth(line)
        filetype = self.parse_type(line)

        return FileRecord(depth=depth, filename=filename, filetype=filetype)