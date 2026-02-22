# Accessibility Extraction Report

- **Source:** `test_commercial_accessible.txt`
- **Building type:** commercial
- **Input type:** text
- **Model:** gpt-4.1
- **Address:** 10155 102 Street NW, Edmonton, Alberta T5J 4G8
- **Coordinates:** 53.5444, -113.4909

## Notes
All listed accessibility requirements are present and compliant per the referenced standards (Alberta Accessibility Design Guide 2024, CSA B651, CAN/ULC-S526, IEC60118-4). The building demonstrates comprehensive accessibility across physical, neurodivergent, sensory, and social health categories, with detailed measurements and operational protocols provided for each feature.

## Found Requirements

### physical_access

- **Accessible Routes** (confidence: 100%)
  - Barrier-free path between all accessible entrances, parking, passenger-loading zones, and public thoroughfares; minimum 1600 mm wide; turning spaces 1500 mm x 1000 mm; passing spaces 1700 mm x 1700 mm every 24 m; rest areas every 30 m; cross-slope max 1:50; overhead clearance min 1980 mm.
  - `min_width`: 1600 mm
  - `turning_space`: 1500 mm x 1000 mm
  - `passing_space`: 1700 mm x 1700 mm every 24 m
  - `rest_area`: 1500 mm x 2000 mm every 30 m
  - `cross_slope`: 1:50 max
  - `overhead_clearance`: 1980 mm

- **Exterior Building Entrances** (confidence: 100%)
  - Power-operated doors at all accessible entrances; minimum clear opening 850 mm; level area 1500 mm x 1500 mm; ramp slope less than 1:20; universal washrooms on barrier-free path with power-operated doors.
  - `door_clear_opening`: 850 mm
  - `level_area`: 1500 mm x 1500 mm
  - `ramp_slope`: <1:20

- **Automatic Door Operation** (confidence: 100%)
  - Power door operators at all primary entrances and universal washrooms; controls at 150–300 mm and 900–1100 mm above floor; marked with International Symbol of Access; door pull 140 mm length at 900–1000 mm height, 200–300 mm from hinge edge.
  - `control_heights`: 150–300 mm, 900–1100 mm
  - `door_pull_length`: 140 mm
  - `door_pull_height`: 900–1000 mm

- **Door Minimum Width** (confidence: 100%)
  - All barrier-free path doors minimum 850 mm clear width; examination rooms 915 mm; lever hardware; closed-fist operable.
  - `min_width`: 850 mm
  - `exam_room_width`: 915 mm

- **Alternate Accessible Routes (Stair Alternatives)** (confidence: 100%)
  - Four elevators serve all floors; ramps at all level changes greater than 13 mm; minimum slope 1:12; minimum width 1000 mm; level landings 1700 mm x 1700 mm; handrails at 865–965 mm.
  - `elevators`: 4
  - `ramp_slope`: 1:12 max
  - `ramp_width`: 1000 mm min
  - `landing`: 1700 mm x 1700 mm

- **Mobility Device Space in Meeting Rooms** (confidence: 100%)
  - Wheelchair spaces per Table 3.8.2.3; each space min 900 mm wide x 1525 mm long (side approach); turning diameter 1700 mm; transfer space 900 mm.
  - `space_width`: 900 mm
  - `space_length`: 1525 mm
  - `turning_diameter`: 1700 mm
  - `transfer_space`: 900 mm

- **Accessible Viewing Space Dimensions** (confidence: 100%)
  - Minimum 850 mm x 1390 mm independent clear space per accessible viewing position; unobstructed sightlines.
  - `min_width`: 850 mm
  - `min_length`: 1390 mm

- **Maintain Required Aisle Width Behind Accessible Seating** (confidence: 100%)
  - Aisle widths behind accessible seating maintained at required minimums; no intrusion into accessible aisle.

- **Limits of Protruding Objects** (confidence: 100%)
  - No elements project more than 100 mm horizontally into paths within 1980 mm of the floor; all protruding elements provide cane-detectable undersides at or below 680 mm.
  - `max_projection`: 100 mm
  - `cane_detection_height`: 680 mm

- **Wheel Stops to Prevent Vehicle Intrusion** (confidence: 100%)
  - Wheel stops provided in all parking areas to prevent vehicle intrusion onto barrier-free paths and sidewalks.
  - `min_clear_sidewalk_width`: 1500 mm

- **Curb Ramp Detectability** (confidence: 100%)
  - All curb ramps identified by colour contrast and truncated dome tactile attention indicators for detection by persons with low vision, blindness, or cognitive impairments.
  - `luminance_contrast`: 70% min

- **Ramps** (confidence: 100%)
  - Maximum slope 1:12; minimum width 1000 mm (1140 mm preferred); maximum rise 750 mm; maximum length 9 m; level landings 1500 mm x 1500 mm; handrails 865–965 mm both sides; curb edges 75 mm minimum; slip-resistant surfaces.
  - `slope`: 1:12 max
  - `width`: 1000 mm min
  - `rise`: 750 mm max
  - `length`: 9 m max
  - `landing`: 1500 mm x 1500 mm
  - `handrail_height`: 865–965 mm
  - `curb_edge`: 75 mm min

### neurodivergent

- **Clear Wayfinding Signage** (confidence: 100%)
  - Large print, tonal contrast (min 70% luminance), pictograms at all decision points; accessible washrooms, elevators, and accessible routes clearly marked; mounted 1500–1800 mm above floor.
  - `font_size`: 18 pt min
  - `luminance_contrast`: 70% min
  - `mounting_height`: 1500–1800 mm

- **Pattern and Colour Blocking for Key Access** (confidence: 100%)
  - Truncated dome tactile attention indicators and high-contrast colour bands at all escalator tops and bottoms; 600 mm depth of textural floor change.
  - `tactile_depth`: 600 mm

- **Braille, Visual, and Audio Cues** (confidence: 100%)
  - Building directories on sloping plane at 760–900 mm; characters raised 0.7 mm; Braille at 1015–1525 mm; dot base 1.5 mm, dot height 0.6–0.8 mm; audio announcements in all elevators and lobby.
  - `directory_height`: 760–900 mm
  - `braille_height`: 1015–1525 mm
  - `dot_base`: 1.5 mm
  - `dot_height`: 0.6–0.8 mm

- **Non-Text Diagrams and Symbols** (confidence: 100%)
  - International Symbol of Access at all accessible facilities; International Symbol of Access for Hearing Loss at all ALD locations; pictogram field minimum 150 mm; conform to ISO 7001 and ISO 21942.
  - `pictogram_height`: 150 mm

- **Tactile Signs for Doors and Openings** (confidence: 100%)
  - Letters minimum 60 mm high, raised 0.7 mm, at 1200 mm above floor, within 150 mm of door; colour contrast minimum 70% luminance.
  - `letter_height`: 60 mm
  - `raised`: 0.7 mm
  - `mounting_height`: 1200 mm
  - `distance_from_door`: 150 mm
  - `luminance_contrast`: 70% min

- **Tactile Signage Requirements** (confidence: 100%)
  - Minimum 60 mm letter height, 0.7 mm raised characters, maximum 1200 mm mounting height, within 150 mm of entrance, colour contrasting.
  - `letter_height`: 60 mm
  - `raised`: 0.7 mm
  - `mounting_height`: 1200 mm max
  - `distance_from_entrance`: 150 mm

- **Accessible Control Mounting Height** (confidence: 100%)
  - All controls mounted 900–1200 mm above floor; adjacent clear floor space 1350 mm x 800 mm.
  - `mounting_height`: 900–1200 mm
  - `clear_floor_space`: 1350 mm x 800 mm

- **Accessible Control Operation** (confidence: 100%)
  - All controls operable with one hand in closed fist position; maximum 22 N operating force; no tight grasping, pinching, or twisting required.
  - `max_operating_force`: 22 N

- **Haptic and Tactile Maps** (confidence: 100%)
  - Raised minimum 0.8 mm; tactile characters 13–19 mm; visual characters 16–51 mm; audio description stations in lobby and all elevator lobbies.
  - `raised`: 0.8 mm
  - `tactile_char_height`: 13–19 mm
  - `visual_char_height`: 16–51 mm

- **High Colour Contrast for Orientation Signs** (confidence: 100%)
  - White on black or black on white; minimum 70% luminance contrast; floor identification and orientation signs in all stairwells and elevator lobbies.
  - `luminance_contrast`: 70% min

- **Lighting, Audible, Tactile, Colour/Contrast, and Ergonomic Cues** (confidence: 100%)
  - Minimum 200 lux on accessible routes, 300 lux at service counters; audible directional announcements; tactile guide strips; luminance contrast at all level changes and hazards; ergonomic seating at 430–500 mm height with armrests.
  - `illumination_routes`: 200 lux min
  - `illumination_counters`: 300 lux min
  - `seat_height`: 430–500 mm

- **Quiet Space Availability** (confidence: 100%)
  - Dedicated quiet rooms on every occupied floor; STC 45 acoustic separation; table for communication devices at 710–760 mm height with knee clearance; minimum 1500 mm x 1500 mm clear floor space; tactile and visual signage.
  - `acoustic_separation`: STC 45
  - `table_height`: 710–760 mm
  - `clear_floor_space`: 1500 mm x 1500 mm

### sensory_alerts

- **Audible and Visual Alerts** (confidence: 100%)
  - All security-controlled entrances provide both visual and audible signals on lock release; all fire alarm areas provide simultaneous audible and visual signals; visual devices in all rooms conform to CAN/ULC-S526; all systems interconnected.

- **Warning Indicators** (confidence: 100%)
  - Tactile attention indicator surfaces per CSA B651 at all downward elevation changes exceeding 300 mm; stair tops/bottoms; pedestrian crossings; curb ramps; elevator doors; escalator landings; full width of hazard; 610 mm platform offset; 150–200 mm curb setback.
  - `platform_offset`: 610 mm
  - `curb_setback`: 150–200 mm

- **Tactile Attention Indicator Configuration** (confidence: 100%)
  - Truncated domes 4–5 mm high; top diameter 12–25 mm; base diameter top+10±1 mm; square grid; spacing 42–70 mm between dome centres; durable, slip-resistant, UV-stable materials; CSA B651 compliant.
  - `dome_height`: 4–5 mm
  - `top_diameter`: 12–25 mm
  - `base_diameter`: top+10±1 mm
  - `spacing`: 42–70 mm

- **Tactile Attention Indicator Installation** (confidence: 100%)
  - Full width of hazard; depth 600–650 mm; one side against hazard edge; flush-mounted maximum 3 mm edge transition; permanently anchored.
  - `depth`: 600–650 mm
  - `edge_transition`: 3 mm max

- **Visual Contrast Between Walls and Floors** (confidence: 100%)
  - Luminance contrast minimum 50% between tactile attention indicator surfaces and adjacent floor surfaces per Michelson formula; stair nosings minimum 50 mm wide minimum 50% luminance contrast; wall-floor junctions have contrasting base trim; door frames have contrasting finish.
  - `luminance_contrast`: 50% min
  - `stair_nosing_width`: 50 mm min

- **Tactile Direction Indicator Configuration** (confidence: 100%)
  - Flat-topped parallel bars; height 4–5 mm; top width 17–30 mm; base width top+10±1 mm; top length minimum 270 mm; bars oriented in direction of travel; distinguishable from attention indicators.
  - `bar_height`: 4–5 mm
  - `top_width`: 17–30 mm
  - `base_width`: top+10±1 mm
  - `top_length`: 270 mm min

- **Fire Alarm Sound Pressure Levels** (confidence: 100%)
  - Maximum 110 dBA in all normally occupied areas; minimum 75 dBA in sleeping rooms with doors closed; minimum 10 dBA above ambient; conforms to CAN/ULC-S524.
  - `max_level`: 110 dBA
  - `min_sleeping_room`: 75 dBA
  - `min_above_ambient`: 10 dBA

- **Visual Signal Device Installation** (confidence: 100%)
  - Strobes installed in addition to audible devices in all suites, corridors, washrooms, meeting rooms, service areas, and elevator cabs; visible throughout each space; flash rate 1–3 Hz; fully supervised; conforms to CAN/ULC-S526.
  - `flash_rate`: 1–3 Hz

- **Assistive Listening at Service Counters** (confidence: 100%)
  - Induction loop or amplification system at all service counters with verbal communication; at least one counter per area with hearing loop; marked with International Symbol of Access for Hearing Loss; amplification at all barrier-protected counters.

- **Assistive Listening Systems in Public Areas** (confidence: 100%)
  - Induction loop systems in all areas with anticipated occupancy of 50 or more persons; all PA/sound system areas equipped with magnetic induction loop; coverage verified to IEC60118-4 2014.

- **Induction Loop Receiver Ratio** (confidence: 100%)
  - Minimum 1 portable loop receiver per 50 occupants in all loop-equipped spaces; receivers stored in clearly identified accessible locations adjacent to each loop area; quantity posted on signage.
  - `receiver_ratio`: 1 per 50 occupants

- **Annual ALD and Loop System Testing** (confidence: 100%)
  - All ALDs and induction loop installations tested once per year; IEC60118-4 2014 protocol followed; Certificate of Conformity issued after each annual test; deficiencies corrected within 30 days.

### social_health

- **Adult Changing Facility** (confidence: 100%)
  - Height-adjustable adult change tables on main floor and floor 3; height range 450–500 mm (low) to 850–900 mm (high); clear floor space minimum 900 mm x 1830 mm in front; load-rated 200 kg; located on barrier-free path in universal washrooms with power-operated doors.
  - `height_range`: 450–900 mm
  - `clear_space`: 900 mm x 1830 mm
  - `load_rating`: 200 kg

- **Multilingual Signage** (confidence: 100%)
  - All building signage and safety information available in plain-language, ASL, and LSQ formats; large-print (minimum 18 pt); Braille; and WCAG 2.1 AA-compliant digital formats.
  - `large_print`: 18 pt min
  - `formats`: plain-language, ASL, LSQ, Braille, digital
