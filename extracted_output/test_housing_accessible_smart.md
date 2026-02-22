# Accessibility Extraction Report

- **Source:** `test_housing_accessible.txt`
- **Building type:** housing
- **Input type:** text
- **Model:** gpt-4.1
- **Address:** 123 Maple Ridge Crescent, Edmonton, Alberta T6G 2R3
- **Coordinates:** 53.5232, -113.5263

## Notes
All listed accessibility requirements are explicitly addressed in the report, with detailed measurements and standards referenced. The building is designed for accessible-ready retrofit without structural, electrical, plumbing, or HVAC modification. Multilingual and multi-format signage, as well as comprehensive sensory alerts, are provided. All physical access features, including routes, doors, maneuvering areas, and room layouts, meet or exceed CSA/ASC B652 standards.

## Found Requirements

### social_health
- **Multilingual Signage** (confidence: 100%)
  - All building signage, including emergency procedures, accessibility information, building rules, wayfinding, and operational instructions, is available in multiple formats and languages, including plain-language, ASL, LSQ, large-print, Braille, and accessible digital formats.
  - `formats`: plain-language, ASL, LSQ, large-print (18pt+), Braille, WCAG 2.1 AA digital PDF

### physical_access
- **Accessible Routes** (confidence: 100%)
  - Barrier-free path of travel from public sidewalk to all main entrances; interior routes minimum 1200 mm clear width, exterior routes minimum 1500 mm clear width, level, slip-resistant, compliant with CSA/ASC B652.
  - `interior_min_width_mm`: 1200
  - `exterior_min_width_mm`: 1500
  - `max_level_change_mm`: 13
- **Alternate Accessible Routes (Stair Alternatives)** (confidence: 100%)
  - Design allows installation of accessible elevating devices (e.g., lifts) between storeys at any future time without structural, electrical, plumbing, or HVAC modifications; structural blocking and electrical rough-ins provided.
  - `future_elevating_device_ready`: True
- **Door Minimum Width** (confidence: 100%)
  - All doorways, including unit entry, bathroom, bedroom, kitchen, laundry, and entrance doors, have a minimum clear width of 860 mm when open.
  - `min_door_width_mm`: 860
- **Accessible Maneuvering Area at Doors** (confidence: 100%)
  - Level, clear, unobstructed maneuvering areas at all doors: 600 mm pull side, 300 mm push side, 1200 mm interior, 1500 mm exterior; all areas level (max slope 1:50).
  - `pull_side_clearance_mm`: 600
  - `push_side_clearance_mm`: 300
  - `interior_maneuvering_area_mm`: 1200
  - `exterior_maneuvering_area_mm`: 1500
  - `max_slope`: 1:50
- **Accessible-Ready Bathroom Showers** (confidence: 100%)
  - Bathrooms with showers designed for future retrofit: structural reinforcement for grab bars, curbless/low-threshold (max 13 mm), plumbing rough-ins for roll-in conversion, 900 mm x 900 mm clear turning space.
  - `threshold_max_mm`: 13
  - `turning_space_mm`: 900x900
- **Accessible-Ready Bathroom Bathtubs** (confidence: 100%)
  - Bathrooms with bathtubs designed for future retrofit: structural backing for grab bars, controls reachable from outside tub, 900 mm x 1500 mm clear floor space beside tub.
  - `clear_space_mm`: 900x1500
- **Accessible-Ready Bathroom Medicine Cabinets** (confidence: 100%)
  - Medicine cabinets recessed and adjustable in height, shelving within 400–1100 mm reach, wall blocking for future repositioning.
  - `reach_range_mm`: 400-1100
- **Accessible-Ready Kitchens** (confidence: 100%)
  - Kitchens designed for future retrofit: 1500 mm x 1500 mm clear turning diameter, under-counter cabinets removable for knee clearance, plumbing/drain repositionable, upper cabinets can be lowered, knee clearance blocking pre-installed.
  - `turning_diameter_mm`: 1500
- **Accessible-Ready Bedrooms** (confidence: 100%)
  - Bedrooms designed for future retrofit: 900 mm clear space on one side, 1500 mm at foot of bed, 860 mm doorway width, closets convertible to accessible wardrobes, electrical rough-ins for motorized/adjustable fixtures.
  - `side_clear_space_mm`: 900
  - `foot_clear_space_mm`: 1500
  - `door_width_mm`: 860
- **Accessible-Ready Laundry Rooms** (confidence: 100%)
  - Laundry rooms designed for future retrofit: front-loading appliances, 900 mm x 1500 mm clear floor space in front of appliances, plumbing/electrical positioned for accessible controls.
  - `clear_space_mm`: 900x1500
- **Operating Controls Height and Reach** (confidence: 100%)
  - All controls (switches, thermostats, outlets, intercoms, etc.) installed 400–1100 mm above floor; display controls 900–1100 mm; all can be relocated 400–1500 mm; operable with closed fist.
  - `controls_height_mm`: 400-1100
  - `display_controls_height_mm`: 900-1100
  - `relocation_range_mm`: 400-1500
- **Mobility Device Space in Meeting Rooms** (confidence: 100%)
  - All common rooms, meeting rooms, amenity spaces, lobbies, and corridors provide clear floor spaces for wheeled mobility devices: stationary space 820 mm x 1390 mm, turning diameter 1800 mm, T-turn 1800 mm x 1200 mm x 1200 mm.
  - `stationary_space_mm`: 820x1390
  - `turning_diameter_mm`: 1800
  - `t_turn_mm`: 1800x1200x1200

### sensory_alerts
- **Audible and Visual Alerts** (confidence: 100%)
  - All units and common areas equipped with interconnected fire alarm, smoke, and CO detectors providing both audible (min 75 dBA in sleeping rooms, max 110 dBA in occupied areas) and visual (strobe) alerts in all rooms, compliant with CAN/ULC-S524 and CAN/ULC-S526.
  - `audible_alarm_min_dBA`: 75
  - `audible_alarm_max_dBA`: 110
  - `visual_alert_standard`: CAN/ULC-S526
