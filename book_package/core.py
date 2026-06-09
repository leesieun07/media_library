"""도서 검색 시스템의 기반이 되는 부모 클래스 모듈."""

from typing import List, Dict


class BookSearchSystem:
    """도서 검색 시스템의 부모 클래스입니다.

    :ivar system_name: 검색 시스템의 이름
    :ivar _book_database: 시스템 내부 도서 데이터베이스
    """

    def __init__(self, system_name: str) -> None:
        """핵심 속성인 시스템 이름과 기본 도서 데이터베이스를 초기화합니다.

        :param system_name: 검색 시스템의 이름
        """
        self.system_name: str = system_name
        self._book_database: List[Dict[str, str]] = [
            {"title": "Python Programming", "author": "John Doe", "genre": "Tech"},
            {"title": "Learning Python", "author": "Jane Smith", "genre": "Tech"},
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction"},
            {"title": "Sherlock Holmes", "author": "Arthur Conan Doyle", "genre": "Mystery"},
        ]

    def get_system_status(self) -> str:
        """시스템이 현재 정상 작동 중인지 상태를 반환합니다.

        >>> system = BookSearchSystem("테스트서점")
        >>> "테스트서점" in system.get_system_status()
        True

        :return: 시스템 상태 메시지
        """
        return f"[{self.system_name}] 시스템이 정상 가동 중입니다. 총 {len(self._book_database)}권의 도서가 로드되었습니다."

    def search_by_title(self, title_keyword: str) -> List[Dict[str, str]]:
        """제목을 기준으로 도서를 검색합니다.

        >>> system = BookSearchSystem("테스트서점")
        >>> len(system.search_by_title("Python"))
        2
        >>> system.search_by_title("Java")
        []

        :param title_keyword: 검색할 도서 제목 키워드
        :return: 검색된 도서 목록
        """
        if not title_keyword:
            return []
            
        results = []
        for book in self._book_database:
            if title_keyword.lower() in book["title"].lower():
                results.append(book)
        return results