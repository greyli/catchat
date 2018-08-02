# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user, login_required

from catchat.extensions import db
from catchat.forms import ProfileForm
from catchat.models import Message, User
from catchat.utils import flash_errors

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
def home():
    messages = Message.query.order_by(Message.timestamp.asc())
    user_amount = User.query.count()
    return render_template('chat/home.html', messages=messages, user_amount=user_amount)


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
