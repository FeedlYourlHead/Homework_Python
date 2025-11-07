import pytest
from task import is_palindrome, word_counts


def test_is_palindrome():
    assert is_palindrome("заказ") == True
    assert is_palindrome(123321) == True
    assert is_palindrome('Привет мир') == False


def test_word_counts():
    assert word_counts("Привет мир! Привет всем в этом прекрасном мире.") == {'привет': 2, 'мир': 1, 'всем': 1, 'в': 1, 'этом': 1, 'прекрасном': 1, 'мире': 1}
    assert word_counts('Hello, World!') == {'hello': 1, 'world': 1}
    assert word_counts('') == {}

