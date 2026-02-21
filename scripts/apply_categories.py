#!/usr/bin/env python3
"""Apply category mapping to assessment_items based on criterion_key.

Usage:
  python scripts/apply_categories.py

Mapping is embedded below for housing/commercial rubrics.
"""
import sqlite3
from pathlib import Path

MAPPING = {
    # Housing / Commercial shared keys (normalize as needed)
    "social_health": ["multilingual_signage"],
    "physical_access": [
        "exterior_entry", "parking_access", "accessible_routes", "alternate_accessible_routes",
        "door_minimum_width", "accessible_maneuvering_area_at_doors", "accessible_ready_bathroom_showers",
        "accessible_ready_bathroom_bathtubs", "accessible_ready_bathroom_medicine_cabinets",
        "accessible_ready_kitchens", "accessible_ready_bedrooms", "accessible_ready_laundry_rooms",
        "operating_controls_height_and_reach", "mobility_device_space", "non_slip_flooring",
        "accessible_ready_parking", "accessible_ready_path", "accessible_ready_closets",
        "accessible_ready_service_rooms", "accessible_ready_emergency_egress",
    ],
    "sensory_alerts": ["audible_and_visual_alerts"],
    # Commercial-focused keys
    "exterior_parking": ["accessible_parking", "exterior_parking"],
    "ramps": ["ramps", "ramp_slope"],
    "entrances": ["entrances", "door_width_and_hardware", "thresholds"],
    "vertical_access": ["elevators_lifts", "vertical_access"],
    "circulation_protrusions": ["interior_circulation", "protrusion_hazards"],
    "restrooms": ["accessible_washrooms"],
    "counters_seating": ["accessible_counters", "service_counters"],
    "signage_comm": ["tactile_braille_signage", "visual_fire_alarms", "signage"],
    "digital_access": ["wcag_compliance", "digital_access"],
}

# Flatten mapping: criterion_key -> category
FLAT_MAP = {}
for cat, keys in MAPPING.items():
    for k in keys:
        FLAT_MAP[k] = cat

DB_PATH = Path("db/assessment.db")


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # Fetch distinct criterion_keys
    cur.execute("SELECT DISTINCT criterion_key FROM assessment_items")
    keys = [row[0] for row in cur.fetchall()]

    updated = 0
    for key in keys:
        cat = FLAT_MAP.get(key)
        if not cat:
            continue
        cur.execute(
            "UPDATE assessment_items SET category = ? WHERE criterion_key = ?",
            (cat, key),
        )
        updated += cur.rowcount

    con.commit()
    con.close()
    print(f"Updated category on {updated} rows. Unknown keys left unchanged.")


if __name__ == "__main__":
    main()
