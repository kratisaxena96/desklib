"""
Django settings for desklib project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.conf import global_settings
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__) + "/.."))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
print(BASE_DIR)
print(PROJECT_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=+8ji%nhjimtp+_4!bwfv!$hn92)jwnk7lr$sl+%wsrgmfq%ou'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', "*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    # 'accounts.apps.AccountsConfig',
    'django.contrib.humanize',
    'haystack',
    'desklib',
    'accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'taggit',
    'user_sessions',
    'ckeditor',
    'ckeditor_uploader',
    'documents',
    'meta',
    'django_json_ld',
    'subjects',
    'writing',
    'captcha',
    'subscription',
    'post_office',
    'phonenumber_field',
    'robots',
    'sorl.thumbnail',
    'study',
    'paypal.standard.ipn',
    'rest_framework',
    'samples',
    'api',
    'django.contrib.admindocs',
    # 'channels',
    'uploads',
    'storages',
    'django_countries',
    'review',
    'admissions',
    'homework_help',
    # 'djadyen',
]

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True,
SOCIALACCOUNT_QUERY_EMAIL=ACCOUNT_EMAIL_REQUIRED,
SOCIALACCOUNT_EMAIL_REQUIRED=ACCOUNT_EMAIL_REQUIRED,
SOCIALACCOUNT_STORE_TOKENS=False
EXPECTED_IP_API = ['192.168.1.1','127.0.0.1']

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12',
    },
     'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'desklib.middleware.IpRestrict',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'desklib.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'desklib.context_processor.from_settings',
                'desklib.context_preprocessor.get_subjects',
                # 'allauth.account.context_processors.account',
                # 'allauth.socialaccount.context_processors.socialaccount',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# EMAIL_BACKEND = 'post_office.EmailBackend'
# EMAIL_BACKEND = "mailer.backend.DbBackend"


# POST_OFFICE = {
#     'DEFAULT_PRIORITY': 'now'
#     }

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of 'allauth'
    'django.contrib.auth.backends.ModelBackend',

    # 'allauth' specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'desklib.wsgi.application'
#Djano Meta Browse more properties on https://django-meta.readthedocs.io/en/latest/settings.html
META_SITE_PROTOCOL = '.'
META_SITE_DOMAIN = '.'
META_USE_TWITTER_PROPERTIES = True

JSON_LD_INVALID_SD = 'throw'



# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

global_settings.TIME_INPUT_FORMATS = [
    '%H:%M:%S',
]



LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': 'localhost:9200',
        'TIMEOUT': 60 * 5,
        'INDEX_NAME': 'haystack_new',
        'INCLUDE_SPELLING': True,
    },
}

# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
# ACCOUNT_USER_DISPLAY = ''
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USERNAME_MIN_LENGTH = 2
ACCOUNT_LOGOUT_ON_GET = True

AUTH_USER_MODEL = 'accounts.UserAccount'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

TAGGIT_CASE_INSENSITIVE = True

GECKO_DRIVER_URL = os.path.join(BASE_DIR, 'geckodriver')
GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

ACCOUNT_FORMS = {
# 'signup': 'accounts.forms.CustomSignupForm',
'login': 'accounts.forms.CustomLoginForm',
}

ACCOUNT_SIGNUP_FORM_CLASS = 'accounts.forms.CustomSignupForm'


HAYSTACK_DEFAULT_OPERATOR = 'AND'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587



#Setr
# ROBOTS_USE_SITEMAP = False
ROBOTS_USE_SCHEME_IN_HOST = True
ROBOTS_SITEMAP_URLS = [
    'http://desklib.com/sitemap.xml',
]
ROBOTS_CACHE_TIMEOUT = 60*60*24
ROBOTS_SITEMAP_VIEW_NAME = 'cached-sitemap'
ROBOTS_USE_SCHEME_IN_HOST = True



# for chaced db run command "python manage.py createcachetable" for first time sorl-thumbnail required it
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'my_table',
    }
}


# DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440*4
# DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000*2
#https://sorl-thumbnail.readthedocs.io/en/latest/requirements.html kindly satisfy requirements for sorl-thumbnail.

ASGI_APPLICATION = 'desklib.routing.application'

COMING_SOON = False

CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_JQUERY_URL = 'http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_ALLOW_NONIMAGE_FILES = False


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
#         'width': 600,
    },
    'extraPlugins': ','.join([
            'autolink', 'dialog',
            'codesnippet','autogrow','placeholder',
    ]),
}

