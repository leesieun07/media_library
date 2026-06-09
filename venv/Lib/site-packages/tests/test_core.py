import pytest
from book_package.core import BookSearchSystem
from book_package.utils import clean_keyword

# 1. utils 정상 케이스
def test_clean_keyword_normal():
    assert clean_keyword("  Python  ") == "python"

# 2. utils 엣지 케이스 (빈 문자열)
def test_clean_keyword_empty():
    assert clean_keyword("") == ""

# 3. core 부모 클래스 상태 확인 정상 케이스
def test_system_status():
    system = BookSearchSystem("테스트서점")
    assert "테스트서점" in system.get_system_status()

# 4. core 제목 검색 정상 케이스
def test_search_by_title_success():
    system = BookSearchSystem("테스트서점")
    results = system.search_by_title("Python")
    assert len(results) == 2
    assert results[0]["title"] == "Python Programming"

# 5. core 제목 검색 엣지 케이스 (결과 없음)
def test_search_by_title_no_result():
    system = BookSearchSystem("테스트서점")
    results = system.search_by_title("Java")
    assert len(results) == 0