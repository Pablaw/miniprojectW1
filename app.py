#import requests 크롤링 라이브러리 (정적)requests
# html 예쁘게 긁어오기 bs4
from bs4 import BeautifulSoup
# 동적페에지 크롤링 selenium
from selenium import webdriver

#flask 임포트
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('crawling.html')

@app.route('/crawling', methods=["POST"])
def web_crawling_youtube():
    #### 1. 사용자 키워드 및 크롤링 대상 url 세팅 ####
    keyword = '건강'
    target_url = 'https://www.youtube.com/results?search_query=' + keyword

    #### 2. 동적페이지 크롤링 ####
    # 옵션 생성
    options = webdriver.ChromeOptions()

    options.add_argument("headless") # 창 숨기는 옵션 추가(백그라운드로 실행, 이걸 하지 않으면 브라우저 열어서 탐색하게 됨)
    options.add_argument("--disable-popup-blocking") #광고팝업안띄움
    options.add_argument("--blink-settings=imagesEnabled=false") #이미지 다운 안받음
    options.add_argument("--disable-gpu");  #gpu 비활성화(GUI 없는 OS를 위해..)

    # driver 실행
    driver = webdriver.Chrome(options=options)
    driver.get(target_url)

    #html 가져오기
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # driver 종료
    driver.quit()

    #### 3. 링크주소 추출 및 json 배열화 ####
    youtube_links = []
    if soup != None:
        i = 0
        j = 0
        for i in  range(0, 3, 1):
            j += 1
            crawling_link = soup.select_one('#contents > ytd-video-renderer:nth-child('+str(j)+') > #dismissible > ytd-thumbnail > #thumbnail')['href'].strip()
            crawling_link = crawling_link.replace('/watch?v=', '') #링크 식별값만 추출
            youtube_links.append({i:crawling_link}) #append : 배열 뒤로 추가
    print(youtube_links)
    return None
    #return jsonify({'ytb_links':youtube_links})

web_crawling_youtube()

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

#<iframe width="560" height="315" src="https://www.youtube.com/embed/M3KWNLf3Mm0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
