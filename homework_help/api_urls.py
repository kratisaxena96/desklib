from django.urls import path
from homework_help.api_views import CommentCreateApiView

urlpatterns = [
    path('create/<order_id>/', CommentCreateApiView.as_view(), name='document-create-api'),

]