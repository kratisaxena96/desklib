from django.urls import path
from homework_help.api_views import CommentCreateApiView

urlpatterns = [
    path('create/', CommentCreateApiView.as_view(), name='document-create-api'),

]