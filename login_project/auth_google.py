from flask import Blueprint, render_template,  redirect, url_for, request, flash, session
import requests
from .models import User
from . import oauth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

auth_google = Blueprint('auth_google', __name__)

@auth_google.route('/login/google')
def login_google():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth_google.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_google.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    email = user_info['email']
    name = user_info['name']
    id = user_info['id']
    user = User.query.filter_by(email=email).first()
    if not user:
        new_user = User(email=email, name=name, password=generate_password_hash(id, method='sha256'), loginvia = True)
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        user = User.query.filter_by(email=email).first()
        login_user(user)
        return redirect(url_for('main.profile'))
    login_user(user)
    return redirect(url_for('main.profile'))