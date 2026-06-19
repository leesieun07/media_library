import pytest
from book_package.utils import clean_keyword

def test_clean_keyword_normal():
    """기본 키워드의 양쪽 공백이 잘 제거되는지 검증"""
    assert clean_keyword("  파이썬  ") == "파이썬"

def test_clean_keyword_empty():
    """빈 문자열이나 공백만 있을 때 빈 문자열을 반환하는지 검증"""
    assert clean_keyword("") == ""
    assert clean_keyword("   ") == ""

def test_clean_keyword_no_change():
    """공백이 없는 정상적인 키워드가 그대로 유지되는지 검증"""
    assert clean_keyword("오브젝트") == "오브젝트"