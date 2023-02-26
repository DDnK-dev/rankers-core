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

driver = wb.Chrome('C:/chromedriver_win32/chromedriver.exe')
driver.maximize_window()

# 소셜러스 사이트 경로
main_path = "https://socialerus.com"
url_path = main_path + "/Index?PageNo="

with open('handle_list.txt', 'w', encoding='utf-8') as f:
    # 페이지 번호 1~999까지
    for index in range(1, 1000):
        # 해당 url로 웹 페이지 불러옴
        url = (f"{url_path}{index}")
        driver.get(url)
        # 한계까지 스크롤 내림
        repeat_scroll(driver) 

        # 현재 페이지 채널들 링크 받아오기
        soup = bs(driver.page_source, 'lxml')
        channels = soup.select('div.ranking_info')
        # 해당 링크에 접속하여 핸들 이름 받아오기
        for channel in channels:
            link = channel.get('onclick')
            link = link.split(' ')[-1]
            link = link[1:-1]
            # 해당 링크에 접속
            driver.get(f"{main_path}{link}")
            time.sleep(1)
            soup = bs(driver.page_source, 'lxml')
            # 핸들 정보가 있는 태그
            span_tag = soup.select('div.my_info_txt>span')
            span_tag = str(span_tag)
            # @로 시작하는 문자열 받아오기
            handle_index = span_tag.find('@')
            if handle_index == -1:
                continue
            # 핸들 이름을 리스트 파일에 작성
            handle = span_tag[handle_index:].split(' ')[0]
            f.write(handle + '\n')