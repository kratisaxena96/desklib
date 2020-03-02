from django.urls import path

from homework_help.api_view import QuestionCreateApiView, CommentCreateApiView

urlpatterns = [
    path('create-question/', QuestionCreateApiView.as_view(), name='question-create-api'),
    path('create/<order_id>/', CommentCreateApiView.as_view(), name='document-create-api'),

]