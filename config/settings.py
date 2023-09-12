from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default=get_random_secret_key())
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'apps.api.apps.ApiConfig',
    'apps.core.apps.CoreConfig',
    'apps.users.apps.UsersConfig',
    'apps.clients.apps.ClientsConfig',
    'apps.session.apps.SessionConfig',
    'apps.psychologists.apps.PsychologistsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

AUTH_USER_MODEL = 'users.CustomUser'

SIMPLE_JWT = {
   'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
   'AUTH_HEADER_TYPES': ('JWT',),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

HIDE_USERS = True
ACTIVATION_URL = 'auth/verify-email/{uid}/{token}'
PASSWORD_RESET_CONFIRM_URL = 'auth/reset-password/{uid}/{token}'
SEND_ACTIVATION_EMAIL = True
SEND_CONFIRMATION_EMAIL = True
PASSWORD_CHANGED_EMAIL_CONFIRMATION = True
LOGOUT_ON_PASSWORD_CHANGE = False
CREATE_SESSION_ON_LOGIN = True

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', default='django.core.mail.backends.filebased.EmailBackend')

# Settings for filebased.EmailBackend
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
EMAIL_SENDER = 'share.with.me-help@yandex.ru'

# Settings for smtp.EmailBackend
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', default='True') == 'True'
EMAIL_HOST = os.getenv('EMAIL_HOST', default='email_host')
EMAIL_PORT = os.getenv('EMAIL_PORT', default=587)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', default=EMAIL_SENDER)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', default='email_pass')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER', default=EMAIL_SENDER)
