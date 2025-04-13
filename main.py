from playwright.sync_api import sync_playwright
import time
import random
import os

def random_delay(min_seconds=0.1, max_seconds=1):
    """자연스러운 사용자 행동을 시뮬레이션하기 위한 랜덤 지연"""
    time.sleep(random.uniform(min_seconds, max_seconds))

def input_tags(page, tags):
    """태그 입력 함수"""
    tag_input = page.locator("input.tag_input")
    for tag in tags:
        tag_input.fill(tag)
        tag_input.press("Enter")
        random_delay()

def upload_image(page, image_path):
    """이미지 업로드 함수"""
    # 이미지 버튼 클릭
    page.evaluate("""() => {
        const buttons = Array.from(document.querySelectorAll('button'));
        const imageButton = buttons.find(b => 
            b.getAttribute('data-name') === 'image' || 
            b.classList.contains('se-image-toolbar-button') || 
            b.textContent.includes('사진')
        );
        if (imageButton) imageButton.click();
    }""")
    random_delay()

    # 파일 입력 필드 준비
    page.wait_for_selector("input[type=file]", state="attached", timeout=5000)
    file_input = page.locator("input[type=file]")

    # 숨겨진 파일 필드 표시
    page.evaluate("""() => {
        const fileInput = document.querySelector('input[type=file]');
        if (fileInput) {
            fileInput.style.display = 'block';
            fileInput.style.opacity = '1';
            fileInput.style.visibility = 'visible';
        }
    }""")
    random_delay()

    # 파일 설정
    file_input.set_input_files(image_path)
    print("이미지 업로드 성공!")

def post_to_naver_cafe():
    with sync_playwright() as p:
        # 브라우저 설정 및 실행
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # 로그인
            page.goto("https://nid.naver.com/nidlogin.login")
            page.evaluate("""([id, pw]) => {
                document.querySelector('#id').value = id;
                document.querySelector('#pw').value = pw;
            }""", ["randme316", "wntkfkd719!"])
            random_delay()
            page.click("#log\\.login")
            
            # 보안 인증 대기
            print("보안 인증이 필요한 경우 지금 처리해주세요...")
            time.sleep(10)
            
            # 카페 이동 및 글쓰기
            page.goto("https://cafe.naver.com/successwithstock")
            random_delay()
            
            # 글쓰기 페이지 열기
            with page.expect_popup() as popup_info:
                page.click("a._rosRestrict")
            write_page = popup_info.value
            write_page.wait_for_load_state("networkidle")
            
            # 게시판 선택
            dropdown_button = write_page.locator("button.button:has-text('게시판을 선택해 주세요.')")
            dropdown_button.click()
            write_page.wait_for_selector("div.select_option")
            option = write_page.locator("div.select_option ul.option_list li:has-text('포스팅테스트')")
            option.click()
            random_delay()
            
            # 제목 입력
            title_input = write_page.locator("textarea.textarea_input")
            title_input.wait_for(state="visible", timeout=5000)
            title_input.fill("Playwright로 작성한 자동 포스팅 제목")
            random_delay()
            
            # 본문 입력
            editor_area = write_page.locator("span.se-placeholder.se-placeholder-focused")
            editor_area.wait_for(state="visible", timeout=5000)
            editor_area.click()
            write_page.keyboard.type("자동으로 입력할 본문 내용")
            random_delay()
            
            # 이미지 업로드
            upload_image(write_page, "cafe.jpg")
            
            # 태그 입력
            tags = ["태그1", "태그2", "태그3", "태그4"]
            input_tags(write_page, tags)
            
            # 등록 버튼 클릭
            register_button = write_page.get_by_role("button", name="등록", exact=True).last
            register_button.wait_for(state="visible", timeout=10000)
            register_button.click()
            
            print("포스팅이 완료되었습니다!")
            
        except Exception as e:
            print(f"오류 발생: {e}")
        finally:
            print("브라우저 종료")
            browser.close()

if __name__ == "__main__":
    post_to_naver_cafe()