"""Settings for the Global Asset Management site.

Database login comes from environment variables, with defaults for a local MySQL:
  DB_NAME (global_asset), DB_USER (root), DB_PASSWORD (empty), DB_HOST (127.0.0.1), DB_PORT (3306)
"""
import os
from pathlib import Path

import pymysql

pymysql.version_info = (2, 2, 7, "final", 0)
pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "dev-only-key-for-class-demo"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = ["dashboard"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "gasite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": ["django.template.context_processors.request"]},
    }
]

WSGI_APPLICATION = "gasite.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "global_asset"),
        "USER": os.environ.get("DB_USER", "root"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "coursework"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "3306"),
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGIN_MAX_ATTEMPTS = 3
LOGIN_LOCKOUT_SECONDS = 30

# Adding admin emails to login as ADMIN
ADMIN_USERS = {
    "tayloraustin@globalasset.com": {"name": "Agent Austin", "password": "falcon;71"},
    "iqtidertaseen@globalasset.com": {"name": "Agent Taseen", "password": "harbor;24"},
    "avilajose@globalasset.com": {"name": "Agent Jose", "password": "cedar;58"},
}

# "Forgot password?" sends a note to this person
SUPERVISOR_EMAIL = "supervisor@globalasset.com"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "Global Asset Mgmt <no-reply@globalasset.com>"

SUPERVISOR_EMAIL = "iqtidertaseen@gmail.com"      # supervisor email

EMAIL_HOST_USER = os.environ.get("EMAIL_USER", "")         
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD", "") 
if EMAIL_HOST_USER:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_TIMEOUT = 10
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "no-reply@globalasset.com"

USE_TZ = False
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
