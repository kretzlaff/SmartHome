# -*- coding: utf-8 -*-

import pytest
from lights.skeleton import fib

__author__ = "Kenny Retzlaff"
__copyright__ = "Kenny Retzlaff"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
