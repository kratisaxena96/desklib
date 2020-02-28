from django.urls import path, include

urlpatterns = [
    path('document/', include(('documents.api_urls', 'documents'), namespace="documents-api")),
    path('sample/', include(('samples.api_urls', 'samples'), namespace="sample-api")),
    path('homework-help/', include(('homework_help.api_urls', 'homework_help'), namespace="homework-help-api")),

]
