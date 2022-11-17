from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)

from dotenv import load_dotenv

from pymongo import MongoClient

import certifi

import hashlib

import os

import jwt

import datetime

####유튜브 크롤링 관련 모듈#####
# html 예쁘게 긁어오기 bs4
from bs4 import BeautifulSoup

# 동적페이지 크롤링 selenium
from selenium import webdriver

load_dotenv()
DB = os.getenv('DB')
client = MongoClient(DB, tlsCAFile=certifi.where())

db = client.dbminiW1
# client = MongoClient('mongodb+srv://test:sparta@cluster0.mapsk1p.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.test

SECRET_KEY = 'SPARTA'

# 사이트 시작화면
@app.route('/')
def firstpage():
    return render_template('firstpage.html')

# 회원가입 페이지 이동
@app.route('/signup')
def sign_up():
    return render_template('signup.html')
@app.route("/main/")
def main_home():

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('main.html', nickname=user_info["user_name"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
@app.route('/login/')
def login():
    msg = request.args.get('msg')
    return render_template('login.html', msg=msg)

# 비밀번호 찾기를 위한 회원 검증 과정
@app.route('/checkinfo')
def check_info():
    return render_template('checkinfo.html')


# 비밀번호 찾기를 위한 회원 검증이 끝나면 비밀번호 변경 페이지로 이동
@app.route('/updatepw/<user_id>')
def update_pw(user_id):
    id_receive = request.form.get('user_id')
    return render_template('updatepw.html', id=user_id)

# 아이디 중복검사
@app.route('/api/checkid', methods=['POST'])
def check_id():
    status_name = True
    id_receive = request.form['id_give']
    users = list(db.user.find({}, {'_id': False}))
    for user in users:
        user_id = user['id']
        if user_id == id_receive:
            status_name = False
    return jsonify({'result': 'success', 'status': status_name})


# 닉네임 중복검사
@app.route('/api/checkname', methods=['POST'])
def check_name():
    status_name = True
    name_receive = request.form['name_give']
    users = list(db.user.find({}, {'_id': False}))
    for user in users:
        user_name = user['user_name']
        if user_name == name_receive:
            status_name = False
    return jsonify({'result': 'success', 'status': status_name})


# 이메일 중복 검사
@app.route('/api/checkmail', methods=['POST'])
def check_mail():
    status_mail = True
    mail_receive = request.form['mail_give']
    users = list(db.user.find({}, {'_id': False}))
    for user in users:
        user_mail = user['mail']
        if user_mail == mail_receive:
            status_mail = False
    return jsonify({'result': 'success', 'status': status_mail})


# 회원 정보 저장
@app.route('/api/signup', methods=['POST'])
def join():
    interest_receive = request.form['interest_give']
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    mail_receive = request.form['mail_give']
    pw_receive = request.form['pw_give']

    # 패스워드 단방향 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'user_name': name_receive, 'interest': interest_receive, 'mail': mail_receive,
                        'pw': pw_hash})

    return jsonify({'result': 'success'})

# 아이디와 메일을 체크해 가입된 회원정보가 있는지 확인한다.
@app.route('/api/checkinfo', methods=['POST'])
def check_user():
    id_receive = request.form['id_give']
    mail_receive = request.form['mail_give']
    user = db.user.find_one({'id': id_receive, 'mail': mail_receive}, {'_id': False})
    if user is not None:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'false'})


# 체크한 아이디의 패스워드를 변경
@app.route('/api/updatepw', methods=['PATCH'])
def update_user_pw():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.update_one({'id': id_receive}, {'$set': {'pw': pw_hash}})

    return jsonify({'result': 'success'})

###################여기 바꿔야됨
@app.route('/login')
def signup_in_login():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('main.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for('firstpage', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("firstpage", msg="로그인 정보가 존재하지 않습니다."))


#형준님 회원가입 페이지 로 봐야하는부분입니다
@app.route('/api/signup', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})


#아이디 비밀번호를 받아오며
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest() #비밀번호를 암호화

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5) #로그인이 얼만큼 유지가 되는가
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

#db에서 비밀번호를 디코딩해서 저장되있는 id값 및 닉네임 값을 가져옴
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print('api_valid')

        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['user_name']})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route("/main/todo", methods=["POST"])
def todo_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print('/main/todo')

        db.user.find_one({'id': payload['id']}, {'_id': 0})

        todo_tesk = request.form['todo_tesk']
        today = request.form['today']
        print(todo_tesk, today)
        num = len(list(db.todo.find({}, {'_id': False}))) + 1
        done = 0
        doc = {'id': payload['id'], 'today': today, 'todo_tesk': todo_tesk, 'num': num, 'done': done}
        db.todo.insert_one(doc)
        return jsonify({'msg': '할 일 등록!'})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})







# @app.route("/main/todoload", methods=["GET"])
# def sample_get():
#     #호진작업(끝난듯)
#     id_receive = request.args.get('id_give')
#     todoList = list(db.todo.find({'id': id_receive}, {'_id': False}))
#     #print(todoList)
#
#     return jsonify(todoList)

@app.route("/main/todoload", methods=["GET"])
def sample_get():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print('/main/todoload')
        todoList = list(db.todo.find({'id':payload['id']}, {'_id': False}))

        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({ 'todoList': todoList,'result': 'success', 'nickname': userinfo['user_name']})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route("/main/tododone", methods=["POST"])
def done_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print('/main/tododone')

        item_num = int(request.form['give_itemNum'])

        doneNum = db.todo.find_one({'id': payload['id'], 'num': item_num})['done']
        print(doneNum)
        if doneNum == 1:
            db.todo.update_one({'num': item_num}, {'$set': {'done': 0}})
            doneNum = 1
        else:
            db.todo.update_one({'num': item_num}, {'$set': {'done': 1}})
            doneNum = 0

        return jsonify({'doneNum': doneNum});

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


#유튜브 키워드 크롤링
@app.route('/main/movie', methods=["GET"])
def web_crawling_youtube():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        print('/main/movie')

        # 해당 사용자 키워드 조회
        result = db.user.find_one({'id':payload['id']}, {'_id': False})
        print(result['interest'])

        #### 1. 사용자 키워드 및 크롤링 대상 url 세팅 ####
        keyword = result['interest']
        target_url = 'https://www.youtube.com/results?search_query=' + keyword

        #### 2. 동적페이지 크롤링 ####
        # 옵션 생성
        options = webdriver.ChromeOptions()
        options.add_argument("headless")  # 창 숨기는 옵션 추가(백그라운드로 실행, 이걸 하지 않으면 브라우저 열어서 탐색하게 됨)
        options.add_argument("--disable-gpu")  # gpu 비활성화(gpu 없는 OS)
        options.add_argument("--disable-popup-blocking")  # 광고팝업노출X
        options.add_argument("--blink-settings=imagesEnabled=false")  # 이미지 다운 X

        # driver 실행
        driver = webdriver.Chrome(options=options)
        driver.get(target_url)

        # html 가져오기
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # driver 종료
        driver.quit()

        #### 3. 링크주소 추출 및 json 배열화 ####
        #크롤링 셀렉터 #contents > 는 item 등으로 변경되기에 삭제함
        #for문도 검색이 2개만 되는 경우가 있어서.. 일단 저렇게 함....
        #(반성)selector 부분 덩어리 찾고, 타겟을 하나씩 뽑아야 되는데, 타겟부터 뽑아보게 코딩함...
        youtube_links = []

        if soup != None:
            print('여긴 if인데')
            i = 0
            j = 0
            for i in range(0, 2, 1):
                j += 1
                crawling_link = soup.select_one('ytd-video-renderer:nth-child(' + str(j) + ') > #dismissible > ytd-thumbnail > #thumbnail')['href'].strip()
                crawling_link = crawling_link.replace('/watch?v=', '')  # 링크 식별값만 추출
                youtube_links.append({i: crawling_link})  # append : 배열 뒤로 추가
            youtube_links.append({0: 'jYT7bup2qe0'})  # 죄송합니다...
        else:
            youtube_links.append({0: 'jYT7bup2qe0'})  # 죄송합니다...
            print('이게 아닌데...')

        print(youtube_links)

        return jsonify({'ytb_links': youtube_links})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=1500, debug=True)