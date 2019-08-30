from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from storages.utils import setting


from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin


class CustomStaticRootS3BotoStorage(S3Boto3Storage):
    location = 'static'


class CustomUploadsRootS3BotoStorage(S3Boto3Storage):
    location = 'media'

# StaticRootS3BotoStorage = lambda: CustomS3Boto3Storage(location='desklib/static')
# MediaRootS3BotoStorage = lambda: S3Boto3Storage(location='desklib/media')


