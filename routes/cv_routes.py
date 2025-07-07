from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from models.user import User
from utils.cv_dispatcher import send_cv
import os
from werkzeug.utils import secure_filename

cv_bp = Blueprint("cv_bp", __name__)

# 🏠 Homepage route for Azure root requests
@cv_bp.route("/")
def home():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        return render_template("dashboard.html", user=user)
    return render_template("index.html")  # Optional public landing page

# 📤 CV Upload Handler
@cv_bp.route("/upload", methods=["POST"])
def upload_cv():
    user_id = session.get("user_id")
    if not user_id:
        flash("❌ Please log in to send your CV.", "danger")
        return redirect(url_for("auth_bp.login"))

    user = User.query.get(user_id)
    if not user:
        flash("❌ User not found.", "danger")
        return redirect(url_for("auth_bp.login"))

    recipient_email = request.form.get("recipient_email")
    cv_file = request.files.get("cv_file")

    if not recipient_email or not cv_file:
        flash("❌ Both recipient email and CV file are required.", "danger")
        return redirect(url_for("dashboard"))

    # 🔐 Gmail OAuth Check
    gmail_creds = session.get("gmail_credentials")
    if not gmail_creds:
        flash("⚠️ Gmail not connected. Please authorize first.", "warning")
        return redirect(url_for("dashboard"))

    # 💾 Save File Temporarily
    try:
        upload_folder = os.path.join("static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)
        filename = secure_filename(cv_file.filename)
        cv_path = os.path.join(upload_folder, filename)
        cv_file.save(cv_path)
    except Exception as e:
        print("🛑 File save error:", e)
        flash("❌ Error saving CV file.", "danger")
        return redirect(url_for("dashboard"))

    # 📧 Send via Gmail
    try:
        subject = f"📄 CV Submission from {user.email}"
        html_body = f"<h3>{user.email} submitted a CV.</h3><p>Please review the attached file.</p>"
        status = send_cv(user, recipient_email, cv_path, subject, html_body, gmail_creds)
        flash(status, "success" if "✅" in status else "danger")
    except Exception as e:
        print("🛑 Gmail send error:", e)
        flash("❌ Failed to send CV via Gmail.", "danger")

    # 🧹 Cleanup
    try:
        os.remove(cv_path)
    except Exception as e:
        print("⚠️ Could not delete temp CV file:", e)

    return redirect(url_for("dashboard"))
