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
    print(" Welcome to '우리 동네 AI 서점' (네이버 API & 장바구니 시스템) ")
    print("=" * 60)
    print(search_system.get_system_status())
    print("※ 프로그램 종료를 원하시면 '종료' 또는 'q'를 입력하세요.\n")

    while True:
        print("-" * 60)
        print(" [메뉴] 1: 네이버 실시간 검색 | 2: 내 장바구니 확인 | q: 종료 ")
        choice = input("👉 원하시는 작업의 번호를 입력하세요: ").strip()

        if choice.lower() in ["q", "종료"]:
            print("\n시스템을 종료합니다. 이용해 주셔서 감사합니다!")
            sys.exit(0)

        elif choice == "1":
            if not NAVER_CLIENT_ID or "Client_ID" in NAVER_CLIENT_ID:
                print("❌ 에러: run.py 상단에 실제 네이버 키들을 입력해야 합니다.")
                continue
            keyword = input("🌐 네이버 API로 실시간 검색할 책 키워드: ").strip()
            print("🔄 네이버 서버에서 실시간 도서 정보를 가져오는 중...")
            
            results = search_system.search_via_api(keyword)
            if not results:
                print("▶ 검색 결과가 존재하지 않습니다.")
                continue

            # 5개씩 끊어 보여주는 더보기 핸들러 호출
            _handle_search_pagination(results, search_system)

        elif choice == "2":
            _show_wishlist_status(search_system)

        else:
            print("❌ 올바른 메뉴 번호를 입력해 주세요.")


def _handle_search_pagination(results: list, system: DetailedBookSearch) -> None:
    """5개씩 도서를 끊어서 보여주고 더보기 및 책 선택을 처리하는 함수입니다."""
    start = 0
    total = len(results)

    while start < total:
        end = min(start + 5, total)
        print(f"\n✨ 도서 검색 결과 ({start + 1}~{end} / 총 {total}건):")
        
        # 5개 단위로 리스트 슬라이싱하여 출력
        for idx in range(start, end):
            book = results[idx]
            print(f" [{idx + 1}] {book['title']} (저자: {book['author']})")
        print("-" * 55)

        # 다음 데이터가 남아있다면 더보기 옵션을 안내 문구에 포함
        if end < total:
            msg = (f"👉 자세히 볼 책 번호(1~{total})를 입력하거나, "
                   f"더 보려면 'm'을 입력하세요: ")
        else:
            msg = f"👉 자세히 볼 책 번호(1~{total})를 입력하세요: "

        user_input = input(msg).strip()

        # 더보기를 원하는 경우
        if user_input.lower() == 'm' and end < total:
            start += 5
            continue

        # 책을 선택한 경우 숫자인지 검증
        if not user_input.isdigit():
            print("❌ 올바른 입력이 아닙니다. 메인 메뉴로 돌아갑니다.")
            break

        selected_idx = int(user_input) - 1
        if selected_idx < 0 or selected_idx >= total:
            print("❌ 범위를 벗어난 번호입니다. 메인 메뉴로 돌아갑니다.")
            break

        # 정상 선택 시 상세 보기로 진입 후 탈출
        _show_book_detail(results[selected_idx], system)
        break


def _show_book_detail(selected_book: dict, system: DetailedBookSearch) -> None:
    """선택된 도서의 상세 정보를 출력하고 장바구니 담기를 처리합니다."""
    print("\n" + "=" * 55)
    print(" 📖 선택하신 도서의 상세 정보 ")
    print("-" * 55)
    print(f" 📘 제목   : {selected_book['title']}")
    print(f" ✍ 저자   : {selected_book['author']}")
    print(f" 🏢 출판사 : {selected_book['publisher']}")
    print(f" 💰 할인가 : {selected_book['discount']}원")
    print(f" 📝 책 소개: {selected_book['description'][:100]}...")
    print("=" * 55)

    print(" [선택] 1: 이 책을 장바구니에 담기 | 2: 담지 않고 메인 메뉴로 이동 ")
    next_action = input("👉 원하시는 작업 번호를 입력하세요: ").strip()

    if next_action == "1":
        system.add_to_wishlist(selected_book['title'], selected_book['author'])
        print(f"🛒 '{selected_book['title']}' 도서가 장바구니에 정상적으로 담겼습니다!")
    else:
        print("🏠 메인 메뉴로 돌아갑니다.")


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