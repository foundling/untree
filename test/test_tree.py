import pytest

from untree.tree import Tree


@pytest.fixture(autouse=True)
def setup_parser() -> Tree:
    return Tree()

def test_parser(tree:Tree):
    assert tree is not None