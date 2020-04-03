from django.urls import path

from homework_help.api_views import QuestionCreateApiView, CommentCreateApiView, QuestionFileCreateApiView, \
    OrderStatusApi, GetAnswerApiView

urlpatterns = [
    path('create-question/', QuestionCreateApiView.as_view(), name='question-create-api'),
    path('create-question-file/', QuestionFileCreateApiView.as_view(), name='question-file-create-api'),
    path('create/<order_id>/', CommentCreateApiView.as_view(), name='comment-create-api'),
    path('get-answer/<uid>/', GetAnswerApiView.as_view(), name='get-answer-api'),
    path('<uuid>/', OrderStatusApi.as_view(), name='order-status-api'),

]