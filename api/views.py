import sys
import tempfile
from pathlib import Path

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Assessment, Comparison
from .serializers import AssessmentSerializer, ComparisonSerializer

# Make smart_extract importable from scripts/
_SCRIPTS_DIR = str(Path(__file__).parent.parent / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import smart_extract  # noqa: E402


class LatestAssessments(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AssessmentSerializer
    queryset = Assessment.objects.order_by("-created_at")[:20]


class ComparisonList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ComparisonSerializer
    queryset = Comparison.objects.order_by("-created_at")


class ExtractView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        suffix = Path(uploaded_file.name).suffix.lower()
        if suffix not in smart_extract.VALID_EXTENSIONS:
            return Response(
                {
                    "error": (
                        f"Unsupported file type '{suffix}'. "
                        "Supported: PDF (.pdf), images (PNG/JPG/WEBP/etc), or text (.txt)."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        building_type = request.data.get("building_type") or None
        if building_type and building_type not in ("housing", "commercial"):
            building_type = None

        model = request.data.get("model") or "gpt-4.1"

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp_path = Path(tmp.name)

            md_content, result = smart_extract.run_extraction(
                input_path=tmp_path,
                building_type=building_type,
                model=model,
                source_name=uploaded_file.name,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            if tmp_path and tmp_path.exists():
                tmp_path.unlink()

        return Response({"markdown": md_content, "result": result})


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
