import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)
db = client.dbsparta
# 기본 세팅 완료 !

keyword = '강아지'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://m.search.naver.com/search.naver?where=m_view&sm=mtb_jum&query=' + keyword, headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

lists = soup.select(
    '#_view_review_body_html > div > div > panel-list > div > select-contents > more-contents > div > ul > li ')
for list in lists:
    title = list.select_one('div div > a.api_txt_lines.total_tit')
    date = list.select_one('div div span.sub_time.sub_txt')
    url = list.select_one('div > a')
    img = list.select_one('div div em')
    img2 = list.select_one('div.total_wrap > div.api_list_scroll_wrap.review_thumb_group._svp_content > div > ul')

    print(title.text)
    print(date.text)
    print(url['data-url'])
    if img is not None:
        print(img.text)
    if img2 is not None:
        print(img2)
    print()


