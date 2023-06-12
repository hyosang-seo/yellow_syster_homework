from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

import time
import pandas as pd

### Crawling Setup
browser = webdriver.Chrome()
browser.implicitly_wait(3)

url = 'https://tickets.interpark.com/goods/09000318'
browser.get(url)

# click the postinfo1
element = browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/nav/div/div/ul/li[3]/a').click()

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

# pandas dataframe setup
titles = []
reviews = []

first = 0
# get pageNumber
for ids in range(30):
    s = 0

    print(ids)
    time.sleep(1)
    try:
        next_button_element = browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/a')
        print('start')
        s = s + 1
        first = first + 1

    except:
        pass
    
    try:
        next_button_element = browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/a[2]')
        print('ing')
        s = s + 1

    except:
        pass

    page_element = browser.find_elements(By.XPATH, '/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/ol/li')
    print('first', first)
    print('s', s)

    for i in page_element:
        time.sleep(1)
        i.click()

        # while True:
        #     # Scroll down to bottom
        #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #     # Wait to load page
        #     time.sleep(0.5)

        #     # Calculate new scroll height and compare with last scroll height
        #     new_height = browser.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         break
        #     last_height = new_height



        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        review_title = soup.find_all("strong", {"class": "bbsTitleText"})
        review = soup.find_all("p", {"class": "bbsText"})

        for i in range(len(review_title)):
            titles.append(review_title[i].get_text())
            # print(review[i].get_text())
            reviews.append(review[i].get_text())
    
    if ids  != 4 :
        time.sleep(3)
        next_button_element.click()
        print("clicked")

    else:
        break

df = pd.DataFrame({'Title': titles, 'Text': reviews})
# clean DataFrame
df = df.replace('\n', ' ', regex=True)
# export to excel
df.to_excel('intepark_yellow.xlsx')

