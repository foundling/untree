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
        self.lines:List[str] = []
        self.line_index: int = 0
        self.max_lines:int | None = None
        self.indent_width: int | None = None

    @property
    def line_number(self):
        return self.line_index + 1

    def load(self, content:str):

        self.lines = [ line for index, line 
                            in enumerate(content.split('\n')) 
                            if self.is_valid_line(line, index) ]
        self.line_index = 0
        self.max_lines = len(self.lines)
        self.indent_width = self.init_indent_width()
        
    def init_indent_width(self) -> int | None:

        if len(self.lines) < 2:
            return None
        
        indent_width = self.parse_indent_width(self.lines[1])
        
        if indent_width < 1:
            raise ParseError('Invalid indent width on line 1.')
        
        return indent_width

    @staticmethod
    def is_valid_line(line: str, index: int) -> bool:

        if index > 0 and len(line.strip()) <= 1:
            return False

        return bool(line.strip())

    def end_of_lines(self) -> bool:

        if self.max_lines is None:
            return True

        return self.line_index >= self.max_lines

    def parse_filetype(self, line:str) -> Filetype:
        return Filetype.directory if line.endswith('/') else Filetype.file

    def parse_filename(self, line:str) -> str:
        return line.rsplit(sep=' ', maxsplit=1)[-1].rstrip('/')

    def parse_indent_width(self, line:str) -> int:

        parts = line.rsplit(' ', maxsplit=1)

        return (0
                if len(parts) < 2
                else len(parts[0]) + 1
        )

    def parse_depth(self, line: str, global_indent_width: int) -> int:
        '''
            calculate the depth as a multiple of the previously calculated indent width.
        '''

        line_indent_width = self.parse_indent_width(line)

        if line_indent_width % global_indent_width != 0:
            raise ParseError(f'Inconsistent indentation.  Got {line_indent_width} on line {self.line_number} but expected {global_indent_width}')

        return line_indent_width // global_indent_width

    def parse_next_line(self, line: str, previous_absolute_depth: int | None) -> Data:

        # this is first line, so we check indent width but do not parse depth
        # because it's relative to previous line.

        if previous_absolute_depth is None:

            if self.parse_indent_width(line) > 0:
                raise ParseError(f'Invalid indent on line: {self.line_number}')

            return Data(
                absolute_depth = 0,
                relative_depth = None,
                filename = self.parse_filename(line),
                filetype = self.parse_filetype(line)
            )

        elif self.indent_width is not None and self.line_index > 0:
            
            absolute_depth = self.parse_depth(line, self.indent_width)
            relative_depth = absolute_depth - previous_absolute_depth

            return Data(
                absolute_depth = absolute_depth,
                relative_depth = relative_depth,
                filename = self.parse_filename(line),
                filetype = self.parse_filetype(line)
            )
    
        else:
            raise ParseError(f'Entered an undefined parsing state on line {self.line_number}')

    def parse(self) -> List[Data]:

        prev_data: Data | None = None
        lines: List[Data] = []

        while not self.end_of_lines():
            line = self.lines[self.line_index]
            # first line
            if self.line_index == 0:

                data = self.parse_next_line(line, previous_absolute_depth=None)

                if data.absolute_depth > 0:
                    raise ParseError('Indent not allowed on first line: indent indicates file or subdirectory.')

            # second line or later
            else:

                if prev_data is None:
                    raise ParseError(f'Previous line data unexpectedly missing at line {self.line_number}')
                
                data = self.parse_next_line(line, previous_absolute_depth=prev_data.absolute_depth)

                if data.absolute_depth == 0:
                    # if prev_data exists, we've done at least one node so far. because the global depth of this
                    # entry is 0, we have an error. can't have two root nodes.
                    raise ParseError(f'Parse Error: two root directories detected at line {self.line_number}')

                if data.relative_depth is None:
                    raise ParseError(f'Previous line data unexpectedly missing at line {self.line_number}')

                if data.relative_depth > 1:
                    # can't have more than 1 indent
                    raise ParseError('Parse Error: expected a single indent.')

            lines.append(data)
            prev_data = data
            self.line_index += 1

        return lines

