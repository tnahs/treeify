import pathlib

import pytest

from src.treeify import Treeify, TreeIndentationError, __version__


DATA = pathlib.Path(__file__).parent / "data"


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture
def output():
    with open(DATA / "output.txt", "r") as f:
        return f.read()


def test_spaced_four(output):

    with open(DATA / "spaced-four.txt", "r") as f:
        string = f.read()

    tree = Treeify(string=string)

    assert tree.output == output


def test_spaced_two(output):

    with open(DATA / "spaced-two.txt", "r") as f:
        string = f.read()

    tree = Treeify(string=string)

    assert tree.output == output


def test_tabbed(output):

    with open(DATA / "tabbed.txt", "r") as f:
        string = f.read()

    tree = Treeify(string=string)

    assert tree.output == output


def test_no_indentation():
    string = """
    root
    parent
    child
    """

    with pytest.raises(TreeIndentationError):
        Treeify(string=string)


def test_invaid_indentation_consistency():
    string = """
    root
        parent
          child
    """

    with pytest.raises(TreeIndentationError):
        Treeify(string=string)


def test_invaid_generation_gap():
    string = """
    root
        parent
                child
    """

    with pytest.raises(TreeIndentationError):
        Treeify(string=string)
