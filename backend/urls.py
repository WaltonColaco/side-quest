from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import (
    LatestAssessments,
    ComparisonList,
    ExtractView,
    FeatureFlagsView,
    GeocodeSearchView,
    LocationView, LocationSaveView, MyLocationsView,
    LocationDetailView,
    LocationReportDownloadView,
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
    path("api/location/save/", LocationSaveView.as_view(), name="location-save"),
    path("api/location/mine/", MyLocationsView.as_view(), name="location-mine"),
    path("api/geocode/", GeocodeSearchView.as_view(), name="geocode"),
    path("api/location/detail/", LocationDetailView.as_view(), name="location-detail"),
    path("api/location/download/", LocationReportDownloadView.as_view(), name="location-download"),
    path("api/location/", LocationView.as_view(), name="location"),
]
