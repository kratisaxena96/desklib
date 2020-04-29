from django.urls import path

from contact.api_views import QueryCreateApiView

urlpatterns = [
    path('create-query/', QueryCreateApiView.as_view(), name='query-create-api'),

]