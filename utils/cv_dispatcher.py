import smtplib
import ssl
from email.message import EmailMessage
from utils.security import decrypt_password
import os

# 🔄 Shared fallback credentials (optional)
DEFAULT_SMTP_EMAIL = os.getenv("SMTP_EMAIL")
DEFAULT_SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
DEFAULT_SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
DEFAULT_SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

def detect_provider(email):
    if email.endswith('@gmail.com'):
        return 'smtp.gmail.com', 587
    elif email.endswith('@outlook.com') or email.endswith('@hotmail.com'):
        return 'smtp.office365.com', 587
    elif email.endswith('@yahoo.com'):
        return 'smtp.mail.yahoo.com', 587
    else:
        return DEFAULT_SMTP_HOST, DEFAULT_SMTP_PORT

def send_cv(user, recipient_email, cv_path, subject="CV Submission", body="Attached is my CV."):
    # ✉️ Use user credentials if present
    smtp_email = user.smtp_email or DEFAULT_SMTP_EMAIL
    smtp_password = decrypt_password(user.smtp_password_encrypted) if user.smtp_password_encrypted else DEFAULT_SMTP_PASSWORD
    smtp_host, smtp_port = detect_provider(smtp_email)

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f"{user.email}"  # Actual user address
    msg['To'] = recipient_email
    msg['Reply-To'] = user.email  # Ensures replies go to user
    msg.set_content(body)

    # 📎 Attach CV
    with open(cv_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(cv_path)
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # 🔐 Send via SMTP
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls(context=context)
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
        return "✅ CV sent successfully."
    except Exception as e:
        print(f"Error: {e}")
        return "❌ Failed to send CV."
