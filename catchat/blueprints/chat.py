# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user, login_required
from flask_socketio import emit

from catchat.extensions import socketio, db
from catchat.forms import ProfileForm
from catchat.models import Message, User
from catchat.utils import flash_errors

chat_bp = Blueprint('chat', __name__)

online_users = []


@socketio.on('new message')
def new_message(message_body):
    message = Message(author=current_user._get_current_object(), body=message_body)
    db.session.add(message)
    db.session.commit()
    emit('new message',
         {'message_html': render_template('chat/_message.html', message=message)},
         broadcast=True)


@socketio.on('new message', namespace='/anonymous')
def new_anonymous_message(message_body):
    avatar = 'https://www.gravatar.com/avatar?d=mm'
    nickname = 'Anonymous'
    emit('new message',
         {'message_html': render_template('chat/_anonymous_message.html',
                                          message=message_body,
                                          avatar=avatar,
                                          nickname=nickname)},
         broadcast=True, namespace='/anonymous')


@socketio.on('connect')
def connect():
    global online_users
    if current_user.is_authenticated and current_user.id not in online_users:
        online_users.append(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


@socketio.on('disconnect')
def disconnect():
    global online_users
    if current_user.is_authenticated and current_user.id in online_users:
        online_users.remove(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


@chat_bp.route('/')
def home():
    messages = Message.query.order_by(Message.timestamp.asc())
    user_amount = User.query.count()
    return render_template('chat/home.html', messages=messages, user_amount=user_amount)


@chat_bp.route('/anonymous')
def anonymous():
    return render_template('chat/anonymous.html')


@chat_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.github = form.github.data
        current_user.website = form.website.data
        current_user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('.home'))
    flash_errors(form)
    return render_template('chat/profile.html', form=form)


@chat_bp.route('/profile/<user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('chat/_profile_card.html', user=user)
