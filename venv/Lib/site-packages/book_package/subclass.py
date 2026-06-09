"""부모 클래스를 상속받아 기능을 확장한 자식 클래스 모듈."""

from typing import List, Dict
from .core import BookSearchSystem
from .utils import clean_keyword


class DetailedBookSearch(BookSearchSystem):
    """부모 클래스를 상속받아 장르별 필터링 및 비공개 메서드를 구현한 자식 클래스.

    :ivar location: 서점 또는 라이브러리 위치
    """

    def __init__(self, system_name: str, location: str) -> None:
        """super()를 활용하여 부모의 속성을 초기화하고 자식만의 속성을 추가합니다.

        :param system_name: 검색 시스템 이름
        :param location: 서점 또는 라이브러리 위치
        """
        super().__init__(system_name)
        self.location: str = location

    def search_by_genre(self, genre: str) -> List[Dict[str, str]]:
        """지정된 장르의 도서만 필터링하여 반환합니다.

        >>> searcher = DetailedBookSearch("강남점", "서울")
        >>> len(searcher.search_by_genre("Tech"))
        2

        :param genre: 검색할 장르 (예: Tech, Fiction 등)
        :return: 장르에 매칭된 도서 목록
        """
        cleaned_genre = clean_keyword(genre)
        results = []
        for book in self._book_database:
            if cleaned_genre in book["genre"].lower():
                results.append(book)
        return results

    def advanced_search(self, keyword: str) -> List[Dict[str, str]]:
        """제목이나 저자 어디든 매칭되면 찾아주는 고급 검색을 수행합니다.

        >>> searcher = DetailedBookSearch("강남점", "서울")
        >>> len(searcher.advanced_search("Fitzgerald"))
        1

        :param keyword: 검색 키워드
        :return: 검색 결과 목록
        """
        cleaned_keyword = clean_keyword(keyword)
        if not cleaned_keyword:
            return []

        results = []
        for book in self._book_database:
            if self._is_match(book, cleaned_keyword):
                results.append(book)
        return results

    def _is_match(self, book: Dict[str, str], keyword: str) -> bool:
        """도서 데이터가 검색어와 일치하는지 판별하는 비공개 메서드입니다.

        :param book: 도서 단건 데이터
        :param keyword: 정제된 검색어
        :return: 일치 여부
        """
        return ((keyword in book["title"].lower()) or
                (keyword in book["author"].lower()))
