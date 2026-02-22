import os
import sys
import tempfile
import threading
from pathlib import Path
import re
import sqlite3
import subprocess
from urllib.parse import quote as url_quote

from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
import httpx

from .models import Assessment, Comparison, Location, ChunkMatch, UserProfile
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


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        password = request.data.get("password", "")
        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "@" not in email:
            return Response(
                {"error": "Please enter a valid email address."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=email).exists():
            return Response(
                {"error": "An account with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        name = request.data.get("name", "").strip()
        role = request.data.get("role", "").strip()
        location = request.data.get("location", "").strip()
        user = User.objects.create_user(username=email, email=email, password=password)
        if name:
            user.first_name = name
            user.save()
        UserProfile.objects.create(user=user, role=role, location=location)
        return Response({"id": user.id, "email": user.email}, status=status.HTTP_201_CREATED)


class MeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, "profile", None)
        return Response({
            "id": user.id,
            "email": user.email or user.username,
            "name": user.first_name,
            "role": profile.role if profile else "",
            "location": profile.location if profile else "",
        })


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

        # Parse coordinates/address from extracted markdown.
        # Do NOT save to DB yet — the user must confirm on LocationFound/LocationNotFound first.
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


class LocationSaveView(APIView):
    """
    POST /api/location/save/
    Called when the user confirms they want to add their audit to the public map.
    Body: { address, lat, lng, source_doc }
    If lat/lng are absent the address is geocoded via Nominatim before saving.
    Optionally authenticated: if a valid JWT is present the location is linked to that user.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        address = request.data.get("address") or None
        lat = request.data.get("lat")
        lng = request.data.get("lng")
        source_doc = request.data.get("source_doc") or "Untitled"

        # Optionally link to the authenticated user (AllowAny — anonymous uploads still work)
        user_id = None
        try:
            result = JWTAuthentication().authenticate(request)
            if result is not None:
                user_id = result[0].id
        except Exception:
            pass

        # Geocode if coordinates were not extracted from the document
        if lat is None or lng is None:
            if not address:
                return Response(
                    {"error": "Address is required when coordinates are not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            geo_lat = geo_lng = None

            # 1) Google Maps Geocoding API (primary)
            env = smart_extract.load_env(smart_extract.ENV_FILE)
            gmaps_key = env.get("GOOGLE_MAPS_API_KEY") or os.getenv("GOOGLE_MAPS_API_KEY")
            if gmaps_key:
                try:
                    gmaps_url = (
                        "https://maps.googleapis.com/maps/api/geocode/json"
                        f"?address={url_quote(address)}&key={gmaps_key}"
                    )
                    resp = httpx.get(gmaps_url, timeout=5)
                    gmaps_data = resp.json() if resp.status_code == 200 else {}
                    if gmaps_data.get("status") == "OK" and gmaps_data.get("results"):
                        loc = gmaps_data["results"][0]["geometry"]["location"]
                        geo_lat = float(loc["lat"])
                        geo_lng = float(loc["lng"])
                except Exception:
                    pass  # fall through to Nominatim

            # 2) Nominatim fallback
            if geo_lat is None:
                try:
                    nom_url = (
                        "https://nominatim.openstreetmap.org/search"
                        f"?q={url_quote(address)}&format=json&limit=1"
                    )
                    resp = httpx.get(nom_url, headers={"User-Agent": "side-quest/1.0"}, timeout=5)
                    nom_results = resp.json() if resp.status_code == 200 else []
                    if not nom_results:
                        return Response(
                            {"error": "Could not geocode the provided address. Try a more specific address."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    geo_lat = float(nom_results[0]["lat"])
                    geo_lng = float(nom_results[0]["lon"])
                except Exception as e:
                    return Response(
                        {"error": f"Geocoding failed: {e}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            lat = geo_lat
            lng = geo_lng
        else:
            lat = float(lat)
            lng = float(lng)

        root_dir = Path(__file__).resolve().parent.parent
        report_path = root_dir / "extracted_output" / f"{Path(source_doc).stem}_smart.md"
        db_path = root_dir / "db" / "assessment.db"

        con = sqlite3.connect(db_path)
        try:
            for alter in (
                "ALTER TABLE locations ADD COLUMN score REAL",
                "ALTER TABLE locations ADD COLUMN comparison_id INTEGER",
                "ALTER TABLE locations ADD COLUMN report_path TEXT",
            ):
                try:
                    con.execute(alter)
                except sqlite3.OperationalError:
                    pass

            cur = con.execute(
                """
                INSERT INTO locations (name, address, latitude, longitude, source_doc, report_path, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (address or source_doc, address, lat, lng, source_doc, str(report_path), user_id),
            )
            location_id = cur.lastrowid
            con.commit()
        finally:
            con.close()

        # Run vector comparison in a background thread so the response returns
        # immediately and the frontend doesn't time out waiting for OpenAI embeddings.
        # The location row is already committed; the score/comparison_id will be
        # written once the thread finishes (typically 30-60 s).
        def _score_in_background(report_path, db_path, root_dir, location_id):
            try:
                scripts_dir = root_dir / "scripts"
                compare_script = scripts_dir / "compare_md_vectors.py"
                rubric_housing = root_dir / "reports" / "housing.md"
                rubric_commercial = root_dir / "reports" / "commercial_interiors.md"
                subprocess.run(
                    [
                        sys.executable,
                        str(compare_script),
                        "--candidate", str(report_path),
                        "--rubric-housing", str(rubric_housing),
                        "--rubric-commercial", str(rubric_commercial),
                        "--db", str(db_path),
                        "--model", "text-embedding-3-small",
                        "--write-assessment",
                    ],
                    check=True,
                )
                con = sqlite3.connect(db_path)
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
                        (str(report_path),),
                    )
                    row = cur.fetchone()
                    if row:
                        comp_id, bg_score = row
                        con.execute(
                            "UPDATE locations SET score = ?, comparison_id = ? WHERE id = ?",
                            (bg_score, comp_id, location_id),
                        )
                        con.commit()
                finally:
                    con.close()
            except Exception as e:
                print(f"[location-save] background scoring failed: {e}", file=sys.stderr)

        threading.Thread(
            target=_score_in_background,
            args=(report_path, db_path, root_dir, location_id),
            daemon=True,
        ).start()

        return Response({"id": location_id})


class MyLocationsView(APIView):
    """
    GET /api/location/mine/
    Returns only the locations uploaded by the currently authenticated user,
    ordered newest first. Used by the Reports page.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        db_path = Path(__file__).resolve().parent.parent / "db" / "assessment.db"
        con = sqlite3.connect(db_path)
        try:
            cur = con.execute(
                """
                SELECT id, address, score, source_doc, created_at
                FROM locations
                WHERE user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id,),
            )
            rows = cur.fetchall()
        finally:
            con.close()

        data = [
            {
                "id": row[0],
                "address": row[1],
                "score": row[2],
                "source_doc": row[3],
                "created_at": row[4],
            }
            for row in rows
        ]
        return Response(data)


class LocationView(APIView):
    permission_classes = [permissions.AllowAny]

    _RAMP_KEYWORDS = ("ramp", "ramps", "sloped floor")
    _POWER_KEYWORDS = ("power door", "automatic door", "door operator")
    _ELEVATOR_KEYWORDS = ("elevator", "lift", "platform lift")

    def _scan_report(self, report_path):
        if not report_path:
            return False, False, False
        try:
            text = Path(report_path).read_text(encoding="utf-8", errors="ignore").lower()
            # Scope search to the Found Requirements section only
            parts = text.split("## found requirements", 1)
            search_text = parts[1].split("## not found", 1)[0] if len(parts) > 1 else ""
            ramp = any(k in search_text for k in self._RAMP_KEYWORDS)
            power = any(k in search_text for k in self._POWER_KEYWORDS)
            elevator = any(k in search_text for k in self._ELEVATOR_KEYWORDS)
        except Exception:
            ramp = power = elevator = False
        return ramp, power, elevator

    def get(self, request):
        qs = Location.objects.all().order_by("-created_at")
        serializer = LocationSerializer(qs, many=True)
        result = []
        for item, loc in zip(serializer.data, qs):
            ramp, power, elevator = self._scan_report(loc.report_path)
            result.append({**item, "ramp": ramp, "powerDoors": power, "elevator": elevator})
        return Response(result)


class GeocodeSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = (request.query_params.get("q") or "").strip()
        if not query:
            return Response({"detail": "Missing query parameter 'q'."}, status=400)

        q_lower = query.lower()
        has_region = "alberta" in q_lower or "canada" in q_lower
        primary_query = query if has_region else f"{query}, Alberta, Canada"
        queries = [primary_query]
        if primary_query != query:
            queries.append(query)

        try:
            first = None
            used_query = query
            for q in queries:
                resp = httpx.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={
                        "q": q,
                        "format": "jsonv2",
                        "limit": 1,
                        "addressdetails": 1,
                        "countrycodes": "ca",
                    },
                    headers={"User-Agent": "side-quest/1.0"},
                    timeout=6,
                )
                if resp.status_code != 200:
                    continue
                results = resp.json()
                if isinstance(results, list) and results:
                    first = results[0]
                    used_query = q
                    break

            if not first:
                return Response({"detail": "No results found."}, status=404)

            lat = first.get("lat")
            lon = first.get("lon")
            if lat is None or lon is None:
                return Response({"detail": "Invalid geocoding response."}, status=502)

            return Response(
                {
                    "query": used_query,
                    "lat": float(lat),
                    "lng": float(lon),
                    "display_name": first.get("display_name"),
                    "boundingbox": first.get("boundingbox"),
                }
            )
        except Exception:
            return Response({"detail": "Geocoding failed."}, status=502)


class LocationDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        location_id = request.query_params.get("id")
        if location_id:
            loc = Location.objects.filter(id=location_id).first()
        else:
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
                resp = httpx.get(url, headers={"User-Agent": "side-quest/1.0"}, timeout=2)
                if resp.status_code == 200:
                    data = resp.json()
                    display_name = data.get("display_name")
                    if display_name:
                        loc.address = display_name
            except Exception:
                pass

        passes = []
        fails = []
        breakdown = []
        if loc.comparison_id:
            raw = list(
                ChunkMatch.objects.filter(comparison_id=loc.comparison_id).values(
                    "status", "similarity", "rubric_path", "rubric_excerpt"
                )
            )

            def clean_label(label: str | None) -> str | None:
                if not label:
                    return None
                if "desc:" in label:
                    label = label.split("desc:", 1)[1]
                if "- values" in label:
                    label = label.split("- values", 1)[0]
                if "- val" in label:
                    label = label.split("- val", 1)[0]
                label = label.strip(" ,-\n\t")
                # Skip aggregate or metadata-like labels
                lower = label.lower()
                if lower.startswith("requirements covered") or lower.startswith("categories:"):
                    return None
                # sentence casing and punctuation tidy
                if label:
                    label = label[0].upper() + label[1:]
                    if label.endswith(","):
                        label = label[:-1]
                    if not label.endswith((".", "!", "?")):
                        label = label + "."
                return label

            _CAT_MAP = {
                "phys": "Physical Access",
                "sens": "Sensory Alerts",
                "soc": "Social & Health",
                "neuro": "Neurodivergent",
            }

            def extract_category(excerpt: str | None) -> str:
                if excerpt:
                    m = re.search(r'id:\s*([a-z]+)_', excerpt)
                    if m:
                        return _CAT_MAP.get(m.group(1), m.group(1).capitalize())
                return "Other"

            # Build per-category breakdown
            cat_counts: dict[str, dict] = {}
            for m in raw:
                cat = extract_category(m["rubric_excerpt"] or m["rubric_path"])
                if cat not in cat_counts:
                    cat_counts[cat] = {"found": 0, "missing": 0}
                if m["status"] in ("strong", "partial"):
                    cat_counts[cat]["found"] += 1
                else:
                    cat_counts[cat]["missing"] += 1
            breakdown = [
                {"name": k, "found": v["found"], "missing": v["missing"]}
                for k, v in cat_counts.items()
            ]

            # All passes ordered by highest similarity
            for m in sorted(raw, key=lambda x: x["similarity"], reverse=True):
                if m["status"] not in ("strong", "partial"):
                    continue
                label = clean_label(m["rubric_excerpt"] or m["rubric_path"])
                if not label:
                    continue
                passes.append({"label": label, "similarity": m["similarity"]})

            # All fails ordered by lowest similarity (worst first)
            for m in sorted(raw, key=lambda x: x["similarity"]):
                if m["status"] != "missing":
                    continue
                label = clean_label(m["rubric_excerpt"] or m["rubric_path"])
                if not label:
                    continue
                fails.append({"label": label, "similarity": m["similarity"]})

            # If no explicit missing, fall back to weakest partials
            if not fails:
                for m in sorted(raw, key=lambda x: x["similarity"]):
                    if m["status"] != "partial":
                        continue
                    label = clean_label(m["rubric_excerpt"] or m["rubric_path"])
                    if not label:
                        continue
                    fails.append({"label": label, "similarity": m["similarity"]})

        data = {
            "score": loc.score,
            "address": loc.address,
            "name": loc.name,
            "source": loc.source_doc,
            "passes": passes,
            "fails": fails,
            "breakdown": breakdown,
        }
        return Response(data)
