from rest_framework import generics, permissions

from .models import Assessment, Comparison
from .serializers import AssessmentSerializer, ComparisonSerializer


class LatestAssessments(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AssessmentSerializer
    queryset = Assessment.objects.order_by("-created_at")[:20]


class ComparisonList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ComparisonSerializer
    queryset = Comparison.objects.order_by("-created_at")
