from django.urls import path, include
from .views import DocumentView




urlpatterns = [
    path('<slug:slug>/', DocumentView.as_view(), name='document-view'),
]