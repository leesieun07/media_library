"""부모 클래스를 상속받아 기능을 확장한 자식 클래스 모듈."""

from typing import List, Dict
import requests
from .core import BookSearchSystem
from .utils import clean_keyword


class DetailedBookSearch(BookSearchSystem):
    """부모 클래스를 상속받아 네이버 API 및 장바구니 기능을 구현한 자식 클래스.

    :ivar wishlist: 사용자가 담은 도서 목록을 저장하는 리스트
    """

    def __init__(self, system_name: str, location: str,
                 client_id: str = "", client_secret: str = "") -> None:
        """super()를 활용하여 부모를 초기화하고 장바구니 리스트를 생성합니다."""
        super().__init__(system_name)
        self.location: str = location
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.wishlist: List[Dict[str, str]] = []

    def search_via_api(self, keyword: str) -> List[Dict[str, str]]:
        """네이버 도서 검색 API를 사용하여 책의 상세 정보들까지 검색한다.

        :param keyword: 검색할 도서 키워드
        :return: 검색된 도서 정보 딕셔너리들의 리스트
        """
        cleaned_keyword = clean_keyword(keyword)
        if not cleaned_keyword or not self.client_id or not self.client_secret:
            return []

        url = "https://openapi.naver.com/v1/search/book.json"
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }
        params = {"query": cleaned_keyword, "display": 50}

        try:
            response = requests.get(url, headers=headers,
                                    params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get("items", []):
                    results.append({
                        "title": item.get("title", ""),
                        "author": item.get("author", ""),
                        "publisher": item.get("publisher", "정보 없음"),
                        "discount": item.get("discount", "가격 정보 없음"),
                        "description": item.get("description", "소개 없음"),
                        "genre": "네이버 실시간 검색"
                    })
                return results
        except requests.RequestException:
            pass
        return []

    def add_to_wishlist(self, book_title: str, book_author: str) -> None:
        """선택한 도서 정보를 딕셔너리로 묶어 wishlist 리스트에 추가한다.

        :param book_title: 추가할 도서 제목
        :param book_author: 추가할 도서 저자

        >>> system = DetailedBookSearch("테스트", "서울")
        >>> system.add_to_wishlist("파이썬 기초", "김철수")
        >>> len(system.get_wishlist())
        1
        """
        book = {"title": book_title, "author": book_author}
        self.wishlist.append(book)

    def get_wishlist(self) -> List[Dict[str, str]]:
        """현재 장바구니 리스트를 그대로 반환한다.

        :return: 장바구니에 담긴 도서 리스트

        >>> system = DetailedBookSearch("테스트", "서울")
        >>> system.get_wishlist()
        []
        """
        return self.wishlist
