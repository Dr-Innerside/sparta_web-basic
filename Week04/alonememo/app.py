from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.preboot


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['GET'])
def read_articles():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    articles = list(db.articles.find({},{'_id': False}))
    # 2. articles라는 키 값으로 영화정보 내려주기
    return jsonify({'all_articles': articles})


## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def post_articles():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title': title,
        'image': image,
        'desc': desc,
        'url': url_receive,
        'comment': comment_receive
    }

    db.articles.insert_one(doc)


    return jsonify({'msg': 'POST 연결되었습니다!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
