import sys
import tempfile
from pathlib import Path
import re
import sqlite3
import subprocess

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
import httpx

from .models import Assessment, Comparison, Location, ChunkMatch
from .serializers import (
    AssessmentSerializer,
    ComparisonSerializer,
    LocationSerializer,
)

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

        # Parse coordinates/address and persist to locations table
        coord_re = re.compile(r"([-+]?\d+\.\d+)\s*,\s*([-+]?\d+\.\d+)")
        address = None
        lat = lng = None
        lines = [line.strip() for line in md_content.splitlines()]
        for i, line in enumerate(lines):
            if line.lower().startswith("location"):
                for nxt in lines[i + 1 : i + 5]:
                    if nxt:
                        address = nxt
                        break
                break
        match = coord_re.search(md_content)
        if match:
            lat, lng = match.groups()
            lat, lng = float(lat), float(lng)
            db_path = Path(__file__).resolve().parent.parent / "db" / "assessment.db"
            con = sqlite3.connect(db_path)
            try:
                # Ensure columns exist
                for alter in (
                    "ALTER TABLE locations ADD COLUMN score REAL",
                    "ALTER TABLE locations ADD COLUMN comparison_id INTEGER",
                ):
                    try:
                        con.execute(alter)
                    except sqlite3.OperationalError:
                        pass

                cur = con.execute(
                    """
                    INSERT INTO locations (name, address, latitude, longitude, source_doc)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (address or uploaded_file.name, address, lat, lng, uploaded_file.name),
                )
                location_id = cur.lastrowid
                con.commit()
            finally:
                con.close()

            # Run vector comparison against rubric and capture score
            try:
                scripts_dir = Path(__file__).parent.parent / "scripts"
                compare_script = scripts_dir / "compare_md_vectors.py"
                rubric_housing = Path(__file__).parent.parent / "reports" / "housing.md"
                rubric_commercial = Path(__file__).parent.parent / "reports" / "commercial_interiors.md"
                db_path_arg = Path(__file__).parent.parent / "db" / "assessment.db"
                # Write the extracted markdown to a temp file for comparison
                with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tmp_md:
                    tmp_md.write(md_content.encode("utf-8"))
                    tmp_md_path = Path(tmp_md.name)
                subprocess.run(
                    [
                        sys.executable,
                        str(compare_script),
                        "--candidate",
                        str(tmp_md_path),
                        "--rubric-housing",
                        str(rubric_housing),
                        "--rubric-commercial",
                        str(rubric_commercial),
                        "--db",
                        str(db_path_arg),
                        "--model",
                        "text-embedding-3-small",
                        "--write-assessment",
                    ],
                    check=True,
                )
                # Read latest score for this temp doc path
                con = sqlite3.connect(db_path_arg)
                try:
                    cur = con.execute(
                        """
                        SELECT comparisons.id, comparisons.overall_score
                        FROM comparisons
                        JOIN documents ON documents.id = comparisons.candidate_document_id
                        WHERE documents.path = ?
                        ORDER BY comparisons.id DESC
                        LIMIT 1
                        """,
                        (str(tmp_md_path),),
                    )
                    row = cur.fetchone()
                    if row:
                        comp_id, score = row
                        con.execute(
                            "UPDATE locations SET score = ?, comparison_id = ? WHERE id = ?",
                            (score, comp_id, location_id),
                        )
                        con.commit()
                finally:
                    con.close()
                tmp_md_path.unlink(missing_ok=True)
            except Exception as e:
                # Don't fail extraction if scoring fails; just return without score.
                print(f"[extract] compare scoring failed: {e}", file=sys.stderr)

        return Response(
            {
                "markdown": md_content,
                "result": result,
                "lat": lat,
                "lng": lng,
                "address": address,
            }
        )


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


class LocationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = Location.objects.all().order_by("-created_at")
        serializer = LocationSerializer(qs, many=True)
        return Response(serializer.data)


class LocationDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        loc = Location.objects.order_by("-created_at").first()
        if not loc:
            return Response({"detail": "No locations"}, status=404)

        # If no address stored, reverse geocode from coords
        if not loc.address and loc.latitude and loc.longitude:
            try:
                url = (
                    "https://nominatim.openstreetmap.org/reverse"
                    f"?format=jsonv2&lat={loc.latitude}&lon={loc.longitude}"
                )
                resp = httpx.get(url, headers={"User-Agent": "side-quest/1.0"}, timeout=6)
                if resp.status_code == 200:
                    data = resp.json()
                    display_name = data.get("display_name")
                    if display_name:
                        loc.address = display_name
            except Exception:
                pass

        passes = []
        fails = []
        if loc.comparison_id:
            matches = (
                ChunkMatch.objects.filter(comparison_id=loc.comparison_id)
                .order_by("-similarity")
                .values("status", "similarity", "rubric_path", "rubric_excerpt")
            )
            for m in matches:
                label = m["rubric_excerpt"] or m["rubric_path"]
                if label and "desc:" in label:
                    label = label.split("desc:", 1)[1]
                if label and "- values" in label:
                    label = label.split("- values", 1)[0]
                if label:
                    label = label.strip(" -\n\t")
                item = {"label": label, "similarity": m["similarity"]}
                if m["status"] in ("strong", "partial") and len(passes) < 2:
                    passes.append(item)
                elif m["status"] == "missing" and len(fails) < 1:
                    fails.append(item)
                if len(passes) >= 2 and len(fails) >= 1:
                    break

        data = {
            "score": loc.score,
            "address": loc.address,
            "name": loc.name,
            "source": loc.source_doc,
            "passes": passes,
            "fails": fails,
        }
        return Response(data)
