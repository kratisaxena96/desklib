from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from .views import MyProfileView
# from .sitemaps import all_sitemaps as sitemaps
from uploads.views import UploadDocumentView,MyUploads



urlpatterns = [
    path('', include('allauth.urls')),
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),
    path('upload-file/', UploadDocumentView.as_view(), name='upload-file'),
    path('my-uploads/', MyUploads.as_view(), name='my-uploads')

    # path('my-uploads/', MyUploadsView.as_view(), name='my-uploads')
]
