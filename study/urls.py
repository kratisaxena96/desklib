from django.urls import path
from .views import StudyPageView
from .views import autocomplete,CustomSearchView

urlpatterns = [
    path('search/', CustomSearchView.as_view(), name='search-results'),
    path(r'autocomplete/', autocomplete, name='autocomplete'),
    # path('<slug:slug>/', StudyPageView.as_view(), name='study-detail'),
    path('', StudyPageView.as_view(), name='study-search')
]