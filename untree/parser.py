from dataclasses import dataclass
from typing import List

from enum import Enum


class ParseError(Exception):

    def __init__(self, message:str):
        super().__init__(f"Parse Error: {message}")


class Filetype(Enum):
    file = 0
    directory = 1


@dataclass
class Data():
    filename: str
    filetype: Filetype
    absolute_depth: int
    relative_depth: int | None


class Parser():

    def __init__(self):
        self.lines: List[str] = []
        self.indent_width: int = 0

    def load(self, content:str):
        self.lines = [ line for index, line 
                            in enumerate(content.split('\n')) 
                            if self.is_valid_line(line, index) ]
        
        if len(self.lines) > 1:

            indent_width = self.parse_indent_width(self.lines[1])
            
            if indent_width < 1:
                raise ParseError('Invalid indent width on line 1.')
            
            self.indent_width = indent_width        


    @staticmethod
    def is_valid_line(line: str, index: int) -> bool:

        if index > 0 and len(line.strip()) <= 1:
            return False

        return bool(line.strip())

    @staticmethod
    def parse_filetype(line:str) -> Filetype:
        return Filetype.directory if line.endswith('/') else Filetype.file

    @staticmethod
    def parse_filename(line:str) -> str:
        return line.rsplit(sep=' ', maxsplit=1)[-1].rstrip('/')

    @staticmethod
    def parse_indent_width(line:str) -> int:

        parts = line.rsplit(' ', maxsplit=1)

        return (0
                if len(parts) < 2
                else len(parts[0]) + 1
        )

    def parse_depth(self, line: str, line_index: int, global_indent_width: int) -> int:
        '''
            calculate the depth as a multiple of the previously calculated indent width.
        '''

        line_indent_width = self.parse_indent_width(line)

        if line_indent_width % global_indent_width != 0:
            raise ParseError(f'Inconsistent indentation.  Got {line_indent_width} on line {line_index} but expected {global_indent_width}')

        return line_indent_width // global_indent_width

    def parse_first_line(self, line: str) -> Data:

        if self.parse_indent_width(line) > 0:
            raise ParseError(f'Invalid indent on line 1')

        return Data(
            absolute_depth = 0,
            relative_depth = None,
            filename = self.parse_filename(line),
            filetype = self.parse_filetype(line)
        )

    def parse_subsequent_line(self, line: str, line_index: int, previous_absolute_depth: int) -> Data:

        absolute_depth = self.parse_depth(line, line_index, self.indent_width)
        relative_depth = absolute_depth - previous_absolute_depth

        if absolute_depth == 0:
            # two dirs with no indents means two parents, invalid.
            raise ParseError(f'Two root directories detected at line {line_index + 1}')

        if relative_depth > 1:
            # more than one indent would mean grandchild without direct parent, invalid.
            raise ParseError('Expected a single indent.')

        return Data(
            absolute_depth = absolute_depth,
            relative_depth = relative_depth,
            filename = self.parse_filename(line),
            filetype = self.parse_filetype(line)
        )

    def parse(self) -> List[Data]:

        prev_data: Data | None = None
        parsed_lines: List[Data] = []

        for line_index, line in enumerate(self.lines):

            # first line
            if line_index < 1:
                data = self.parse_first_line(line)

            # second line or later
            else:
                
                if prev_data is None:
                    raise ParseError(f'Previous line data unexpectedly missing at line {line_index + 1}')   
                          
                data = self.parse_subsequent_line(line, line_index, previous_absolute_depth=prev_data.absolute_depth)

            parsed_lines.append(data)
            prev_data = data

        return parsed_lines

