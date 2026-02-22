# Accessibility Extraction Report

- **Source:** `test_commercial_accessible.txt`
- **Building type:** commercial
- **Input type:** text
- **Model:** gpt-4.1
- **Address:** 10155 102 Street NW, Edmonton, Alberta T5J 4G8
- **Coordinates:** 53.5444, -113.4909

## Notes
The report provides comprehensive details for physical access and neurodivergent support, including specific measurements and standards. Sensory alert and social health features are not described in the provided content, despite references to relevant standards. No explicit mention of assistive listening systems, fire alarms, or multilingual signage. All location and compliance standard details are clearly stated.

## Found Requirements

### physical_access
- **Accessible Routes** (confidence: 100%)
  - Continuous barrier-free path of travel connects entrances, parking, loading zone, and public thoroughfares; minimum clear width 1600 mm, pinch points 850 mm for max 600 mm, turning and passing spaces, rest areas, cross-slope, overhead clearance, grating/joint specs.
  - `min_clear_width`: 1600 mm
  - `pinch_point_width`: 850 mm (max 600 mm length)
  - `turning_space`: 1500 mm x 1000 mm
  - `passing_space`: 1700 mm x 1700 mm every 24 m
  - `rest_area`: 1500 mm x 2000 mm every 30 m
  - `cross_slope`: 1:50 max
  - `overhead_clearance`: 1980 mm
  - `grating_opening`: ≤13 mm
  - `grating_depth`: ≤6 mm
- **Exterior Building Entrances** (confidence: 100%)
  - All primary entrances fully accessible; min clear opening 850 mm, power-operated doors, level area 1500 mm x 1500 mm inside/outside, door viewers at two heights, universal washrooms on barrier-free path, entrance ramps <1:20 slope.
  - `min_door_width`: 850 mm
  - `level_area`: 1500 mm x 1500 mm
  - `door_viewer_heights`: 1500–1700 mm and 1000–1200 mm
  - `ramp_slope`: <1:20
- **Automatic Door Operation** (confidence: 100%)
  - Power door operators at all primary entrances, universal washrooms, elevator lobbies, service counters; automatic via motion sensor and push-plate at two heights (150–300 mm, 900–1100 mm); controls marked with International Symbol of Access.
  - `push_plate_heights`: 150–300 mm and 900–1100 mm
  - `hardware_length`: 140 mm
  - `hardware_height`: 900–1000 mm
  - `hardware_distance_from_hinge`: 200–300 mm
- **Door Minimum Width** (confidence: 100%)
  - All barrier-free doors min 850 mm clear width; exam/treatment rooms 915 mm; corridors 1000–1200 mm; lever-type hardware operable with closed fist.
  - `door_min_width`: 850 mm
  - `exam_room_door_width`: 915 mm
  - `corridor_width`: 1000–1200 mm
- **Alternate Accessible Routes (Stair Alternatives)** (confidence: 100%)
  - Four passenger elevators (cab 1500 mm x 2000 mm, door 900 mm), elevator/platform lift alternative to escalators, ramps (max slope 1:12, min width 1000 mm, landings 1700 mm x 1700 mm, handrails 865–965 mm).
  - `elevator_cab_size`: 1500 mm x 2000 mm
  - `elevator_door_width`: 900 mm
  - `ramp_slope`: 1:12 max
  - `ramp_width`: 1000 mm min
  - `landing_size`: 1700 mm x 1700 mm
  - `handrail_height`: 865–965 mm
- **Mobility Device Space in Meeting Rooms** (confidence: 100%)
  - Meeting/assembly/waiting rooms with fixed seating provide designated wheelchair spaces per Table 3.8.2.3; each space min 900 mm wide x 1525 mm long (side approach) or 1220 mm (front/rear); 1700 mm turning diameter; 900 mm transfer space.
  - `wheelchair_space_width`: 900 mm
  - `wheelchair_space_length_side`: 1525 mm
  - `wheelchair_space_length_front_rear`: 1220 mm
  - `turning_diameter`: 1700 mm
  - `transfer_space`: 900 mm
- **Accessible Viewing Space Dimensions** (confidence: 100%)
  - Assembly areas with tiered/fixed seating provide accessible viewing spaces min 850 mm x 1390 mm, unobstructed sightlines equivalent or better than adjacent seats.
  - `viewing_space`: 850 mm x 1390 mm
- **Maintain Required Aisle Width Behind Accessible Seating** (confidence: 100%)
  - Aisle width behind accessible seating is fully maintained; no encroachment or reduction below minimum.
- **Limits of Protruding Objects** (confidence: 100%)
  - No elements within 1980 mm of floor project more than 100 mm; signage/fixtures/equipment recessed or set back; cane detection at ≤680 mm; protruding elements have colour contrast or tactile warning.
  - `max_projection`: 100 mm
  - `cane_detection_height`: ≤680 mm
  - `overhead_clearance`: 1980 mm
- **Wheel Stops to Prevent Vehicle Intrusion** (confidence: 100%)
  - Wheel stops in all parking areas prevent vehicle intrusion onto barrier-free paths; maintain min clear sidewalk width 1500 mm.
  - `min_sidewalk_width`: 1500 mm
- **Curb Ramp Detectability** (confidence: 100%)
  - Curb ramps/curb cuts have colour and textural contrast (truncated dome tactile attention indicators), min 70% luminance contrast, tactile surfaces at base and crossings, CSA B651 compliant.
  - `luminance_contrast`: ≥70%
  - `tactile_surface`: truncated dome
- **Ramps** (confidence: 100%)
  - All ramps: min width 1000 mm (1140 mm preferred), max slope 1:12 (1:10 for assembly/care), max rise/run 750 mm, max length 9 m before landing, landings 1500 mm x 1500 mm, handrails both sides 865–965 mm, curb/edge protection, slip-resistant.
  - `min_width`: 1000 mm
  - `preferred_width`: 1140 mm
  - `max_slope`: 1:12
  - `max_rise_per_run`: 750 mm
  - `max_length`: 9 m
  - `landing_size`: 1500 mm x 1500 mm
  - `handrail_height`: 865–965 mm
  - `curb_height`: ≥75 mm

### neurodivergent
- **Clear Wayfinding Signage** (confidence: 100%)
  - Signage for accessible washrooms, elevators, parking, routes, exits; large print (18 pt), 70% luminance contrast, pictograms, positioned at 1500–1800 mm.
  - `font_size`: 18 pt min
  - `luminance_contrast`: ≥70%
  - `sign_height`: 1500–1800 mm
- **Pattern and Colour Blocking for Key Access** (confidence: 100%)
  - Escalator landings have truncated dome tactile attention indicators and high-contrast colour bands; 600 mm textural change at thresholds.
  - `tactile_pattern_depth`: truncated dome
  - `colour_band`: high-contrast
  - `pattern_extent`: 600 mm
- **Braille, Visual, and Audio Cues** (confidence: 100%)
  - Directories in lobbies with raised characters, Braille (1.5 mm dot base, 0.6–0.8 mm height), Braille on room signs, audio announcements in elevators and lobbies.
  - `braille_dot_base`: 1.5 mm
  - `braille_dot_height`: 0.6–0.8 mm
  - `directory_mount_height`: 760–900 mm
- **Non-Text Diagrams and Symbols** (confidence: 100%)
  - International Symbol of Access at all accessible features; Hearing Loss symbol at ALD/loop points; pictogram fields min 150 mm high; ISO 7001/21942 compliant.
  - `pictogram_height`: 150 mm
  - `standards`: ISO 7001, ISO 21942
- **Tactile Signs for Doors and Openings** (confidence: 100%)
  - All public doors/openings have tactile signs; letter height 60 mm, raised 0.7 mm, mounted 1200 mm above floor, within 150 mm of door, 70% luminance contrast.
  - `letter_height`: 60 mm
  - `raised_height`: 0.7 mm
  - `mounting_height`: 1200 mm
  - `luminance_contrast`: ≥70%
- **Tactile Signage Requirements** (confidence: 100%)
  - All tactile signage: letter height 60 mm, raised 0.7 mm, max mounting height 1200 mm, within 150 mm of entrance, colour contrast, consistent installation.
  - `letter_height`: 60 mm
  - `raised_height`: 0.7 mm
  - `mounting_height`: ≤1200 mm
- **Accessible Control Mounting Height** (confidence: 100%)
  - All controls mounted 900–1200 mm above floor; clear floor space 1350 mm x 800 mm adjacent; display controls at upper end.
  - `mounting_height`: 900–1200 mm
  - `clear_space`: 1350 mm x 800 mm
- **Accessible Control Operation** (confidence: 100%)
  - Controls operable with one hand, closed fist, max force 22 N; lever handles, push, loop pulls, capacitive touch; no two-handed operation.
  - `max_operating_force`: 22 N
- **Haptic and Tactile Maps** (confidence: 100%)
  - Tactile maps/directories in main and elevator lobbies; raised 0.8 mm, tactile text 13–19 mm, visual text 16–51 mm; audio description via push-button and QR code.
  - `tactile_map_height`: 0.8 mm
  - `tactile_text_height`: 13–19 mm
  - `visual_text_height`: 16–51 mm
- **High Colour Contrast for Orientation Signs** (confidence: 100%)
  - Orientation signs: white on black or black on white, ≥70% luminance contrast; stair nosings with 50 mm wide contrast strips, ≥70% contrast.
  - `luminance_contrast`: ≥70%
  - `stair_nosing_width`: 50 mm
- **Lighting, Audible, Tactile, Colour/Contrast, and Ergonomic Cues** (confidence: 100%)
  - Uniform, glare-free lighting (200 lux routes, 300 lux counters); audible announcements at intersections/elevators; tactile guide strips; colour/luminance contrast at hazards; ergonomic rest areas (seat height 430–500 mm, armrests).
  - `illumination_routes`: 200 lux
  - `illumination_counters`: 300 lux
  - `seat_height`: 430–500 mm
- **Quiet Space Availability** (confidence: 100%)
  - Dedicated quiet room on main and each occupied floor; acoustically separated (STC 45), table 600 mm x 900 mm at 710–760 mm height, knee clearance, 1500 mm x 1500 mm clear space, tactile/visual signage.
  - `acoustic_rating`: STC 45
  - `table_size`: 600 mm x 900 mm
  - `table_height`: 710–760 mm
  - `clear_space`: 1500 mm x 1500 mm

## Not Found

### sensory_alerts
- Audible and Visual Alerts
- Warning Indicators
- Tactile Attention Indicator Configuration
- Tactile Attention Indicator Installation
- Visual Contrast Between Walls and Floors
- Tactile Direction Indicator Configuration
- Fire Alarm Sound Pressure Levels
- Visual Signal Device Installation
- Assistive Listening at Service Counters
- Assistive Listening Systems in Public Areas
- Induction Loop Receiver Ratio
- Annual ALD and Loop System Testing

### social_health
- Adult Changing Facility
- Multilingual Signage
