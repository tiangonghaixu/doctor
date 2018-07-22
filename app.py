# coding=utf-8
import os

from flask import Flask

from handlers.ask.get_ask_list_handler import GetAskListHandler
from handlers.hello_handler import HelloHandler
from handlers.news.get_news_by_category_handler import GetNewsByCategoryHandler
from handlers.news.get_news_categories_handler import GetNewsCategoriesHandler
from handlers.user.login_handler import LoginHandler
from handlers.user.report_status_handler import UserReportStatusHandler

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF', "docx"])

app.add_url_rule('/hello', view_func=HelloHandler.as_view("index"))
# 用户
app.add_url_rule('/v1/user/login', view_func=LoginHandler.as_view("user_login"))
app.add_url_rule('/v1/user/report_status', view_func=UserReportStatusHandler.as_view("user_report_status"))

# 问答
app.add_url_rule('/v1/ask/get_list', view_func=GetAskListHandler.as_view("ask_get_list"))

# 头条
app.add_url_rule('/v1/news/categories', view_func=GetNewsCategoriesHandler.as_view("news_category_list"))
app.add_url_rule('/v1/news/by_category', view_func=GetNewsByCategoryHandler.as_view("news_list"))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
