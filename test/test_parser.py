from untree.parser import Parser, Filetype


TEST_INPUT = '''
dir_a/
    file_a.txt
    subdir_a/
        subdir_file_a.txt
    subdir_b/
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

def test_parse_filetype():

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
    lines = parser.parse()

    assert lines[0].absolute_depth == 0
    assert lines[1].absolute_depth == 1
    assert lines[2].absolute_depth == 1
    assert lines[3].absolute_depth == 2
    assert lines[4].absolute_depth == 1


    assert lines[0].relative_depth == None
    assert lines[1].relative_depth == 1
    assert lines[2].relative_depth == 0
    assert lines[3].relative_depth == 1
    assert lines[4].relative_depth == -1

    assert lines[0].filename == 'dir_a'
    assert lines[1].filename == 'file_a.txt'
    assert lines[2].filename == 'subdir_a'
    assert lines[3].filename == 'subdir_file_a.txt'
    assert lines[4].filename == 'subdir_b'  

    assert lines[0].filetype == Filetype.directory
    assert lines[1].filetype == Filetype.file
    assert lines[2].filetype == Filetype.directory
    assert lines[3].filetype == Filetype.file
    assert lines[4].filetype == Filetype.directory