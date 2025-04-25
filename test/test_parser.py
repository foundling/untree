from untree.parser import Parser

def test_parse_depth_ascii():


    parser = Parser()

    assert parser.parse_depth('|-- a/', indent_width=4) == 1
    assert parser.parse_depth('|   `-- a.txt', indent_width=4) == 2
    assert parser.parse_depth('|       `-- subdir_a.txt', indent_width=4) == 3


def test_parse_depth_utf8():

    parser = Parser()

    assert parser.parse_depth('├── a/', indent_width=4) == 1
    assert parser.parse_depth('│   └── a.txt', indent_width=4) == 2
    assert parser.parse_depth('│       └── subdir_a.txt', indent_width=4) == 3
