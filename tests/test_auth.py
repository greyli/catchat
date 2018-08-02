# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import url_for

from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):

    def test_login_user(self):
        response = self.login()
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Create Snippets', data)
        self.assertNotIn('Sign in', data)

    def test_fail_login(self):
        response = self.login(email='wrong@helloflask.com', password='wrong-password')
        data = response.get_data(as_text=True)
        self.assertIn('Either the email or password was incorrect.', data)

    def test_logout_user(self):
        self.login()
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertNotIn('Create Snippets', data)
        self.assertIn('Sign in', data)

    def test_login_protect(self):
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertIn('Please log in to access this page.', data)

    def test_register(self):
        response = self.client.post(url_for('auth.register'), data={
            'email': 'new@helloflask.com',
            'nickname': 'nick',
            'password': '123'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tell us about you!', data)

    def test_register_email_exist(self):
        response = self.client.post(url_for('auth.register'), data={
            'email': 'test@helloflask.com',
            'nickname': 'nick',
            'password': '123'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('The email is already registered, please log in.', data)
