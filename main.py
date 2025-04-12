from playwright.sync_api import sync_playwright
import time
import random

def random_delay(min_seconds=1, max_seconds=2):
    """자연스러운 사용자 행동을 시뮬레이션하기 위한 랜덤 지연"""
    time.sleep(random.uniform(min_seconds, max_seconds))

def post_to_naver_cafe():
    with sync_playwright() as p:
        # 브라우저 실행 (headless=False로 설정하여 시각적으로 확인 가능)
        browser = p.chromium.launch(headless=False)
        
        # 컨텍스트 생성 (화면 크기, 디바이스 특성 설정 가능)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        # 새 페이지 열기
        page = context.new_page()
        
        # 네이버 로그인 페이지로 이동
        page.goto("https://nid.naver.com/nidlogin.login")
        random_delay()
        
        # 로그인 정보 입력 (Playwright는 타이핑 감지를 우회할 수 있음)
        # JS 주입 방식 사용
        page.evaluate("""([id, pw]) => {
            document.querySelector('#id').value = id;
            document.querySelector('#pw').value = pw;
        }""", ["randme316", "wntkfkd719!"])
        
        random_delay()
        
        # 로그인 버튼 클릭
        page.click("#log\\.login")
        
        # 2단계 인증이나 보안 캡챠가 있을 경우 처리 필요
        # 여기서는 수동 처리를 위한 대기 시간 추가
        print("보안 인증이 필요한 경우 지금 처리해주세요...")
        time.sleep(10)  # 필요시 조정
        
        # 네이버 카페 페이지로 이동
        page.goto("https://cafe.naver.com/successwithstock")
        random_delay()
        
        # 글쓰기 버튼 클릭
        # 글쓰기 버튼 클릭 - 새 탭에서 열림
        with page.expect_popup() as popup_info:
            page.click("a._rosRestrict")
        
        # 새로 열린 탭으로 컨텍스트 전환
        write_page = popup_info.value
        random_delay()
        
        # 새 탭의 로딩 완료 대기
        write_page.wait_for_load_state("networkidle")
        
        # 디버깅용 스크린샷
        write_page.screenshot(path="write_page.png")
        
        print(f"현재 URL: {write_page.url}")

        try:
            # 제목 입력 필드 찾기
            title_input = write_page.locator("textarea.textarea_input")
            title_input.wait_for(state="visible", timeout=5000)
            title_input.fill("Playwright로 작성한 자동 포스팅 제목")
            random_delay()
            
            # XPath를 사용하여 내용 입력 영역 찾기
            content_element = write_page.locator('xpath=//*[@id="SE-80880d82-ec44-42ea-9ad6-ca26e10d302c"]/span[2]')
            
            # 요소가 보일 때까지 대기
            content_element.wait_for(state="visible", timeout=5000)
            
            # 내용 입력
            content_element.fill("Playwright로 작성한 자동 포스팅 내용입니다.\n\n오늘의 날씨는 맑습니다.")
            
            # 또는 클릭 후 타이핑 방식 사용
            content_element.click()
            write_page.keyboard.type("Playwright로 작성한 자동 포스팅 내용입니다.\n\n오늘의 날씨는 맑습니다.")
            
            random_delay()
            print("내용 입력 성공!")

        except Exception as e: 
            print(f"오류 발생: {e}")



        # page.click("a._rosRestrict")
        # random_delay()
        
        # # iframe으로 전환 (네이버 카페는 iframe 사용)
        # cafe_main_frame = page.frame("join-cafe-iframe")
        # if not cafe_main_frame:
        #     print("카페 메인 프레임을 찾을 수 없습니다.")
        #     browser.close()
        #     return
        
        # # 글 제목 입력
        # cafe_main_frame.fill("textarea.textarea_input", "Playwright로 작성한 자동 포스팅 제목")
        # # CSS 셀렉터를 더 단순화
        # # cafe_main_frame.fill("div.WritingEditor textarea", "Playwright로 작성한 자동 포스팅 제목")
        # random_delay()
        
        # 글 내용 입력 (에디터 타입에 따라 선택자가 달라질 수 있음)
        # 먼저 에디터 iframe으로 전환
        # editor_frame = cafe_main_frame.frame_locator("iframe.se2_input_wysiwyg").first
        # editor_frame.locator("body").fill("Playwright로 작성한 자동 포스팅 내용입니다.\n\n오늘의 날씨는 맑습니다.")
        # random_delay()
        
        # 게시판 선택 (필요한 경우)
        # cafe_main_frame.click("선택자")
        
        # 글 등록 버튼 클릭
        # cafe_main_frame.click("a.btn_post")
        # random_delay(3, 5)
        
        # 결과 확인
        print("포스팅이 완료되었습니다!")
        
        # 브라우저 종료
        browser.close()

if __name__ == "__main__":
    post_to_naver_cafe()