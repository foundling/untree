import pytest

from untree.parser import Parser


@pytest.fixture
def parser() -> Parser:

    with open('./test/test_data/schema_ascii.txt', 'r') as f:
        p = Parser()
        p.load(f.read())
    
        return p

def test_parse_depth(parser:Parser):

    assert False is True

