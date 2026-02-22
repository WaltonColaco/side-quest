from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import (
    LatestAssessments,
    ComparisonList,
    ExtractView,
    FeatureFlagsView,
    GeocodeSearchView,
    LocationView,
    LocationDetailView,
    RegisterView,
    MeView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/me/", MeView.as_view(), name="me"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/assessments/", LatestAssessments.as_view(), name="assessments"),
    path("api/comparisons/", ComparisonList.as_view(), name="comparisons"),
    path("api/extract/", ExtractView.as_view(), name="extract"),
    path("api/features/", FeatureFlagsView.as_view(), name="features"),
    path("api/geocode/", GeocodeSearchView.as_view(), name="geocode"),
    path("api/location/detail/", LocationDetailView.as_view(), name="location-detail"),
    path("api/location/", LocationView.as_view(), name="location"),
]
