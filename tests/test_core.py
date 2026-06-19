import pytest
from book_package import DetailedBookSearch


@pytest.fixture
def sample_system():
    """테스트용 기본 시스템 객체 생성"""
    return DetailedBookSearch("테스트 서점", "서울", "mock_id", "mock_secret")


def test_initialization(sample_system):
    """1. 정상 케이스 - 객체가 정상적으로 속성들을 가지고 초기화되는지 검증"""
    assert sample_system.system_name == "테스트 서점"
    assert sample_system.location == "서울"


def test_credentials(sample_system):
    """2. 정상 케이스 - 클라이언트 ID와 Secret이 잘 설정되었는지 검증"""
    assert sample_system.client_id == "mock_id"
    assert sample_system.client_secret == "mock_secret"