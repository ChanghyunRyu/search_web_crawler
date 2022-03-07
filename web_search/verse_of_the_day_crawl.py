import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re

base_url = 'https://qt.swim.org/user_utf/life/user_print_web.php?edit_all='
driver = webdriver.Chrome()
driver.get(base_url + '2022-03-07')

html = driver.page_source
bs = BeautifulSoup(html, 'html.parser')
driver.close()

# 본문 추출, id 존재하는 부분이 이것밖에 없음.
document = bs.find('div', {'class': 'box3'})
title = document.parent.find('strong')
document = document.text
title = title.text
# 텍스트 가공
# document: 처음 3번 띄어쓰기 제거, 각 문장 앞 성경 구절 번호 제거
# title: 변동 사항 없음
texts = document.split('\n')
document = ''
for text in texts:
    if text == '':
        continue
    else:
        text = re.sub('[0-9]*', '', text, count=1)
        document += text

# id 등의 별도 구별할 것이 존재하지 않기에 원시적인 형태로 추출하기 위한 번호 확인
# contents = bs.find('table').findAll('tr')
# for i in range(len(contents)):
#     print("-------------------------------------------------{}-------------------------------------------------".format(i))
#     print(contents[i])

summary = bs.find('table').findAll('tr')[11]
summary = summary.find('td').find('p').text
# 텍스트 가공: '[오늘의 말씀 요약]' 제거
summary = re.sub('\[오늘의 말씀 요약\]', '', summary)
summary = summary.split('\n')[1]
print(summary)
