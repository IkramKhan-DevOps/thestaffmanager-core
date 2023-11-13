import os
from pathlib import Path
import environ

""" __ BASE CONFIGURATIONS __"""
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, True)
)
environ.Env.read_env(BASE_DIR / '.env')

""" __ CORE CONFIGURATIONS __"""
DEBUG = bool(env('DEBUG'))
SECRET_KEY = env('SECRET_KEY')
ENVIRONMENT = env('ENVIRONMENT')

SITE_ID = 1
DOMAIN = env('DOMAIN')
PROTOCOL = env('PROTOCOL')
ROOT_URLCONF = 'core.urls'
BASE_URL = f"{PROTOCOL}://{DOMAIN}"
ALLOWED_HOSTS = str(env('ALLOWED_HOSTS')).split(',')
CSRF_TRUSTED_ORIGINS = [f'{PROTOCOL}://{host}' for host in ALLOWED_HOSTS]
GOOGLE_CALLBACK_ADDRESS = f"{BASE_URL}/accounts/google/login/callback/"

AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/accounts/cross-auth/'
LOGOUT_REDIRECT_URL = '/accounts/cross-auth/'
WSGI_APPLICATION = 'core.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

FIXTURE_DIRS = ['fixtures']

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
    'crispy_bootstrap5',
    'ckeditor',
    'rest_framework',
    'colorfield',
    'widget_tweaks',

    # SYSTEM APPS
    'src.accounts',
    'src.administration.employees',
    'src.administration.admins',

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
            'ENGINE': 'django.db.backends.postgresql',
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

""" INTERNATIONALIZATION --------------------------------------------------------------------------------"""
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" EMAIL CONFIGURATION --------------------------------------------------------------------------------"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "donald.duck0762@gmail.com"
EMAIL_HOST_PASSWORD = "cikghsgphicaptqj"
EMAIL_PORT = "587"
DEFAULT_FROM_EMAIL = 'support@exarth.com'

# EMAIL_BACKEND = 'django_ses.SESBackend'
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')  # AKIAVALBCDPOQMNWPVVZ
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')  # 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
AWS_SES_REGION_NAME = 'eu-west-2'
AWS_SES_REGION_ENDPOINT = 'email.eu-west-2.amazonaws.com'

""" RESIZER IMAGE --------------------------------------------------------------------------------"""
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR / 'assets'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

""" RESIZER IMAGE --------------------------------------------------------------------------------"""
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {
    'JPEG': ".jpg",
    'PNG': ".png",
    'GIF': ".gif"
}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

""" __ ALL AUTH CONFIGURATIONS ------------------------------------------------------------------ """
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

""" DEBUGGING TOOLS ----------------------------------------------------------------------------- """

if ENVIRONMENT != 'server':
    INSTALLED_APPS += [
        'django_browser_reload'
    ]
    MIDDLEWARE += [
        'django_browser_reload.middleware.BrowserReloadMiddleware'
    ]
