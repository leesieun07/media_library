import pytest
from book_package.subclass import DetailedBookSearch

# 6. subclass 장르 검색 정상 케이스
def test_search_by_genre_success():
    searcher = DetailedBookSearch("강남점", "서울")
    results = searcher.search_by_genre("Tech")
    assert len(results) == 2

# 7. subclass 고급 검색 정상 케이스 (저자명 검색)
def test_advanced_search_by_author():
    searcher = DetailedBookSearch("강남점", "서울")
    results = searcher.advanced_search("Fitzgerald")
    assert len(results) == 1
    assert results[0]["title"] == "The Great Gatsby"

# 8. subclass 고급 검색 엣지 케이스 (빈 값 입력)
def test_advanced_search_empty_keyword():
    searcher = DetailedBookSearch("강남점", "서울")
    results = searcher.advanced_search("")
    assert len(results) == 0

# 9. subclass 비공개 메서드 간접 테스트 (대소문자 구분 없음 확인)
def test_subclass_case_insensitivity():
    searcher = DetailedBookSearch("강남점", "서울")
    results = searcher.advanced_search("gAtSbY")
    assert len(results) == 1