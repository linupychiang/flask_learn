from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

db_flask_demo = PyMongo(
    app,
    uri='mongodb://admin:12345678@localhost:27017/flask_demo?authSource=admin')


@app.route('/')
def get_index():
    datas = db_flask_demo.db.datas.find({'name': 'zhangsan'}, {'_id': 0})
    return render_template('index.html',
                           name=datas[0]['name'],
                           movies=datas[0]['movies'])
