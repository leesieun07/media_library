"""도서 검색 시스템을 실행하는 대화형 CLI 프로그램 인터페이스."""

import sys
from book_package import DetailedBookSearch

# 💡 보내주신 네이버 Client ID와 Client Secret을 안전하게 심었습니다.
NAVER_CLIENT_ID = "TwAnWdbWJ3lcmzfLYMtV"
NAVER_CLIENT_SECRET = "AWJ63EXWSY"


def main() -> None:
    """사용자 입력을 받아 도서 검색 시스템을 구동하는 메인 함수."""
    search_system = DetailedBookSearch(
        system_name="우리 동네 AI 서점",
        location="서울시",
        client_id=NAVER_CLIENT_ID,
        client_secret=NAVER_CLIENT_SECRET
    )

    print("=" * 60)
    print(" Welcome to '우리 동네 AI 서점' (네이버 API 실시간 연동) ")
    print("=" * 60)
    print(search_system.get_system_status())
    print("※ 프로그램 종료를 원하시면 '종료' 또는 'q'를 입력하세요.\n")

    while True:
        print("-" * 60)
        print(" [메뉴] 1: 통합 검색 | 2: 장르별 검색 | "
              "3: 네이버 실시간 검색 | q: 종료 ")
        choice = input("👉 원하시는 작업의 번호를 입력하세요: ").strip()

        if choice.lower() in ["q", "종료"]:
            print("\n시스템을 종료합니다. 이용해 주셔서 감사합니다!")
            sys.exit(0)

        if choice == "1":
            keyword = input("🔍 검색할 제목 또는 저자를 입력하세요: ").strip()
            results = search_system.advanced_search(keyword)
            _print_results(results)

        elif choice == "2":
            msg = "📂 검색할 장르를 입력하세요 (Tech/Fiction/Mystery 등): "
            genre = input(msg).strip()
            results = search_system.search_by_genre(genre)
            _print_results(results)

        elif choice == "3":
            if not NAVER_CLIENT_ID or "Client_ID" in NAVER_CLIENT_ID:
                print("❌ 에러: run.py 상단에 실제 네이버 키들을 입력해야 합니다.")
                continue
            keyword = input("🌐 네이버 API로 실시간 검색할 책 키워드: ").strip()
            print("🔄 네이버 서버에서 실시간 도서 정보를 가져오는 중...")
            results = search_system.search_via_api(keyword)
            _print_results(results)

        else:
            print("❌ 올바른 메뉴 번호를 입력해 주세요.")


def _print_results(results: list) -> None:
    """검색 결과를 예쁘게 포맷팅하여 출력하는 헬퍼 함수."""
    if not results:
        print("▶ 검색 결과가 존재하지 않습니다.")
        return

    print(f"\n✨ 총 {len(results)}건의 검색 결과가 있습니다:")
    for idx, book in enumerate(results, 1):
        print(f" [{idx}] 제목: {book['title']} | "
              f"저자: {book['author']} | 장르: {book['genre']}")
    print()


if __name__ == "__main__":
    main()