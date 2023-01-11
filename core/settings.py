import os
from pathlib import Path
import environ

""" __ BASE CONFIGURATIONS __"""
env = environ.Env(
    DEBUG=(bool, False)
)
MAINTENANCE = False
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
BASE_URL = env('BASE_URL')

""" __ CORE CONFIGURATIONS __"""
DEBUG = bool(env('DEBUG'))
SECRET_KEY = env('SECRET_KEY')
ENVIRONMENT = env('ENVIRONMENT')
AUTH_USER_MODEL = 'accounts.User'
ALLOWED_HOSTS = ['*']
WSGI_APPLICATION = 'core.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

""" __ Application definition __ """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # AUTH
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # REQUIRED APPLICATIONS
    'django_filters',
    'crispy_forms',
    'ckeditor',
    'rest_framework',
    'colorfield',
    'widget_tweaks',

    # SYSTEM APPS
    'src.accounts',
    'src.administration.employees',
    'src.administration.admins',
    'src.website',

    # NOTIFICATIONS APPS
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

if ENVIRONMENT == 'server':
    DATABASES = {
        'default': {
            'ENGINE': env('DB_ENGINE'),
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASS'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
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

""" __ TIME ZONE CONFIGURATIONS __ """
LANGUAGE_CODE = 'en-us'
TIME_ZONE = env("TIME_ZONE")
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" __ STATIC AND MEDIA CONFIGURATIONS __ """
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

""" __ TEMPLATES AND THEMES CONFIGURATIONS __ """
CRISPY_TEMPLATE_PACK = 'bootstrap4'

""" __ TIME ZONE CONFIGURATIONS __ """

""" __ EMAIL AND SMTP CONFIGURATIONS __ """
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
DEFAULT_FROM_EMAIL = "Support-Team <support@thestaffmanager.com>"

""" __ ACCOUNTS CONFIGURATIONS __ """
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

""" __ ALL AUTH CONFIGURATIONS __ """
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

""" APP """
SYS_VERIFICATION_EMAILS = env('SYS_VERIFICATION_EMAILS')
