import pytest
from book_package import DetailedBookSearch


@pytest.fixture
def sample_system():
    """테스트용 기본 시스템 객체 생성"""
    return DetailedBookSearch("테스트 서점", "서울", "mock_id", "mock_secret")


def test_add_to_wishlist(sample_system):
    """3. 정상 케이스 - 장바구니에 도서가 정상적으로 추가되는지 검증"""
    sample_system.add_to_wishlist("파이썬 기초", "김철수")
    assert len(sample_system.wishlist) == 1
    assert sample_system.wishlist[0]["title"] == "파이썬 기초"


def test_get_wishlist_multiple(sample_system):
    """4. 정상 케이스 - 장바구니에 여러 권이 있을 때 목록을 잘 반환하는지 검증"""
    sample_system.add_to_wishlist("책A", "저자A")
    sample_system.add_to_wishlist("책B", "저자B")
    cart = sample_system.get_wishlist()
    assert len(cart) == 2
    assert cart[1]["title"] == "책B"


def test_get_wishlist_initially_empty(sample_system):
    """5. 엣지 케이스 - 시스템이 처음 켜졌을 때 장바구니가 비어있는가"""
    assert sample_system.get_wishlist() == []


def test_search_via_api_invalid_token(sample_system):
    """6. 엣지 케이스 - 잘못된 토큰 환경에서 API 호출 시 터지지 않고 빈 리스트를 주는가"""
    result = sample_system.search_via_api("파이썬")
    assert result == []