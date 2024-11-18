import pytest
from cal import add

def test_add():
    assert add(2,3) == 5
    assert add(23,3) == 26
