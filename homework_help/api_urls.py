from django.urls import path

from homework_help.api_views import QuestionCreateApiView, CommentCreateApiView, QuestionFileCreateApiView

urlpatterns = [
    path('create-question/', QuestionCreateApiView.as_view(), name='question-create-api'),
    path('create-question-file/', QuestionFileCreateApiView.as_view(), name='question-file-create-api'),
    path('create/<order_id>/', CommentCreateApiView.as_view(), name='comment-create-api'),

]