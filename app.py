import requests
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')

# API 역할을 하는 부분
@app.route('/my_project', methods=['GET'])
def show_stars():
    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    star_list = list(db.mystar.find({},{'_id':False}).sort('like', -1))

    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'data': star_list})

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
    date = li.select_one('div.total_wrap > div.total_sub > span > span > span.etc_dsc_area > span')
    rank = li['data-cr-rank']

    print()
    print('rank', rank)
    print(name)
    print('date', date.text)
    print(url)
    if 'moment' in url:
        print('type', 'moment')
        continue
    elif 'cafe' in url:
        print('type', 'cafe')
        continue
    elif 'blog' in url:
        print('type', 'blog')
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        content = soup.select_one('#viewTypeSelector')
        img_list = content.select('img')
        print('total image', len(img_list))
        print('total keyword', content.text.count(keyword))
        print('total text', len(content.text))



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


