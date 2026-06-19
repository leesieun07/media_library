import requests

from book_package.core import BookSearchSystem


class DetailedBookSearch(BookSearchSystem):
    """네이버 API 연동 및 장바구니 기능을 확장한 상세 도서 검색 클래스"""

    def __init__(
        self, system_name, location, client_id=None, client_secret=None
    ):
        super().__init__(system_name)
        self.location = location
        self.client_id = client_id
        self.client_secret = client_secret
        self.wishlist = []

    def add_to_wishlist(self, title, author):
        """장바구니(위시리스트)에 도서 정보를 추가합니다.

        :param title: 추가할 도서의 제목
        :param author: 추가할 도서의 저자
        :return: 없음
        """
        self.wishlist.append({"title": title, "author": author})

    def get_wishlist(self):
        """현재 장바구니에 담긴 모든 도서 목록을 반환합니다.

        :return: 담긴 도서 정보(dict)들이 저장된 리스트
        """
        return self.wishlist

    def _clean_html(self, text):
        """네이버 API 결과의 HTML 태그(<b> 등)를 제거하는 비공개 메서드

        >>> system = DetailedBookSearch("서점", "서울")
        >>> system._clean_html("<b>파이썬</b> 프로그래밍")
        '파이썬 프로그래밍'
        """
        if not text:
            return ""
        return text.replace("<b>", "").replace("</b>", "")

    def search_via_api(self, keyword):
        """네이버 Book 검색 API를 호출하여 도서 리스트를 반환합니다.

        :param keyword: 검색할 도서의 키워드
        :return: 검색 결과 도서 정보 리스트
        """
        url = (
            f"https://openapi.naver.com/v1/search/book.json"
            f"?query={keyword}&display=50"
        )
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }

        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                raw_items = res.json().get('items', [])
                for item in raw_items:
                    item['title'] = self._clean_html(item.get('title', ''))
                return raw_items
        except Exception:
            pass
        return []
