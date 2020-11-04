"""
Django settings for desklib project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from desklib.settings.base import *
from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('ro', _('Romanian')),
)
# Application definition
FLAG_MAIL_TO_TEST = True

INSTALLED_APPS += [
    'debug_toolbar',
    # 'djcelery',
    # 'admissions',
    'formtools',
    # 'homework',
    # 'channels',
    # 'django_celery_results',
    # 'kombu.transport.django'
]

ALLOWED_IPS = ['127.0.0.1']
CELERY_RESULT_BACKEND = 'django-db'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'desklib_dev_db',
        'USER': 'root',
        'PASSWORD': 'locus123',
    }
}
# EXPECTED_IP_API = ['192.168.1.1','127.0.0.1']
#Commented out in production envirment
# SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

EMAIL_HOST_USER = 'vishakha.sharma@locusrags.com'
EMAIL_HOST_PASSWORD = 'vishakhalocus7@4'

DEFAULT_FROM_EMAIL = 'vishakha.sharma@locusrags.com'

# DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440*4
# DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000*2
#https://sorl-thumbnail.readthedocs.io/en/latest/requirements.html kindly satisfy requirements for sorl-thumbnail.
# Channels
# ASGI_APPLICATION = 'desklib.routing.application'
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6379)],
#         },
#     },
# }

THUMBNAIL_DEBUG = True
MIDDLEWARE += [
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = False

# Paypal settings
PAYPAL_TEST = True
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 6
META_USE_TITLE_TAG = True

RECAPTCHA_PUBLIC_KEY= "6LeT_rYUAAAAACn413JJTLeX6FJShA3sCK3Tc5b4"
RECAPTCHA_PRIVATE_KEY = "6LeT_rYUAAAAADYzTg-nkVC3eRv5KBUrbRPTkkxZ"

# ASGI_APPLICATION = "desklib.routing.application"

PAYPAL_CLIENT = "Aei6_cYX5hfSF0WsVXJ3VR3Rc_C0KbneVwh3RLYx_OUJG3gS5m2XM-1tg9EFL7ffTjggfvaNhKQQnsyE"
PAYPAL_SECRET = "EDVPo6BKm3W20QSivNv8IsZSxExWw71RC99Vvb_uN4xCmI7QFkTuHJ6g_YCX9lMIKfpx7-rs_upjOFmw"

PAYPAL_TOKEN_API = "https://api.sandbox.paypal.com/v1/oauth2/token"
PAYPAL_CHECKOUT_API = "https://api.sandbox.paypal.com/v2/checkout/orders"
PAYPAL_RISK_API = "https://api.sandbox.paypal.com/v1/risk/transaction-contexts/"
PAYPAL_MERCHANT_ID = "BL4F4UGTX2VCW"
