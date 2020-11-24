from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf.urls import url
from .views import DocumentView, DocumentDownloadView, DownloadSuccessView, PageViewsFinishView, \
    DocumentDownloadDetailView, DocumentPayment, PaypalDocumentRedirect, PaypalPaymentView, PaypalPaymentCheckView, DocumentSearchDescription
from django.views.generic import TemplateView
# from .sitemaps import all_sitemaps as sitemaps


urlpatterns = [
    path('download/confirm/', DocumentDownloadDetailView.as_view(), name='download-info-view'),
    # path('download/', DocumentDownloadView.as_view(url='https://desklib.com/?doc=%(slug)&pay=%(single)'), name='document-download-view'),
    path('document-search/', DocumentSearchDescription.as_view(), name='document-search-view'),
    path('download/', DocumentDownloadView.as_view(url='https://desklib.com/?doc=%(slug)'), name='document-download-view'),
    path('download/success', DownloadSuccessView.as_view(), name='download-success-view'),
    path('extend/subscription', PageViewsFinishView.as_view(), name='pageviews-finish-view'),
    path('paypal/payment-check/', PaypalPaymentCheckView.as_view(), name='payment-check'),
    path('paypal/validate/', PaypalPaymentView.as_view(), name='payment-validate'),
    path('paypal/redirect/<slug:slug>', PaypalDocumentRedirect.as_view(), name='document-redirect'),
    path('payment/', DocumentPayment.as_view(), name='document-pay'),
    path('<slug:slug>/', DocumentView.as_view(), name='document-view'),
]

