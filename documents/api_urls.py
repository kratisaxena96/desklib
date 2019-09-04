from django.urls import path
from .api_views import DocumentCreateApiView, ReportDocumentApi, DocumentFeedbackApi

urlpatterns = [
    path('create/document/', DocumentCreateApiView.as_view(), name='document-create-api'),
    path('report-document-api/', ReportDocumentApi.as_view(), name='report-document-api'),
    path('document-feedback-api/<slug:slug>/', DocumentFeedbackApi.as_view(), name='document-feedback-api'),

]