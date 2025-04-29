from untree.parser import Parser, Filetype


TEST_INPUT = '''
dir_a/
    file_a.txt
    subdir_a/
        subdir_file_a.txt
'''.strip()

def test_parse_depth_ascii():


    parser = Parser()

    assert parser.parse_depth('|-- a/', 4) == 1
    assert parser.parse_depth('|   `-- a.txt', 4) == 2
    assert parser.parse_depth('|       `-- subdir_a.txt', 4) == 3
    assert parser.parse_depth('|-- a/', 2) == 2
    assert parser.parse_depth('|   `-- a.txt', 2) == 4
    assert parser.parse_depth('|       `-- subdir_a.txt', 2) == 6

def test_parse_depth_utf8():

    parser = Parser()

    assert parser.parse_depth('├── a/', 4) == 1
    assert parser.parse_depth('│   └── a.txt', 4) == 2
    assert parser.parse_depth('│       └── subdir_a.txt', 4) == 3


    assert parser.parse_depth('├── a/', 2) == 2
    assert parser.parse_depth('│   └── a.txt', 2) == 4
    assert parser.parse_depth('│       └── subdir_a.txt', 2) == 6

def test_parse_type():

    parser = Parser()

    assert parser.parse_filetype('├── a/') == Filetype.directory
    assert parser.parse_filetype('│   └── a.txt') == Filetype.file
    assert parser.parse_filetype('│       └── subdir_a.txt') == Filetype.file
    assert parser.parse_filetype('             subdir_a/') == Filetype.directory

def test_parse_filename():

    parser = Parser()

    assert parser.parse_filename('dir_a/') == 'dir_a'
    assert parser.parse_filename('│       └── subdir_a.txt') == 'subdir_a.txt'

def test_parse_indent_width():

    parser = Parser()

    assert parser.parse_indent_width('dir_a/') == 0
    assert parser.parse_indent_width(' dir_a/') == 1
    assert parser.parse_indent_width('               dir_a/') == 15

def test_parse_next_line():

    parser = Parser()


    parser.load(TEST_INPUT)

    line1 = parser.parse_next_line(previous_absolute_depth=0)

    assert line1.filename == 'dir_a'
    assert line1.filetype == Filetype.directory
    assert line1.absolute_depth == 0
    assert line1.relative_depth == 0

    line2 = parser.parse_next_line(previous_absolute_depth=line1.absolute_depth)

    assert line2.filename == 'file_a.txt'
    assert line2.filetype == Filetype.file
    assert line2.absolute_depth == 1
    assert line2.relative_depth == 1


    line3 = parser.parse_next_line(previous_absolute_depth=line2.absolute_depth)

    assert line3.filename == 'subdir_a'
    assert line3.filetype == Filetype.directory
    assert line3.absolute_depth == 1
    assert line3.relative_depth == 0

    line4 = parser.parse_next_line(previous_absolute_depth=line3.absolute_depth)

    assert line4.filename == 'subdir_file_a.txt'
    assert line4.filetype == Filetype.file
    assert line4.absolute_depth == 2
    assert line4.relative_depth == 1