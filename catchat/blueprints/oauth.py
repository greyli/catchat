# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os

from flask import flash, redirect, url_for, Blueprint, abort
from flask_login import login_user, current_user

from catchat.extensions import oauth, db
from catchat.models import User

oauth_bp = Blueprint('oauth', __name__)

github = oauth.remote_app(
    name='github',
    consumer_key=os.getenv('GITHUB_CLIENT_ID'),
    consumer_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    request_token_params={'scope': 'user'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

google = oauth.remote_app(
    name='google',
    consumer_key=os.getenv('GOOGLE_CLIENT_ID'),
    consumer_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    request_token_params={'scope': 'email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)
twitter = oauth.remote_app(
    name='twitter',
    consumer_key=os.getenv('TWITTER_CLIENT_ID'),
    consumer_secret=os.getenv('TWITTER_CLIENT_SECRET'),
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
)

providers = {
    'github': github,
    'google': google,
    'twitter': twitter
}

profile_endpoints = {
    'github': 'user',
    'google': 'userinfo',
    'twitter': 'account/verify_credentials.json?include_email=true'
}


def get_social_profile(provider, access_token):
    profile_endpoint = profile_endpoints[provider.name]
    response = provider.get(profile_endpoint, token=access_token)

    if provider.name == 'twitter':
        username = response.data.get('name')
        website = response.data.get('url')
        github = ''
        email = response.data.get('email')
        bio = response.data.get('description')
    elif provider.name == 'google':
        username = response.data.get('name')
        website = response.data.get('link')
        github = ''
        email = response.data.get('email')
        bio = ''
    else:
        username = response.data.get('name')
        website = response.data.get('blog')
        github = response.data.get('html_url')
        email = response.data.get('email')
        bio = response.data.get('bio')
    return username, website, github, email, bio


@oauth_bp.route('/login/<provider_name>')
def oauth_login(provider_name):
    if provider_name not in providers.keys():
        abort(404)

    if current_user.is_authenticated:
        return redirect(url_for('chat.home'))

    callback = url_for('.oauth_callback', provider_name=provider_name, _external=True)
    return providers[provider_name].authorize(callback=callback)


@oauth_bp.route('/callback/<provider_name>')
def oauth_callback(provider_name):
    if provider_name not in providers.keys():
        abort(404)

    provider = providers[provider_name]
    response = provider.authorized_response()

    if response is not None:
        if provider_name == 'twitter':
            access_token = response.get('oauth_token'), response.get('oauth_token_secret')
        else:
            access_token = response.get('access_token')
    else:
        access_token = None

    if access_token is None:
        flash('Access denied, please try again.')
        return redirect(url_for('auth.login'))

    username, website, github, email, bio = get_social_profile(provider, access_token)

    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email=email, nickname=username, website=website,
                    github=github, bio=bio)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('chat.profile'))
    login_user(user, remember=True)
    return redirect(url_for('chat.home'))
