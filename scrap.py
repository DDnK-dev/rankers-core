from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import pdb

def repeat_scroll(driver):
    #스크롤 내리기 전 위치
    scroll_location = driver.execute_script("return document.documentElement.scrollHeight")
    
    while True:
        #현재 스크롤의 가장 아래로 내림
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")

        #전체 스크롤이 늘어날 때까지 대기
        time.sleep(2)

        #늘어난 스크롤 높이
        scroll_height = driver.execute_script("return document.documentElement.scrollHeight")

        #늘어난 스크롤 위치와 이동 전 위치 같으면(더 이상 스크롤이 늘어나지 않으면) 종료
        if scroll_location == scroll_height:
            break

        #같지 않으면 스크롤 위치 값을 수정하여 같아질 때까지 반복
        else:
            #스크롤 위치값을 수정
            scroll_location = driver.execute_script("return document.documentElement.scrollHeight")

# 크롬 드라이버 경로
driver = wb.Chrome('C:/chromedriver_win32/chromedriver.exe')
driver.maximize_window()
# 스크랩할 url 경로
url = ('https://www.youtube.com/@BLACKPINK/videos')
driver.get(url)

# 스크롤 끝에 도달할 때까지 무한 반복
repeat_scroll(driver) 

# body = driver.find_element(by=By.TAG_NAME, value='body')
# body.send_keys(Keys.PAGE_DOWN)

# for i in range(50):
#     body.send_keys(Keys.PAGE_DOWN)
#     time.sleep(0.5)

# with open('webpage_data.txt', 'w', encoding='utf-8') as f:
#     f.write(driver.page_source)

soup = bs(driver.page_source, 'lxml')
video = soup.select('a#video-title-link')
subscribes = soup.select('yt-formatted-string#subscriber-count')

# 영상 제목, 조회수 전체 조회
for i in video:
    print(i.text.strip())
    if i.get('aria-label'):
	    print(i.get('aria-label').split()[-1])
# 구독자 수 출력        
for s in subscribes:
    print(s.get('aria-label'))