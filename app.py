from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient("mongodb+srv://mire:dbsrjsdn1!@cluster0.e4w3e80.mongodb.net/?retryWrites=true&w=majority")
db = client.dbsparta

SECRET_KEY = 'SPARTA'

import jwt

import datetime

import hashlib


@app.route('/')
def firstpage():
    return render_template('firstpage.html')


@app.route('/login')
def login():
    msg = request.args.get('msg')
    return render_template('login.html', msg=msg)



# 회원가입페이지 이동
@app.route('/register')
def signup():
    return render_template('register.html')

#메인 페이지
@app.route('/mainpage')
def mainpage():
    return render_template('/mainpage.html')


#토큰을 받아 맞으면 메인페이지로 이동 및 msg출력
@app.route('/login')
def signup_in_login():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('mainpage.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for('firstpage', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("firstpage", msg="로그인 정보가 존재하지 않습니다."))


#회원가입 페이지에서 값을 받아 db에 저장하는곳
@app.route('/api/register', methods=['POST'])
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
        print(payload)

        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


@app.route("/todo", methods=["POST"])
def todo_post():
    todo_tesk = request.form['todo_tesk']
    num = len(list(db.todo.find({},{'_id':False}))) + 1
    done = 0
    doc = {'todo_tesk': todo_tesk, 'num': num, 'done': done}
    db.todo.insert_one(doc)

    return jsonify({'msg': '작성 완료!'})

@app.route("/todo", methods=["GET"])
def sample_get():
    todoList = list(db.todo.find({}, {'_id': False}))
    return jsonify(todoList)

@app.route("/tododone", methods=["POST"])
def done_post():
    item_num = request.form['give_itemNum']
    type(item_num)
    db.todo.update_one({'num':item_num},{'$set':{'done':1}})

    return jsonify({'msg': '목표 달성!'});



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
