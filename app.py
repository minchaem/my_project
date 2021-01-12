import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
client = MongoClient('localhost', 27017)
db = client.dbsparta

keyword = '강아지'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://m.search.naver.com/search.naver?where=m_view&sm=mtb_jum&query=' + keyword, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

lis = soup.select(
    '#_view_review_body_html > div > div > panel-list > div:nth-child(1) > select-contents > more-contents > div > ul > li')
for li in lis:
    a_tag = li.select_one('div.total_wrap > a')
    name = a_tag.text
    url = a_tag['href']
    if 'moment' in url:
        continue
    elif 'cafe' in url:
        continue
    elif 'blog' in url:
        print(name)
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        content = soup.select_one('#viewTypeSelector')
        img_list = content.select('img')
        text_length = content.select('span.se-fs-.se-ff-')
        print('total image', len(img_list))
        print('total keyword', content.text.count(keyword))
        print('total text', len(text_length))