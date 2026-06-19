"""도서 검색 시스템을 실행하는 대화형 CLI 프로그램 인터페이스."""

import sys
from book_package import DetailedBookSearch

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
    print(" Welcome to '우리 동네 AI 서점' (파이썬 기본기 장바구니 버전) ")
    print("=" * 60)
    print(search_system.get_system_status())
    print("※ 프로그램 종료를 원하시면 '종료' 또는 'q'를 입력하세요.\n")

    while True:
        print("-" * 60)
        print(" [메뉴] 1:통합검색 | 2:장르검색 | "
              "3:네이버검색 | 4:장바구니확인 | q:종료 ")
        choice = input("👉 원하시는 작업의 번호를 입력하세요: ").strip()

        if choice.lower() in ["q", "종료"]:
            print("\n시스템을 종료합니다. 이용해 주셔서 감사합니다!")
            sys.exit(0)

        elif choice == "1":
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
            if not results:
                print("▶ 검색 결과가 존재하지 않습니다.")
                continue

            _print_results(results)
            _handle_book_selection(results, search_system)

        elif choice == "4":
            _show_wishlist_status(search_system)

        else:
            print("❌ 올바른 메뉴 번호를 입력해 주세요.")


def _print_results(results: list) -> None:
    """검색 결과를 예쁘게 포맷팅하여 출력하는 헬퍼 함수."""
    print(f"\n✨ 총 {len(results)}건의 도서가 검색되었습니다:")
    for idx, book in enumerate(results, 1):
        print(f" [{idx}] {book['title']} (저자: {book['author']})")
    print()


def _handle_book_selection(results: list, system: DetailedBookSearch) -> None:
    """도서 목록 중 하나를 선택하여 상세 정보를 보고 장바구니에 담는 흐름을 제어합니다."""
    select_msg = f"👉 자세히 보고 싶은 책의 번호(1~{len(results)})를 입력하세요: "
    idx_input = input(select_msg).strip()
    
    if not idx_input.isdigit():
        print("❌ 숫자로만 입력해 주세요. 메뉴로 돌아갑니다.")
        return

    selected_idx = int(idx_input) - 1
    if selected_idx < 0 or selected_idx >= len(results):
        print("❌ 범위를 벗어난 번호입니다. 메뉴로 돌아갑니다.")
        return

    selected_book = results[selected_idx]
    
    print("\n" + "=" * 55)
    print(" 📖 선택하신 도서의 상세 정보 ")
    print("-" * 55)
    print(f" 📘 제목   : {selected_book['title']}")
    print(f" ✍ 저자   : {selected_book['author']}")
    print(f" 🏢 출판사 : {selected_book['publisher']}")
    print(f" 💰 할인가 : {selected_book['discount']}원")
    print(f" 📝 책 소개: {selected_book['description'][:100]}...")  # 100자만 자르기
    print("=" * 55)

    print(" [선택] 1: 이 책을 장바구니에 담기 | 2: 담지 않고 메인 메뉴로 이동 ")
    next_action = input("👉 원하시는 작업 번호를 입력하세요: ").strip()

    if next_action == "1":
        system.add_to_wishlist(selected_book['title'], selected_book['author'])
        print(f"🛒 '{selected_book['title']}' 도서가 장바구니에 정상적으로 담겼습니다!")
    elif next_action == "2":
        print("🏠 장바구니에 담지 않고 메인 메뉴로 돌아갑니다.")
    else:
        print("❌ 잘못된 입력입니다. 메인 메뉴로 돌아갑니다.")


def _show_wishlist_status(system: DetailedBookSearch) -> None:
    """현재 장바구니 리스트의 보관 현황을 보여줍니다."""
    print("\n📋 [내 장바구니 리스트 현황]")
    wish_list = system.get_wishlist()
    if not wish_list:
        print("▶ 현재 장바구니가 비어 있습니다.")
        return

    for idx, item in enumerate(wish_list, 1):
        print(f"  [{idx}] 제목: {item['title']} | 저자: {item['author']}")
    print(f"✨ 총 {len(wish_list)}권의 도서가 보관 중입니다.")


if __name__ == "__main__":
    main()