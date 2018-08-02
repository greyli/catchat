# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os

os.environ['GITHUB_CLIENT_ID'] = 'test'
os.environ['GITHUB_CLIENT_SECRET'] = 'test'
os.environ['GOOGLE_CLIENT_ID'] = 'test'
os.environ['GOOGLE_CLIENT_SECRET'] = 'test'
os.environ['TWITTER_CLIENT_ID'] = 'test'
os.environ['TWITTER_CLIENT_SECRET'] = 'test'

import unittest

from flask import url_for

from catchat import create_app
from catchat.extensions import db
from catchat.models import User


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()
        user = User(nickname='Grey Li', email='test@helloflask.com')
        user.set_password('123')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, email=None, password=None):
        if email is None and password is None:
            email = 'test@helloflask.com'
            password = '123'

        return self.client.post(url_for('auth.login'), data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)
