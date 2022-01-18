from bs4 import BeautifulSoup
from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.sparta_3team

# doc = {'name': 'sea_elephant'}
# db.users.insert_one(doc)


## URL 별로 함수명이 같거나,
## route('/') 등의 주소가 같으면 안됩니다.

# index_.html 불러오기
@app.route('/')
def home():
    return render_template('final_matView.html')




# DB작성(이름, 리뷰, 별점)
@app.route('/review', methods=['POST'])
def review_POST():

   name_recieve = request.form['name_give'] # name_recieve 로 클라이언트가 준 name 가져오기
   review_recieve = request.form['review_give'] # review_recieve 로 클라이언트가 준 review 가져오기
   star_recieve = request.form['star_give'] # star -- 로 클라이언트가 준 별점 가져오기

   doc = {'name':name_recieve,
          'review':review_recieve,
          'star':star_recieve
          }
   db.cafereview.insert_one(doc) # db에 name, review, star 저장

   return jsonify({'msg': '리뷰가 성공적으로 작성되었습니다.'})

# 리뷰 저장하기
def get_datas():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://openapi.gg.go.kr/PlaceThatDoATasteyFoodSt?KEY=86a1365c9daa4cf3b12afb3126c439c7', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    trs = soup.select('#folder3 > div.opened > div:nth-child(2)')
    print(soup)


# 리뷰 보여주기
@app.route('/review', methods=['GET'])
def review_get():

    reviews = list(db.cafereview.find({},{'_id': False}))

    return jsonify({'all_reviews': reviews})

# 맛집 API 저장
def get_datas():
   headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
   data = requests.get('https://openapi.gg.go.kr/PlaceThatDoATasteyFoodSt?KEY=86a1365c9daa4cf3b12afb3126c439c7',
                       headers=headers)

   soup = BeautifulSoup(data.text, 'html.parser')
   # print(soup)

   rows = soup.select('row')

   for names in rows:
      name = names.select_one('restrt_nm').text
      juso = names.select_one('REFINE_ROADNM_ADDR').text
      callnumber = names.select_one('TASTFDPLC_TELNO').text
      gyundo = names.select_one('REFINE_WGS84_LOGT').text
      wedo = names.select_one('REFINE_WGS84_LAT').text
      dic = {'name':name,
             'juso':juso,
             'callnumber':callnumber,
             'gyundo':gyundo,
             'wedo':wedo
             }
      # print(dic)
      db.matjipjido.insert_one(dic)
   return rows
# app.py를 run할때 Api를 새로 불러옵니다
def insert_all():
    db.matjipjido.drop()  # matjipjido 콜렉션을 모두 지워줍니다.
    get_datas()


insert_all()

# 맛집API 불러오기
@app.route('/list', methods=['GET'])
def show_reviews():

    matjip_list = list(db.matjipjido.find({},{'_id': False}))

    return jsonify({'all_list': matjip_list})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

