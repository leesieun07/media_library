import pytest
from book_package import DetailedBookSearch


@pytest.fixture
def sample_system():
    """테스트용 기본 시스템 객체 생성"""
    return DetailedBookSearch("테스트 서점", "서울", "mock_id", "mock_secret")


def test_clean_html_with_tags(sample_system):
    """7. 정상 케이스 - HTML 태그를 정상적으로 정제하여 제거하는지 검증"""
    raw_title = "<b>데이터</b> 분석"
    assert sample_system._clean_html(raw_title) == "데이터 분석"


def test_clean_html_empty_and_none(sample_system):
    """8. 엣지 케이스 - 빈 문자열이나 None이 들어왔을 때 에러 없이 빈 문자열을 반환하는가"""
    assert sample_system._clean_html("") == ""
    assert sample_system._clean_html(None) == ""