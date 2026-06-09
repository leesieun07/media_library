"""도서 검색 시스템의 기반이 되는 부모 클래스 모듈."""

from typing import List, Dict, Optional


class BookSearchSystem:
    """도서 검색 시스템의 부모 클래스입니다."""

    def __init__(self, system_name: str) -> None:
        """핵심 속성인 시스템 이름과 기본 도서 데이터베이스를 초기화합니다.

        Args:
            system_name (str): 검색 시스템의 이름
        """
        self.system_name: str = system_name
        # 시뮬레이션을 위한 기본 도서 데이터 (제목, 저자, 장르)
        self._book_database: List[Dict[str, str]] = [
            {"title": "Python Programming", "author": "John Doe", "genre": "Tech"},
            {"title": "Learning Python", "author": "Jane Smith", "genre": "Tech"},
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction"},
            {"title": "Sherlock Holmes", "author": "Arthur Conan Doyle", "genre": "Mystery"},
        ]

    def get_system_status(self) -> str:
        """시스템이 현재 정상 작동 중인지 상태를 반환하는 공개 메서드 1.

        Returns:
            str: 시스템 상태 메시지
        """
        return f"[{self.system_name}] 시스템이 정상 가동 중입니다. 총 {len(self._book_database)}권의 도서가 로드되었습니다."

    def search_by_title(self, title_keyword: str) -> List[Dict[str, str]]:
        """제목을 기준으로 도서를 검색하는 공개 메서드 2.

        Args:
            title_keyword (str): 검색할 도서 제목 키워드

        Returns:
            List[Dict[str, str]]: 검색된 도서 목록
        """
        if not title_keyword:
            return []
            
        results = []
        for book in self._book_database:
            if title_keyword.lower() in book["title"].lower():
                results.append(book)
        return results