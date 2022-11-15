from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://ID:PW@clusterName.spvewgv.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('main.html')

@app.route("/sample", methods=["POST"])
def sample_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    doc = {'name': name_receive, 'comment': comment_receive}
    db.fancomments.insert_one(doc)

    return jsonify({'msg': '작성 완료!'})

@app.route("/sample", methods=["GET"])
def sample_get():
    cheer_comments = list(db.fancomments.find({}, {'_id': False}))
    return jsonify(cheer_comments)

if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)