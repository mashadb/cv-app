from flask import Blueprint, request, redirect, url_for, flash, session
from models.user import User, db
from utils.security import encrypt_password

settings_bp = Blueprint('settings_bp', __name__)

@settings_bp.route('/update', methods=['POST'])
def update_smtp():
    # 🔐 Ensure user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to configure SMTP settings.', 'danger')
        return redirect(url_for('auth_bp.login'))

    # 🧾 Get form fields
    smtp_host = request.form.get('smtp_host')
    smtp_port = request.form.get('smtp_port')
    smtp_email = request.form.get('smtp_email')
    smtp_password = request.form.get('smtp_password')

    # 🧪 Basic validation
    if not smtp_host or not smtp_port or not smtp_email or not smtp_password:
        flash('All SMTP fields are required.', 'danger')
        return redirect(url_for('dashboard'))

    # ✨ Encrypt and update
    encrypted_smtp_pw = encrypt_password(smtp_password)

    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth_bp.login'))

    user.smtp_host = smtp_host
    user.smtp_port = smtp_port
    user.smtp_email = smtp_email
    user.smtp_password_encrypted = encrypted_smtp_pw
    db.session.commit()

    flash('✅ SMTP configuration saved successfully.', 'success')
    return redirect(url_for('dashboard'))
