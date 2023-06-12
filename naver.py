from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

import time
import pandas as pd

### Crawling Setup
browser = webdriver.Chrome()
browser.implicitly_wait(3)

url = 'https://booking.naver.com/review/bizes/699664'
browser.get(url)


titles = []
reviews = []

time.sleep(10)
for i in range(0,672):
    time.sleep(0.5)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    review_title = soup.find_all("div", {"class" : "contents_tit"})
    review = soup.find_all("p", {"class" : "review"})


    for i in range(len(review_title)):
        titles.append(review_title[i].get_text())
        reviews.append(review[i].get_text())

    element = browser.find_elements(By.CLASS_NAME, 'btn_nxt')[-1].click()


df = pd.DataFrame({'Title': titles, 'Text': reviews})
# clean DataFrame
df = df.replace('\n', ' ', regex=True)
# export to excel
df.to_excel('naver_yellow.xlsx')

