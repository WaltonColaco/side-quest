from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import LatestAssessments, ComparisonList, FeatureFlagsView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/assessments/", LatestAssessments.as_view(), name="assessments"),
    path("api/comparisons/", ComparisonList.as_view(), name="comparisons"),
    path("api/features/", FeatureFlagsView.as_view(), name="features"),
]
