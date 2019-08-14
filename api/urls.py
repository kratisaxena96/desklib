from django.urls import path, include
from api.views import DocumentCreateApiView, CreateSampleApiView, ReportDocumentApi, DocumentFeedbackApi

urlpatterns = [
    path('create/document', DocumentCreateApiView.as_view(), name='document-create-api'),
    path('create/sample/', CreateSampleApiView.as_view(), name='create-sample-api'),
    path('report-document-api/', ReportDocumentApi.as_view(), name='report-document-api'),
    path('document-feedback-api/<slug:slug>/', DocumentFeedbackApi.as_view(), name='document-feedback-api'),

]