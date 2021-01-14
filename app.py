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
def read_keword():
    keyword = request.args.get('keyword_give')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://m.search.naver.com/search.naver?where=m_view&sm=mtb_jum&query=' + keyword,
                        headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    lis = soup.select(
        '#_view_review_body_html > div > div > panel-list > div:nth-child(1) > select-contents > more-contents > div > ul > li')
    results = []
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
        info = {
            'rank': rank,
            'name': name,
            'date': date.text,
            'url': url
        }
        results.append(info)
        if 'moment' in url:
            print('type', 'moment')
            type = {
                'type': 'moment'
            }
            results.append(type)
            continue
        elif 'cafe' in url:
            print('type', 'cafe')
            type = {
                'type': 'cafe'
            }
            results.append(type)
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
            blog = {
                'type': 'blog',
                'total_image': len(img_list),
                'total_keyword': content.text.count(keyword),
                'total_text': len(content.text)
            }
            results.append(blog)
    return jsonify({'result': 'success', 'data': results})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
