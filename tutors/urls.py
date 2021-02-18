from django.urls import path
from .views import TutorPlanPageView, TutorListPageView, TutorDetailPageView, TutorPageView

urlpatterns = [
    path('tutor-list/', TutorListPageView.as_view(), name='tutor-list'),
    path('tutor-detail/<slug>/$', TutorDetailPageView.as_view(), name='tutor-detail'),
    path('tutor-plans/', TutorPlanPageView.as_view(), name='tutor-plans'),
    path('', TutorPageView.as_view(), name='tutor')
    # path('<slug:slug>/', StudyPageView.as_view(), name='study-detail'),
]
