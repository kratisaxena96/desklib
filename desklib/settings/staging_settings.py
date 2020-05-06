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

ALLOWED_HOSTS = ['.68.183.89.118']
DEBUG = False
ADMINS = [('Rishi', 'rishi.dutta@zucolservices.com')]

ALLOWED_IPS = ['68.183.89.118']

META_USE_TITLE_TAG = True

#INSTALLED_APPS += [
#    'haystack',
#]


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
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
    }
}
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = False

# Actual Parameter to be filled as provided by google for your domain
# RECAPTCHA_PUBLIC_KEY = 'MyRecaptchaKey123'
# RECAPTCHA_PRIVATE_KEY = 'MyRecaptchaPrivateKey456'

EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']


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
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}



# # Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'propagate': True,
#             'level': 'INFO'
#         },
#         'chat': {
#             'handlers': ['console'],
#             'propagate': False,
#             'level': 'DEBUG',
#         },
#     },
# }


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }


THUMBNAIL_DEBUG = False


# Paypal settings
PAYPAL_TEST = True

RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

DEFAULT_FILE_STORAGE = 'desklib.storages.CustomUploadsRootS3BotoStorage'
STATICFILES_STORAGE = 'desklib.storages.CustomStaticRootS3BotoStorage'
# storage
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_S3_REGION_NAME = os.environ['AWS_S3_REGION_NAME']
# AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
# AWS_S3_ENDPOINT_URL = 'https://%s.digitaloceanspaces.com' % AWS_S3_REGION_NAME
#AWS_LOCATION = 'static'
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

#STATIC_URL = '%s/%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME,  STATICFILES_LOCATION)
#STATIC_URL = 'https://desklib.com/static/'
AWS_S3_CUSTOM_DOMAIN = 'desklib.com'

AWS_S3_SECURE_URLS = True
FLAG_MAIL_TO_TEST = True
#AWS_HEADERS = {
#   'Expires': 'Thu, 25 Nov 2016 21:00:00 GMT',
#    'Cache-Control': 'max-age=94608000',
#}

AWS_QUERYSTRING_AUTH = False
