from untree.parser import Parser, Filetype

TEST_INPUT = '''
dir_a/
  file_a.txt
  subdir_a/
    subdir_file_a.txt
'''.strip()

def test_parse_depth_ascii():


    parser = Parser()

    assert parser.parse_depth('|-- a/', indent_width=4) == 1
    assert parser.parse_depth('|   `-- a.txt', indent_width=4) == 2
    assert parser.parse_depth('|       `-- subdir_a.txt', indent_width=4) == 3
    assert parser.parse_depth('|-- a/', indent_width=2) == 2
    assert parser.parse_depth('|   `-- a.txt', indent_width=2) == 4
    assert parser.parse_depth('|       `-- subdir_a.txt', indent_width=2) == 6

def test_parse_depth_utf8():

    parser = Parser()

    assert parser.parse_depth('├── a/', indent_width=4) == 1
    assert parser.parse_depth('│   └── a.txt', indent_width=4) == 2
    assert parser.parse_depth('│       └── subdir_a.txt', indent_width=4) == 3


    assert parser.parse_depth('├── a/', indent_width=2) == 2
    assert parser.parse_depth('│   └── a.txt', indent_width=2) == 4
    assert parser.parse_depth('│       └── subdir_a.txt', indent_width=2) == 6

def test_parse_type():

    parser = Parser()

    assert parser.parse_type('├── a/') == Filetype.directory
    assert parser.parse_type('│   └── a.txt') == Filetype.file
    assert parser.parse_type('│       └── subdir_a.txt') == Filetype.file
    assert parser.parse_type('             subdir_a/') == Filetype.directory

def test_parse_filename():

    parser = Parser()

    assert parser.parse_filename('dir_a/') == 'dir_a'
    assert parser.parse_filename('│       └── subdir_a.txt') == 'subdir_a.txt'

def test_parse_indent_width():

    parser = Parser()

    assert parser.parse_indent_width('dir_a/') == 0
    assert parser.parse_indent_width(' dir_a/') == 1
    assert parser.parse_indent_width('               dir_a/') == 15


def test_get_next_line():

    parser = Parser()

    parser.load(TEST_INPUT)

    data, depth = parser.get_next_line()

    assert data.filename == 'dir_a'
    assert data.filetype == Filetype.directory
    assert depth == 0

    data, depth = parser.get_next_line()
    
    assert data.filename == 'file_a.txt'
    assert data.filetype == Filetype.file
    assert depth == 1

    data, depth = parser.get_next_line()
    
    assert data.filename == 'subdir_a'
    assert data.filetype == Filetype.directory
    assert depth == 1

    data, depth = parser.get_next_line()
    
    assert data.filename == 'subdir_file_a.txt'
    assert data.filetype == Filetype.file
    assert depth == 2

