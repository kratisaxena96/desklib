
from django.urls import path
from .views import (
    OrderDetailView,
    AskQuestionView,
    QuestionDetailView,
    OrderCreateView,
    OrderListView,
    CustomSearchQuestionView,
    autocomplete,
    HomeworkHelpPaypalPaymentView,
    HomeworkHelpPaypalPaymentCheckView,
    ParentSubjectQuestionView,
    OrdersPayment,
    PaypalOrderPaymentCheckView,
    PaypalOrderPaymentUpdateView, EmailerView
)

urlpatterns = [
    path('order_added/', EmailerView.as_view(), name='emailer'),
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
    path('order/payment/<uid>/', OrdersPayment.as_view(), name='order_payment'),
    path('payment/check', PaypalOrderPaymentCheckView.as_view(), name='payment-check'),
    path('payment/update', PaypalOrderPaymentUpdateView.as_view(), name='payment-update'),
]
