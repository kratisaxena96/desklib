from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from .views import OrderDetailView, AskQuestionView, QuestionDetailView, OrderCreateView
from django.views.generic import TemplateView
# from .sitemaps import all_sitemaps as sitemaps


urlpatterns = [
    path('ask-question/', AskQuestionView.as_view(), name='ask-question-view'),
    path('order/', OrderCreateView.as_view(), name='order-create-view'),
    path('question/<slug>', QuestionDetailView.as_view(), name='question-detail-view'),
    path('<order_id>/', OrderDetailView.as_view(), name='order-detail-view'),
]
