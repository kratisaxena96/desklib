
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ReviewPageView, AddReviewPageView

urlpatterns = [
    path('', ReviewPageView.as_view(), name="review"),
    path('add/', AddReviewPageView.as_view(), name="add_review"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)