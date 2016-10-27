# -*- coding: utf-8 -*-

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api
import sys

# Fix messy code
reload(sys)
sys.setdefaultencoding("utf8")


app = Flask(__name__)
app.config.from_object('config')

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

api = Api(app)


from app import views, models

@login_manager.user_loader
def load_user(user_id):
  return models.User.query.get(int(user_id))


if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('Otaku Calendar startup')