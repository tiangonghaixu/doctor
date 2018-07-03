# coding=utf-8
import os

from flask import Flask

from handlers.ask.get_ask_list_handler import GetAskListHandler
from handlers.hello_handler import HelloHandler
from handlers.user.login_handler import LoginHandler

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF', "docx"])

app.add_url_rule('/hello', view_func=HelloHandler.as_view("index"))
app.add_url_rule('/v1/user/login', view_func=LoginHandler.as_view("login"))
app.add_url_rule('/v1/ask/get_list', view_func=GetAskListHandler.as_view("ask_get_list"))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=False)
