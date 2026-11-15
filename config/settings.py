"""
Configurações do Django para o projeto "config".
Gerado por 'django-admin startproject' usando Django 6.0.
"""

from pathlib import Path
import os
import re
import sys

from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DJANGO_DEBUG", "0").lower() in ("1", "true", "yes", "on")
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured("Defina DJANGO_SECRET_KEY; para desenvolvimento local, defina DJANGO_DEBUG=1.")
    # Chave efemera apenas para desenvolvimento; use a variavel para persistir sessoes.
    SECRET_KEY = get_random_secret_key()

ALLOWED_HOSTS = [
    host.strip() for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS", "127.0.0.1,127.0.0.2,127.0.0.3,localhost"
    ).split(",") if host.strip()
]
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 0 if DEBUG else 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps do projeto
    "accounts.apps.AccountsConfig",
    "portal",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS.append("django_browser_reload")
    MIDDLEWARE.insert(3, "django_browser_reload.middleware.BrowserReloadMiddleware")

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # IMPORTANT
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.static",
                "django.template.context_processors.csrf",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "portal.context_processors.role_context",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"

# Database (MVP: SQLite local)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# âœ… usa a pasta /static que vocÃª vai criar agora
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 🔐 SESSION ISOLATION BY PORT
# Cada porta (8000, 8001, 8002) tem sua própria sessão.
# Isso permite que Admin, Solicitante e Projetista tenham usuários logados diferentes,
# mesmo quando o navegador usa o mesmo host (ex.: 127.0.0.1).
def _detect_port():
    # Permite definir a porta via variável de ambiente (mais confiável em scripts).
    env_port = os.environ.get("DJANGO_PORT")
    if env_port:
        return env_port

    # Padrão do Django: manage.py runserver [addrport]
    try:
        idx = sys.argv.index("runserver")
        if idx + 1 < len(sys.argv):
            candidate = sys.argv[idx + 1]
            m = re.search(r":(?P<port>\d+)$", candidate)
            if m:
                return m.group("port")
            if candidate.isdigit():
                return candidate
    except ValueError:
        pass

    # Fallback: procura algo que pareça uma porta nos argumentos
    for arg in sys.argv:
        m = re.search(r":(?P<port>\d+)$", arg)
        if m:
            return m.group("port")
        if arg.isdigit():
            return arg

    return None


port = _detect_port()

# Define o nome do cookie de sessão baseado na porta
if port == "8000":
    SESSION_COOKIE_NAME = "sessionid_admin"
    CSRF_COOKIE_NAME = "csrftoken_admin"
elif port == "8001":
    SESSION_COOKIE_NAME = "sessionid_solicitante"
    CSRF_COOKIE_NAME = "csrftoken_solicitante"
elif port == "8002":
    SESSION_COOKIE_NAME = "sessionid_projetista"
    CSRF_COOKIE_NAME = "csrftoken_projetista"
else:
    SESSION_COOKIE_NAME = "sessionid_default"
    CSRF_COOKIE_NAME = "csrftoken_default"

# Auth redirects
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "portal_redirect"
LOGOUT_REDIRECT_URL = "login"


