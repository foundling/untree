import os
from untree.parser import Parser, Filetype

TEST_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_data'
)

def test_parse_depth():

    schema_ascii = os.path.join(TEST_DIR, 'schema_ascii.txt')
    parser = Parser()

    with open(schema_ascii) as f:
        
        parser.load(f.read())

        parsed_line = parser.parse_first_line(parser.lines[0])

        assert parsed_line.absolute_depth == 0
        assert parsed_line.relative_depth == None
        assert parsed_line.filename == 'testdir'
        assert parsed_line.filetype ==  Filetype.directory

        parsed_line = parser.parse_subsequent_line(line=parser.lines[1], line_index=1, previous_absolute_depth=0)

        assert parsed_line.absolute_depth == 1
        assert parsed_line.relative_depth == 1
        assert parsed_line.filename == 'a'
        assert parsed_line.filetype ==  Filetype.directory

        parsed_line = parser.parse_subsequent_line(line=parser.lines[2], line_index=2, previous_absolute_depth=1)

        assert parsed_line.absolute_depth == 2
        assert parsed_line.relative_depth == 1
        assert parsed_line.filename == 'a.txt'
        assert parsed_line.filetype ==  Filetype.file

        parsed_line = parser.parse_subsequent_line(line=parser.lines[3], line_index=3, previous_absolute_depth=2)

        assert parsed_line.absolute_depth == 2
        assert parsed_line.relative_depth == 0
        assert parsed_line.filename == 'subdir_a'
        assert parsed_line.filetype ==  Filetype.directory

        parsed_line = parser.parse_subsequent_line(line=parser.lines[4], line_index=4, previous_absolute_depth=2)

        assert parsed_line.absolute_depth == 3
        assert parsed_line.relative_depth == 1
        assert parsed_line.filename == 'subdir_a.txt'
        assert parsed_line.filetype ==  Filetype.file

        parsed_line = parser.parse_subsequent_line(line=parser.lines[5], line_index=5, previous_absolute_depth=3)

        assert parsed_line.absolute_depth == 1
        assert parsed_line.relative_depth == -2
        assert parsed_line.filename == 'b'
        assert parsed_line.filetype ==  Filetype.directory

        parsed_line = parser.parse_subsequent_line(line=parser.lines[6], line_index=6, previous_absolute_depth=1)

        assert parsed_line.absolute_depth == 2
        assert parsed_line.relative_depth == 1
        assert parsed_line.filename == 'b.txt'
        assert parsed_line.filetype ==  Filetype.file