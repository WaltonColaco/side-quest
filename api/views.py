from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from pathlib import Path

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


class FeatureFlagsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        root = Path(__file__).resolve().parent.parent
        extracted_dir = root / "extracted_output"
        ramp_keywords = ("ramp", "ramps", "sloped floor")
        power_keywords = ("power door", "automatic door", "door operator")
        elevator_keywords = ("elevator", "lift", "platform lift")

        ramp = power = elevator = False
        if extracted_dir.exists():
            for md in extracted_dir.glob("*.md"):
                text = md.read_text(encoding="utf-8", errors="ignore").lower()
                if any(k in text for k in ramp_keywords):
                    ramp = True
                if any(k in text for k in power_keywords):
                    power = True
                if any(k in text for k in elevator_keywords):
                    elevator = True
        return Response({"ramp": ramp, "powerDoors": power, "elevator": elevator})
