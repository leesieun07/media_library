from book_package import DetailedBookSearch

def main():
    CLIENT_ID = "TwAnWdbWJ3lcmzfLYMtV"          
    CLIENT_SECRET = "AWJ63EXWSY"  
    
    system = DetailedBookSearch(
        system_name="우리 동네 AI 서점",
        location="서울시",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )

    print(f"=== [{system.system_name}] 시스템 가동 ===")

    while True:
        # [1단계: 메인 메뉴 화면]
        print("\n================================================")
        print(" 1. 도서 검색하기 | 2. 장바구니 보기 | 3. 프로그램 종료")
        print("================================================")
        main_choice = input(" 원하시는 작업 번호를 선택하세요: ").strip()

        # 3번: 종료하기
        if main_choice == '3':
            print("프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break

        # 2번: 장바구니 보기
        elif main_choice == '2':
            current_wishlist = system.get_wishlist()
            if not current_wishlist:
                print("\n 장바구니가 비어 있습니다. 마음에 드는 책을 담아보세요!")
            else:
                print("\n 현재 장바구니 목록:")
                for idx, item in enumerate(current_wishlist, 1):
                    print(f"  {idx}. {item['title']} ({item['author']})")
            continue

        # 1번: 도서 검색하기
        elif main_choice == '1':
            while True:
                # [2단계: 키워드 입력 화면]
                print("\n------------------------------------------------")
                keyword = input(" 검색할 도서 키워드를 입력하세요 (메인 메뉴로 가려면 'b' 입력): ").strip()
                
                if keyword.lower() == 'b':
                    break # 내부 루프를 빠져나가서 다시 [1단계 메인 메뉴]로 이동
                if not keyword:
                    print(" 키워드가 비어 있습니다. 다시 입력해 주세요.")
                    continue

                print(f"\n '{keyword}' 검색 결과를 네이버 API에서 가져오는 중...")
                books = system.search_via_api(keyword)

                if not books:
                    print(" 검색 결과가 없습니다. 다른 키워드를 입력해 보세요.")
                    continue

                total_books = len(books)
                start_index = 0
                back_to_keyword = False  # '키워드 다시 입력하기'

                # [3단계: 5개씩 끊어보는 결과 출력 화면]
                while start_index < total_books:
                    end_index = min(start_index + 5, total_books)
                    print(f"\n--- 검색 결과 ({start_index + 1} ~ {end_index} / 총 {total_books}건) ---")
                    
                    for i in range(start_index, end_index):
                        print(f"[{i + 1}] {books[i]['title']} - {books[i]['author']}")

                    print("------------------------------------------------")
                    print(" 선택: [번호 입력] 자세히 보기 | [m] 더 보기")
                    print("       [r] 키워드 다시 입력하기 | [q] 메인 메뉴로 이동")
                    print("------------------------------------------------")
                    
                    user_input = input(" 원하시는 선택지를 입력하세요: ").strip().lower()

                    if user_input == 'q':
                        break # 5개 루프 탈출해서 메인 메뉴로 복귀
                    
                    elif user_input == 'r':
                        print("\n 현재 결과를 닫고 키워드 입력창으로 돌아갑니다.")
                        back_to_keyword = True
                        break # 5개 루프 탈출해서 바로 위 [2단계 키워드 입력]으로 복귀
                        
                    elif user_input == 'm':
                        if end_index >= total_books:
                            print("\n 마지막 페이지입니다. 더 이상 볼 도서가 없습니다.")
                        else:
                            start_index += 5
                        continue

                    elif user_input.isdigit():
                        choice = int(user_input)
                        if start_index < choice <= end_index:
                            selected_book = books[choice - 1]
                            
                            # 상세 정보 화면 출력
                            print("\n================================================")
                            print(f" [상세 정보] {selected_book['title']}")
                            print(f" 저자: {selected_book['author']} | 🏢 출판사: {selected_book['publisher']}")
                            print(f" 할인가: {selected_book['discount']}원")
                            print(f" 요약: {selected_book['description']}")
                            print("================================================")
                            
                            wish_choice = input("🛒 이 책을 장바구니에 담으시겠습니까? (y/n): ").strip().lower()
                            if wish_choice == 'y':
                                system.add_to_wishlist(selected_book['title'], selected_book['author'])
                                print(" 장바구니에 성공적으로 담겼습니다!")
                        else:
                            print(f" 현재 화면에 보이는 번호({start_index + 1} ~ {end_index}) 중에서 선택해 주세요.")
                    else:
                        print(" 올바른 번호나 명령어를 입력해 주세요.")
                
                # 만약 사용자가 'r'을 누른 게 아니라 'q'를 누르거나 목록이 끝나서 나온 거라면 끝내기
                if not back_to_keyword:
                    break
        else:
            print(" 잘못된 선택입니다. 1, 2, 3 중에서 번호를 선택해 주세요.")

if __name__ == "__main__":
    main()
