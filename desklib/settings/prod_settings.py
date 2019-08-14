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
# Application definition



# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
MIDDLEWARE += [
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',

]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'desklib_dev_db',
        'USER': 'root',
        'PASSWORD': 'locus123',
    }
}
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = False

# Actual Parameter to be filled as provided by google for your domain
# RECAPTCHA_PUBLIC_KEY = 'MyRecaptchaKey123'
# RECAPTCHA_PRIVATE_KEY = 'MyRecaptchaPrivateKey456'

EMAIL_HOST_USER = 'siddharthjhanwar7@gmail.com'
EMAIL_HOST_PASSWORD = 'fwwffwwffw'

DEFAULT_FROM_EMAIL = 'siddharthjhanwar7@gmail.com'


# DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440*4
# DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000*2
#https://sorl-thumbnail.readthedocs.io/en/latest/requirements.html kindly satisfy requirements for sorl-thumbnail.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


THUMBNAIL_DEBUG = False


# Paypal settings
PAYPAL_TEST = False