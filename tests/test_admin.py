# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import url_for

from tests.base import BaseTestCase
from catchat.extensions import db
from catchat.models import User


class AdminTestCase(BaseTestCase):

    def setUp(self):
        super(AdminTestCase, self).setUp()
        admin = User(email='admin@helloflask.com', nickname='Admin User')
        admin.set_password('123')
        db.session.add(admin)
        db.session.commit()

    def test_admin_permission(self):
        response = self.client.delete(url_for('admin.block_user', user_id=1))
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.delete(url_for('admin.block_user', user_id=1))
        self.assertEqual(response.status_code, 403)

    def test_block_admin(self):
        self.login(email='admin@helloflask.com', password='123')
        response = self.client.delete(url_for('admin.block_user', user_id=2))
        self.assertEqual(response.status_code, 400)

    def test_block_user(self):
        self.login(email='admin@helloflask.com', password='123')
        response = self.client.delete(url_for('admin.block_user', user_id=1))
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(User.query.get(1))
