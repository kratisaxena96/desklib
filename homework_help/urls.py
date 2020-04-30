from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from .views import OrderDetailView, AskQuestionView, QuestionDetailView, OrderCreateView, OrderListView, \
    CustomSearchQuestionView, autocomplete
from django.views.generic import TemplateView
# from .sitemaps import all_sitemaps as sitemaps


urlpatterns = [
    path('', AskQuestionView.as_view(), name='ask-question-view'),
    path('question/<slug>/', QuestionDetailView.as_view(), name='question-detail-view'),
    path('order-create/<uid>/', OrderCreateView.as_view(), name='order-create-view'),
    path('order/', OrderListView.as_view(), name='order-list-view'),
    path('order/<uuid>/', OrderDetailView.as_view(), name='order-detail-view'),
    path('search/', CustomSearchQuestionView.as_view(), name='search-question'),
    path(r'autocomplete/', autocomplete, name='autocomplete'),

]
