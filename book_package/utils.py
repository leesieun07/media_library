"""도서 검색에 필요한 도우미 함수 모음."""


def clean_keyword(keyword: str) -> str:
    """입력된 검색어의 공백을 제거하고 소문자로 변환하여 정제합니다.

    Args:
        keyword (str): 사용자가 입력한 검색어

    Returns:
        str: 정제된 검색어
    """
    if not keyword:
        return ""
    return keyword.strip().lower()