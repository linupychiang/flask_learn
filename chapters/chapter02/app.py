from flask import Flask
from markupsafe import escape

app = Flask(__name__)

# flask默认你把程序存储在app.py 或 wsgi.py 中
# 所以如果app.py更改成了其他名称，需要指定环境变量的值FLASK_APP='ooxx.py'

# 关于flask中的环境变量
# FLASK_APP
# FLASK_ENV，默认为production，开发时设置为调试模式，即更改为development


@app.route('/')
@app.route('/hello')
def hello_flask():
    return 'hello, flask'


@app.route('/user/<name>')
def get_user(name):
    return {'name': escape(name)}  # 对用户输入内容转义（安全考虑）
