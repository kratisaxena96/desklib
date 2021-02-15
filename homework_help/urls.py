from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from .views import OrderDetailView, AskQuestionView, QuestionDetailView, OrderCreateView, OrderListView, \
    CustomSearchQuestionView, autocomplete, HomeworkHelpPaypalPaymentView, HomeworkHelpPaypalPaymentCheckView, ParentSubjectQuestionView
from django.views.generic import TemplateView
# from .sitemaps import all_sitemaps as sitemaps


urlpatterns = [
    path('', AskQuestionView.as_view(), name='ask-question-view'),
    path('question/<slug>/', QuestionDetailView.as_view(), name='question-detail-view'),
    path('paypal/check-payment/', HomeworkHelpPaypalPaymentCheckView.as_view(), name='homework-help-check'),
    path('paypal/validate/', HomeworkHelpPaypalPaymentView.as_view(), name='homework-help-payment-validate'),
    path('order-create/<uid>/', OrderCreateView.as_view(), name='order-create-view'),
    path('order/', OrderListView.as_view(), name='order-list-view'),
    path('order/<uuid>/', OrderDetailView.as_view(), name='order-detail-view'),
    path('search/', CustomSearchQuestionView.as_view(), name='search-question'),
    path(r'autocomplete/', autocomplete, name='autocomplete'),
    path('<slug:slug>/', ParentSubjectQuestionView.as_view(), name='parent-question-view'),

]
