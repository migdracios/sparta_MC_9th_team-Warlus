from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.sparta_3team

# doc = {'name': 'sea_elephant'}
# db.users.insert_one(doc)


## URL 별로 함수명이 같거나,
## route('/') 등의 주소가 같으면 안됩니다.

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/review', methods=['POST'])  # DB작성(이름, 리뷰, 별점)
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

@app.route('/review', methods=['GET'])
def review_get():

    reviews = list(db.cafereview.find({},{'_id': False}))

    return jsonify({'all_reviews': reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

