

from dataclasses import dataclass
import re
from typing import Generator, List

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
    absolute_depth: int
    relative_depth: int


class Parser():

    def __init__(self):
        self.lines:List[str] | None = None
        self.line_index: int = 0
        self.max_lines:int | None = None
        self.indent_width: int | None = None

    def load(self, content:str):

        self.lines = [ line for index, line in enumerate(content.split('\n')) if self.is_valid_line(line, index) ]
        self.line_index = 0
        self.max_lines = len(self.lines)
        self.indent_width = (None if len(self.lines) == 1
                                  else self.parse_indent_width(self.lines[1])
        )

    # TODO: decide on what you will and won't accept as tree input
    # there is bound to be 'tree-like' input on the web, can't support everything.
    @staticmethod
    def is_valid_line(line: str, index: int) -> bool:

        if index > 0 and len(line.strip()) <= 1:
            return False

        return bool(line.strip())

    # designed to be run on first indented line, aka line #1
    def parse_indent_width(self, line:str) -> int:

        parts = line.rsplit(' ', maxsplit=1)

        return (0
                if len(parts) < 2
                else len(parts[0]) + 1
        )

    def parse_depth(self, line:str, indent_width: int | None) -> int:
        '''
            calculate the depth as a multiple of the previously calculated indent width,
            returning 0 if indent width width is None.
        '''

        if indent_width is None:
            return 0

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

    def get_next_line(self, previous_absolute_depth: int) -> Data:

        if not self.lines:
            raise ValueError('no lines!')

        line:str = self.lines[self.line_index]

        absolute_depth = self.parse_depth(line, self.indent_width)
        relative_depth = absolute_depth - previous_absolute_depth

        filename = self.parse_filename(line)
        filetype = self.parse_type(line)

        self.line_index += 1

        return Data(
            filename=filename,
            filetype=filetype,
            absolute_depth=absolute_depth,
            relative_depth=relative_depth
        )

    def parse(self) -> Generator[Data, None, None]:

        prev_data = None

        while not self.end_of_lines():

            previous_absolute_depth = 0 if not prev_data else prev_data.absolute_depth
            data = self.get_next_line(previous_absolute_depth=previous_absolute_depth)

            # first line, assuming depth 0
            if  (prev_data):

                # if we've done at least one node so far and the global depth of this
                # entry is 0, we have an error. can't have two root nodes.

                if data.absolute_depth == 0:
                    raise ParseError('Parse Error: two root directories detected.')

                if data.relative_depth > 1:
                    # can't have more than 1 indent
                    raise ParseError('Parse Error: expected a single indent.')


            yield data
            prev_data = data

