"""부모 클래스를 상속받아 기능을 확장한 자식 클래스 모듈."""

from typing import List, Dict
import requests
from .core import BookSearchSystem
from .utils import clean_keyword


class DetailedBookSearch(BookSearchSystem):
    """부모 클래스를 상속받아 네이버 API 및 장바구니 기능을 구현한 자식 클래스."""

    def __init__(self, system_name: str, location: str,
                 client_id: str = "", client_secret: str = "") -> None:
        """super()를 활용하여 부모를 초기화하고 장바구니 리스트를 생성합니다."""
        super().__init__(system_name)
        self.location: str = location
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        # 프로그램이 실행되는 동안 메모리에만 유지되는 순수 파이썬 리스트 장바구니
        self.wishlist: List[Dict[str, str]] = []

    def search_via_api(self, keyword: str) -> List[Dict[str, str]]:
        """네이버 도서 검색 API를 사용하여 책의 상세 정보들까지 검색합니다."""
        cleaned_keyword = clean_keyword(keyword)
        if not cleaned_keyword or not self.client_id or not self.client_secret:
            return []

        url = "https://openapi.naver.com/v1/search/book.json"
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }
        params = {"query": cleaned_keyword, "display": 5}

        try:
            response = requests.get(url, headers=headers,
                                    params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get("items", []):
                    # 자세한 정보 조회를 위해 출판사, 가격, 요약 필드를 추가로 저장합니다.
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
        """선택한 도서 정보를 딕셔너리로 묶어 wishlist 리스트에 추가합니다."""
        book = {"title": book_title, "author": book_author}
        self.wishlist.append(book)

    def get_wishlist(self) -> List[Dict[str, str]]:
        """현재 장바구니 리스트를 그대로 반환합니다."""
        return self.wishlist

    def search_by_genre(self, genre: str) -> List[Dict[str, str]]:
        """지정된 장르의 도서만 필터링하여 반환합니다."""
        cleaned_genre = clean_keyword(genre)
        results = []
        for book in self._book_database:
            if cleaned_genre in book["genre"].lower():
                results.append(book)
        return results

    def advanced_search(self, keyword: str) -> List[Dict[str, str]]:
        """제목이나 저자 어디든 매칭되면 찾아주는 고급 검색을 수행합니다."""
        cleaned_keyword = clean_keyword(keyword)
        if not cleaned_keyword:
            return []

        results = []
        for book in self._book_database:
            if self._is_match(book, cleaned_keyword):
                results.append(book)
        return results

    def _is_match(self, book: Dict[str, str], keyword: str) -> bool:
        """도서 데이터가 검색어와 일치하는지 판별하는 비공개 메서드입니다."""
        return ((keyword in book["title"].lower()) or
                (keyword in book["author"].lower()))
