import pytest

from untree.parser import Parser


@pytest.fixture(autouse=True)
def setup_parser() -> Parser:
    return Parser()

def test_parse_depth(parser:Parser):
    assert parser is not None