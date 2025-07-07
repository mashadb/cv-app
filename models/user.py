from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    # 👤 Login credentials
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # hashed

    # 📬 SMTP config (defaults included)
    smtp_host = db.Column(db.String(255), nullable=False, default='smtp.gmail.com')
    smtp_port = db.Column(db.String(10), nullable=False, default='587')
    smtp_email = db.Column(db.String(255), nullable=False)  # same as user email
    smtp_password_encrypted = db.Column(db.String, nullable=False)  # Fernet encrypted

    def __repr__(self):
        return f'<User {self.email}>'
