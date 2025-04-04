import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Security-Too configuration
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'salt-change-in-production')
    SECURITY_REGISTERABLE = False  # We use our custom registration
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_CONFIRMABLE = False  # Disable email confirmation
    SECURITY_SEND_REGISTER_EMAIL = False  # Disable registration email
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False  # Disable password change email
    SECURITY_USERNAME_ENABLE = False  # We're using email as the main identifier
    SECURITY_URL_PREFIX = None
    SECURITY_LOGIN_URL = '/auth/login'
    SECURITY_LOGOUT_URL = '/auth/logout'
    SECURITY_CHANGE_URL = '/auth/change-password'
    SECURITY_POST_LOGIN_VIEW = 'dashboard.index'
    SECURITY_POST_LOGOUT_VIEW = 'auth.login'
    SECURITY_POST_CHANGE_VIEW = 'dashboard.index'
    SECURITY_TOKEN_MAX_AGE = 3600  # 1 hour
    SECURITY_RESET_PASSWORD_WITHIN = '1 days'
    SECURITY_TWO_FACTOR = False
    SECURITY_BLUEPRINT_NAME = 'security'

    # Email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_PROTECTION = 'strong'

    # Upload configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
