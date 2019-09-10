from django.urls import path
from .api_views import CreateSampleApiView

urlpatterns = [
    path('create/', CreateSampleApiView.as_view(), name='create-sample-api'),

]