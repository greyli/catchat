# -*- coding: utf-8 -*-
""" 
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from tests.base import BaseTestCase
from catchat.extensions import db
from catchat.models import User, Message


class CLITestCase(BaseTestCase):

    def setUp(self):
        super(CLITestCase, self).setUp()
        db.drop_all()

    def test_initdb_command(self):
        result = self.runner.invoke(args=['initdb'])
        self.assertIn('Initialized database.', result.output)

    def test_initdb_command_with_drop(self):
        result = self.runner.invoke(args=['initdb', '--drop'], input='y\n')
        self.assertIn('This operation will delete the database, do you want to continue?', result.output)
        self.assertIn('Drop tables.', result.output)

    def test_forge_command(self):
        result = self.runner.invoke(args=['forge'])

        self.assertEqual(User.query.count(), 50 + 1)
        self.assertIn('Generating users...', result.output)

        self.assertEqual(Message.query.count(), 300)
        self.assertIn('Generating messages...', result.output)

        self.assertIn('Done.', result.output)

    def test_forge_command_with_count(self):
        result = self.runner.invoke(args=['forge', '--message', '100'])

        self.assertEqual(Message.query.count(), 100)
        self.assertIn('Generating messages...', result.output)

        self.assertIn('Done.', result.output)
