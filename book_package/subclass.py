import requests
from book_package.core import BookSearchSystem


class DetailedBookSearch(BookSearchSystem):
    """네이버 API 검색이랑 장바구니 기능 추가한 클래스"""

    def __init__(
        self, system_name, location, client_id=None, client_secret=None
    ):
        super().__init__(system_name)
        self.location = location
        self.client_id = client_id
        self.client_secret = client_secret
        self.wishlist = []

    def add_to_wishlist(self, title, author):
        """위시리스트에 책 추가

        :param title: 책 제목
        :param author: 저자 이름
        """
        self.wishlist.append({"title": title, "author": author})

    def get_wishlist(self):
        """담긴 위시리스트 리스트 반환

        :return: 장바구니 리스트
        """
        return self.wishlist

    def _clean_html(self, text):
        """네이버 API 결과에서 b 태그 지워주는 함수

        >>> system = DetailedBookSearch("서점", "서울")
        >>> system._clean_html("<b>파이썬</b> 과제")
        '파이썬 과제'
        """
        if not text:
            return ""
        return text.replace("<b>", "").replace("</b>", "")

    def search_via_api(self, keyword):
        """네이버 책 검색 API 호출

        :param keyword: 검색어
        :return: 검색된 결과 dictionary 리스트
        """
        url = (
            f"https://openapi.naver.com/v1/search/book.json"
            f"?query={keyword}&display=50"
        )
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }

        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            raw_items = res.json().get('items', [])
            for item in raw_items:
                item['title'] = self._clean_html(item.get('title', ''))
            return raw_items
        return []
