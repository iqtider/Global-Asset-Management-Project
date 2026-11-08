"""Settings for the Global Asset Management demo site.

Database login comes from environment variables, with defaults for a local MySQL:
  DB_NAME (global_asset), DB_USER (root), DB_PASSWORD (empty), DB_HOST (127.0.0.1), DB_PORT (3306)
"""
import os
from pathlib import Path

import pymysql

# PyMySQL stands in for mysqlclient, which is hard to install on Windows.
pymysql.version_info = (2, 2, 7, "final", 0)
pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "dev-only-key-for-class-demo"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = ["dashboard"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "3306"),
    }
}

USE_TZ = False
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
