from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from datetime import timedelta


client = MongoClient('localhost', 27017)
db = client.question

app = Flask(__name__)
app.secret_key = "BBackco@question!"
app.permanent_session_lifetime = timedelta(days = 1)

@app.route('/')
def home():
    return render_template('mainpage.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


@app.route('/contents')
def contents():
    return render_template('contents.html')

@app.route('/all_list')
def all_list():
    return render_template('all_list.html')
    
@app.route('/user_info')
def user_info():
    return render_template('user_info.html')

# register api
@app.route('/register', methods=['POST'])
def register_info():
    if request.method == "POST":
        user_receive = request.form['user_give']
        email_receive = request.form['email_give']
        pw_receive = request.form['pw_give']
        repeatpw_receive = request.form['repeatpw_give']

    if "@" not in email_receive:
        return jsonify({'msg': '이메일을 입력해주세요.'})

    elif '.' not in email_receive:
        return jsonify({'msg': '이메일을 완성해주세요'})

    elif not (email_receive and pw_receive and repeatpw_receive):
        return jsonify({'msg': '모두 입력해주세요'})

    doc, data = {
        'username': username_receive,
        'email': email_receive,
        'pw': pw_receive,
        'repeatpw': repeatpw_receive
    }

    db.bbackco.insert_one(doc)
    return jsonify({'msg': '회원가입 완료!'})


@app.route('/login/post', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email_receive = request.form['email_give']
        pw_receive = request.form['pw_give']
        session["user"] = user

    users = list(db.bbackco.findOne({}, {'_id': False}))

    if "@" and "." not in email_receive:
        return jsonify({"msg": "이메일을 확인해주세요"})
    elif not (email_receive and pw_receive):
        return jsonify({'msg': '패스워드를 입력해주세요'})
    else:
        for user in users:
            if email_receive in user['email'] and pw_receive in user['pw']:
                if "user" in session:
                   return jsonify({'msg': '환영합니다'})
            else:
                return jsonify({'msg': '입력값을 확인해주세요'})
                
@app.route("/logout")
def logout():
    return jsonify({'msg': '로그아웃 하시겠습니까?'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug="true")


