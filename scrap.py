from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import pdb
import pymongo

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


# 크롬 드라이버 불러오기
driver = wb.Chrome('C:/chromedriver_win32/chromedriver.exe')
driver.maximize_window()

# handle 리스트 불러오기
with open('handle_list.txt', 'r', encoding='utf-8') as f:
     lines = f.readlines()

for line in lines:
    line = line[:-1]
    # handle로 유튜브 채널 정보 url 생성
    url = (f'https://www.youtube.com/{line}/about')
    # 해당 url로 웹 페이지 불러옴
    driver.get(url)
    time.sleep(1)
    # bs4로 해당 웹 페이지 정보 parsing
    soup = bs(driver.page_source, 'lxml')
    # 채널 이름 받아오기
    channel_name = soup.select_one('yt-formatted-string#text.style-scope.ytd-channel-name').get_text()
    
    # 구독자 수 받아오기
    subscribes = soup.select('yt-formatted-string#subscriber-count')
    subscribes = subscribes[0].get('aria-label').split(' ')[1]

    # 동영상 조회수 받아오기
    views = soup.select('yt-formatted-string.style-scope.ytd-channel-about-metadata-renderer')
    views_string = str(views)
    front_index = views_string.find('조회수')
    back_index = views_string.find('회<')
    views = views_string[front_index + 4:back_index]
    views = int(views.replace(',',''))
    
    # 해당 채널의 동영상 파트로 이동
    url = (f'https://www.youtube.com/{line}/videos')
    driver.get(url)
    # 한계까지 스크롤 내리기
    repeat_scroll(driver)

    # 비디오 개수 받아오기
    soup = bs(driver.page_source, 'lxml')
    videos = soup.select('a#video-title-link')
    video_num = len(videos)

    # with open(channel_name + '.txt', 'w', encoding='utf-8') as txt_f:
    #     for i in videos:
    #         txt_f.write(i.text.strip() + '\n')
    #         if i.get('aria-label'):
    #             txt_f.write(i.get('aria-label').split()[-1] + '\n')

    # 몽고디비 연결
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['ranker']
    collection = db['Channel_info']
    # 데이터 생성 후, db에 삽입
    data = {"name": channel_name, "handle": line, "subscribes": subscribes, "views": views, "video_num": video_num}
    collection.insert_one(data)