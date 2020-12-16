from django.urls import path
from .api_views import DocumentCreateApiView, ReportDocumentApi, DocumentFeedbackApi, UploadDocumentApi, UploadForDocumentApiView

urlpatterns = [
    path('dastavej/srijan/api/', DocumentCreateApiView.as_view(), name='document-create-api'),
    path('report-document-api/', ReportDocumentApi.as_view(), name='report-document-api'),
    path('document-feedback-api/<slug:slug>/', DocumentFeedbackApi.as_view(), name='document-feedback-api'),
    path('upload-document/', UploadDocumentApi.as_view(), name='document-upload-api'),
    path('upload-for-document/', UploadForDocumentApiView.as_view(), name='document-for-upload-api'),


]