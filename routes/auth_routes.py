from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from google_auth_oauthlib.flow import Flow
import os

auth_bp = Blueprint('auth_bp', __name__)

# 🛂 Registration Route (no SMTP setup)
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        re_password = request.form.get('re_password')

        if password != re_password:
            flash('❌ Passwords do not match.', 'danger')
            return redirect(url_for('auth_bp.register'))

        if User.query.filter_by(email=email).first():
            flash('⚠️ Email already exists.', 'warning')
            return redirect(url_for('auth_bp.register'))

        hashed_pw = generate_password_hash(password)

        new_user = User(email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('✅ Account created!', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('auth/register.html')

# 🔐 Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('❌ Invalid credentials.', 'danger')
            return redirect(url_for('auth_bp.login'))

        session['user_id'] = user.id
        flash('✅ Logged in successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('auth/login.html')

# 🔐 Gmail OAuth Login
@auth_bp.route('/login/google')
def login_google():
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/gmail.send'],
        redirect_uri=url_for('auth_bp.auth_callback', _external=True)
    )
    auth_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state
    return redirect(auth_url)

@auth_bp.route('/auth/callback')
def auth_callback():
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/gmail.send'],
        redirect_uri=url_for('auth_bp.auth_callback', _external=True),
        state=session['state']
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['gmail_credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    flash('✅ Gmail authorized!', 'success')
    return redirect(url_for('dashboard'))
