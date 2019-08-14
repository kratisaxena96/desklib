from django.urls import path, include
from api.views import DocumentCreateApiView

urlpatterns = [
    path('create/document', DocumentCreateApiView.as_view(), name='document-create-api'),

]