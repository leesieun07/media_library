from .core import BookSearchSystem


class DetailedBookSearch(BookSearchSystem):
    """네이버 API 연동 및 장바구니 기능을 확장한 상세 도서 검색 클래스"""

    def __init__(self, system_name, location,
                 client_id=None, client_secret=None):
        super().__init__(system_name)
        self.location = location
        self.client_id = client_id
        self.client_secret = client_secret
        self.wishlist = []

    def add_to_wishlist(self, title, author):
        """장바구니(위시리스트)에 도서 추가"""
        self.wishlist.append({"title": title, "author": author})

    def get_wishlist(self):
        """장바구니 목록 전체 반환"""
        return self.wishlist

    def search_via_api(self, keyword):
        """네이버 Book 검색 API를 호출하여 도서 리스트를 반환"""
        import requests

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
                return res.json().get('items', [])
        except Exception:
            pass
        return []
