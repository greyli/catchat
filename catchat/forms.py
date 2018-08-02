# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, EqualTo


class ProfileForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired(), Length(1, 64)])
    github = StringField('GitHub', validators=[Optional(), URL(), Length(0, 128)])
    website = StringField('Website', validators=[Optional(), URL(), Length(0, 128)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(0, 120)])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
