import os
import logging
from flask import Flask, request
from routes.cv_routes import cv_bp
from routes.auth_routes import auth_bp  # Optional, if you’re using Google OAuth
from cryptography.fernet import Fernet

# 🧠 Setup Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("🚀 Starting CV App")

# 🔐 Load Fernet Key
fernet_key_raw = os.getenv("FERNET_KEY")
try:
    fernet = Fernet(fernet_key_raw.encode())
    logger.info("🔐 Fernet key loaded successfully.")
except Exception as e:
    logger.error(f"❌ Fernet key loading failed: {e}")

# ⚙️ Initialize Flask App
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

# 🧩 Register Blueprints
try:
    app.register_blueprint(cv_bp)
    logger.info("✅ cv_bp registered successfully.")
except Exception as e:
    logger.error(f"❌ cv_bp registration failed: {e}")

try:
    app.register_blueprint(auth_bp)
    logger.info("✅ auth_bp registered successfully.")
except Exception as e:
    logger.warning(f"⚠️ auth_bp not registered: {e}")

# 📩 Log every request path
@app.before_request
def log_request():
    logger.debug(f"📨 Request: {request.method} {request.path}")

# 🩺 Health check for Azure probes
@app.route("/health")
def health():
    return "OK", 200

# 🚀 Run on Azure-assigned port
if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8000))
        logger.info(f"🌍 Running on port: {port}")
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        import traceback
        logger.error("🛑 App crashed during startup.")
        logger.error(traceback.format_exc())
