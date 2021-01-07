import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
keyword = '강아지'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://m.search.naver.com/search.naver?where=m_view&sm=mtb_jum&query=' + keyword, headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.

soup = BeautifulSoup(data.text, 'html.parser')

# _view_review_body_html > div > div > panel-list > div:nth-child(1) > select-contents > more-contents > div > ul > li:nth-child(1) > div > a
# _view_review_body_html > div > div > panel-list > div:nth-child(1) > select-contents > more-contents > div > ul > li
# _view_review_body_html > div > div > panel-list > div:nth-child(1) > select-contents > more-contents > div > ul > li:nth-child(1) > div > a > mark
# ranks = soup.select('#_view_review_body_html > div > div > panel-list > div > select-contents > more-contents > div > ul > li')
# for rank in ranks :
#     title = rank.select_one('div div ')
#     url = rank.select_one('div > a')
#     print(title.text)

lists = soup.select(
    '#_view_review_body_html > div > div > panel-list > div > select-contents > more-contents > div > ul > li ')
for list in lists:
    all = list.select_one('div')
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
