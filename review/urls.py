
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ReviewPageView

urlpatterns = [
    path('', ReviewPageView.as_view(), name="review"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)