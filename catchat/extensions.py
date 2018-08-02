# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_login import LoginManager
from flask_moment import Moment
from flask_oauthlib.client import OAuth
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()
oauth = OAuth()


@login_manager.user_loader
def load_user(user_id):
    from catchat.models import User
    return User.query.get(int(user_id))


login_manager.login_view = 'auth.login'
