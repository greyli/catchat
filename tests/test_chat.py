# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import url_for, current_app

try:
    from unittest import mock
except ImportError:
    import mock

from tests.base import BaseTestCase
from catchat.extensions import db, socketio
from catchat.models import User, Message


class ChatTestCase(BaseTestCase):

    def setUp(self):
        super(ChatTestCase, self).setUp()

        admin = User(email='admin@helloflask.com', nickname='Admin User', github='https://github.com/greyli')
        admin.set_password('123')
        message1 = Message(body='Test Message 1')
        message2 = Message(body='Test Message 2')
        message3 = Message(body='Test Message 3')
        admin.messages = [message1, message2, message3]
        db.session.add(admin)
        db.session.commit()

    @mock.patch('flask_login.utils._get_user')
    def test_new_message_event(self, current_user):
        current_user.return_value = User.query.get(1)

        self.assertEqual(User.query.get(1).messages, [])
        self.login()

        socketio_client = socketio.test_client(current_app)
        socketio_client.get_received()
        socketio_client.emit('new message', 'Hello, Test')
        received = socketio_client.get_received()
        self.assertEqual(received[0]['name'], 'new message')
        self.assertEqual(received[0]['args'][0]['message_body'], '<p>Hello, Test</p>')
        self.assertNotEqual(User.query.get(1).messages, [])
        self.assertEqual(User.query.get(1).messages[0].body, '<p>Hello, Test</p>')

        response = self.client.get(url_for('chat.home'))
        data = response.get_data(as_text=True)
        self.assertIn('Hello, Test', data)

        socketio_client.disconnect()

    @mock.patch('flask_login.utils._get_user')
    def test_new_anonymous_message_event(self, current_user):
        current_user.return_value = User.query.get(1)

        self.assertEqual(User.query.get(1).messages, [])
        self.login()
        socketio_client = socketio.test_client(current_app, namespace='/anonymous')
        socketio_client.get_received('/anonymous')
        socketio_client.emit('new message', 'Hello, Anonymous', namespace='/anonymous')
        received = socketio_client.get_received('/anonymous')
        self.assertEqual(received[0]['name'], 'new message')
        self.assertEqual(received[0]['args'][0]['message_body'], '<p>Hello, Anonymous</p>')
        self.assertEqual(User.query.get(1).messages, [])

        socketio_client.disconnect(namespace='/anonymous')

    @mock.patch('flask_login.utils._get_user')
    def test_connect_event(self, current_user):
        self.login()

        socketio_client = socketio.test_client(current_app)
        received = socketio_client.get_received()
        self.assertEqual(received[0]['name'], 'user count')
        self.assertEqual(received[0]['args'][0]['count'], 1)
        socketio_client.disconnect()

    @mock.patch('flask_login.utils._get_user')
    def test_disconnect_event(self, current_user):
        self.login()

        socketio_client = socketio.test_client(current_app)
        socketio_client.get_received()
        socketio_client.disconnect()
        received = socketio_client.get_received()
        self.assertEqual(received[0]['name'], 'user count')
        self.assertEqual(received[0]['args'][0]['count'], 0)

    def test_home_page(self):
        response = self.client.get(url_for('chat.home'))
        data = response.get_data(as_text=True)
        self.assertIn('Test Message 1', data)
        self.assertIn('Test Message 2', data)
        self.assertIn('Test Message 3', data)

    def test_anonymous_page(self):
        response = self.client.get(url_for('chat.anonymous'))
        data = response.get_data(as_text=True)
        self.assertIn('CatChat (Incognito Mode)', data)
        self.assertNotIn('Test Message 1', data)

    def test_get_messages(self):
        current_app.config['CATCHAT_MESSAGE_PER_PAGE'] = 1
        response = self.client.get(url_for('chat.home'))
        data = response.get_data(as_text=True)
        self.assertIn('Test Message 3', data)
        self.assertNotIn('Test Message 1', data)
        self.assertNotIn('Test Message 2', data)

        response = self.client.get(url_for('chat.get_messages', page=1))
        data = response.get_data(as_text=True)
        self.assertIn('Test Message 3', data)
        self.assertNotIn('Test Message 1', data)
        self.assertNotIn('Test Message 2', data)

        response = self.client.get(url_for('chat.get_messages', page=2))
        data = response.get_data(as_text=True)
        self.assertIn('Test Message 2', data)
        self.assertNotIn('Test Message 1', data)
        self.assertNotIn('Test Message 3', data)

        response = self.client.get(url_for('chat.get_messages', page=3))
        data = response.get_data(as_text=True)
        self.assertIn('Test Message 1', data)
        self.assertNotIn('Test Message 2', data)
        self.assertNotIn('Test Message 3', data)

    def test_delete_message(self):
        self.login(email='admin@helloflask.com', password='123')
        response = self.client.delete(url_for('chat.delete_message', message_id=1))
        self.assertEqual(response.status_code, 204)

        response = self.client.get(url_for('chat.home'))
        data = response.get_data(as_text=True)
        self.assertNotIn('Test Message 1', data)
        self.assertIn('Test Message 2', data)
        self.assertIn('Test Message 3', data)

        user = User.query.get(1)
        message4 = Message(body='Test Message 4')
        user.messages.append(message4)
        db.session.commit()

        response = self.client.delete(url_for('chat.delete_message', message_id=4))
        self.assertEqual(response.status_code, 204)

        response = self.client.get(url_for('chat.home'))
        data = response.get_data(as_text=True)
        self.assertNotIn('Test Message 4', data)
        self.assertIn('Test Message 2', data)
        self.assertIn('Test Message 3', data)

        self.logout()
        self.login()

        response = self.client.delete(url_for('chat.delete_message', message_id=2))
        self.assertEqual(response.status_code, 403)

    def test_get_profile(self):
        response = self.client.get(url_for('chat.get_profile', user_id=2))
        data = response.get_data(as_text=True)
        self.assertIn('admin', data)
        self.assertIn('Admin User', data)
        self.assertIn('https://github.com/greyli', data)
        self.assertIn('This user want to maintain an aura of mystique.', data)

    def test_edit_profile(self):
        self.login(email='admin@helloflask.com', password='123')
        self.client.post(url_for('chat.profile'), data={
            'nickname': 'New Name',
            'github': 'https://github.com/helloflask',
            'bio': 'blah...'
        }, follow_redirects=True)
        response = self.client.get(url_for('chat.get_profile', user_id=2))
        data = response.get_data(as_text=True)
        self.assertIn('New Name', data)
        self.assertNotIn('Admin User', data)
        self.assertIn('https://github.com/helloflask', data)
        self.assertNotIn('https://github.com/greyli', data)
        self.assertIn('blah...', data)
        self.assertNotIn('This user want to maintain an aura of mystique.', data)
