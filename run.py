import sys
from book_package import DetailedBookSearch


def main():
    # 1. 시스템 초기화 및 환영 메시지
    search_system = DetailedBookSearch(
        system_name="우리 동네 AI 서점", location="서울시 강남구"
    )

    print("=" * 60)
    print(f" Welcome to '{search_system.system_name}' ")
    print("=" * 60)
    print(search_system.get_system_status())
    print("※ 프로그램 종료를 원하시면 '종료' 또는 'q'를 입력하세요.\n")

    while True:
        print("-" * 60)
        print(" [메뉴 선택] 1: 통합 검색 (제목/저자) | 2: 장르별 검색 | q: 종료 ")
        menu = input("👉 원하시는 작업의 번호를 입력하세요: ").strip()

        # 종료 조건 처리
        if menu.lower() in ["q", "종료", "quit", "exit"]:
            print("\n👋 프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            sys.exit(0)

        # 1번 메뉴: 통합 검색
        if menu == "1":
            keyword = input("🔍 검색할 책 제목이나 저자를 입력하세요: ")

            # 공백 입력 예외 처리 (엣지 케이스 대응)
            if not keyword.strip():
                print("⚠️ 검색어를 한 글자 이상 입력해 주세요.")
                continue

            # 패키지 내부의 고급 검색 로직 실행
            results = search_system.advanced_search(keyword)

            print(f"\n📚 '{keyword.strip()}' 검색 결과 (총 {len(results)}건):")
            if not results:
                print("   ❌ 일치하는 도서가 없습니다.")
            else:
                for idx, book in enumerate(results, 1):
                    print(
                        f"  [{idx}] {book['title']} - {book['author']} (장르: {book['genre']})"
                    )

        # 2번 메뉴: 장르 필터링
        elif menu == "2":
            print("💡 [선택 가능한 장르] Tech, Fiction, Mystery")
            genre = input("🔍 필터링할 장르를 입력하세요: ")

            if not genre.strip():
                print("⚠️ 장르를 입력해 주세요.")
                continue

            results = search_system.search_by_genre(genre)

            print(f"\n📚 '{genre.strip()}' 장르 검색 결과 (총 {len(results)}건):")
            if not results:
                print("   ❌ 해당 장르에 등록된 도서가 없습니다.")
            else:
                for idx, book in enumerate(results, 1):
                    print(
                        f"  [{idx}] {book['title']} - {book['author']}"
                    )

        # 잘못된 메뉴 입력 처리
        else:
            print("⚠️ 올바른 메뉴 번호(1, 2)를 선택하거나 'q'를 입력해 주세요.")


if __name__ == "__main__":
    main()