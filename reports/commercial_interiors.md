
# Accessibility Rubric (commercial_interiors)

- Requirements covered: 38
- Categories: 4
- Conflicts flagged: 34


## physical_access

- **Accessible Routes** (id: phys_001, conf 1.00)
  - desc: A barrier-free path of travel must be provided between accessible entrances and designated parking, passenger-loading zones, and public thoroughfares.
  - values: {'min_width': '1600 mm (recommended 1800 mm for two deaf people side by side)', 'reduced_width': '850 mm for max 600 mm length', 'turning_space': '1500 mm x 1000 mm', 'passing_space': '1700 mm x 1700 mm every 24 m', 'clear_space': '1700 mm diameter or 1700 mm x 1500 mm or T-shaped 1700 mm x 1500 mm', 'text': 'Clear width: 1000 mm min; Headroom: 2100 mm min; Slope: as gentle as possible', 'cross_slope_max': '1:50', 'min_width_mm': '1100', 'obstruction_free_height_mm': '1980', 'preferred_width_mm': '1500', 'rest_area_interval_m': '30', 'rest_area_width_mm': '1500', 'rest_area_length_mm': '2000', 'grating_max_opening_mm': '13', 'joint_max_width_mm': '13', 'joint_max_depth_mm': '6', 'min_overhead_clearance_mm': '1980', 'interval_m': '30', 'diameter_min_mm': '1500', 'ramp_max_length': '9 m', 'ramp_max_rise': '750 mm', 'minimum_width': '1,500 mm'}
  - pages: [20]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Exterior Building Entrances** (id: phys_003, conf 1.00)
  - desc: Universal washrooms require a power-operated door along a barrier-free path of travel.
  - values: {'text': 'Door viewer at 1500-1700 mm, optional at 1000-1200 mm', 'level_area_mm': '1500x1500', 'min_percent_barrier_free': '50', 'clear_opening_min': '850 mm', 'clear_opening_preferred': '900 mm', 'minimum_width': '1,140 mm', 'width': '1200 mm', 'slope': '<1:20'}
  - pages: [62]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Automatic Door Operation** (id: phys_006, conf 1.00)
  - desc: Power door operators must activate automatically or by accessible controls, be marked, and be operable at specified heights.
  - values: {'text': 'controls operable at 150-300 mm and 900-1100 mm above floor', 'applicable_occupancies': 'hotel, Group B Div 2, Group A/B3/D/E >500m²', 'door_pull_length_mm': '140', 'door_pull_height_mm': '900-1000', 'door_pull_distance_from_hinge_mm': '200-300'}
  - pages: [44]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Door Minimum Width** (id: phys_004, conf 1.00)
  - desc: Doorways in barrier-free paths must have a clear width of at least 850 mm when open.
  - values: {'text': '≥ 850 mm (short side), ≥ 1 000 mm (long side)', 'dwelling_unit_min_width_mm': '850', 'clinic_exam_treatment_min_width_mm': '915', 'door_min_width_mm': '900', 'hallway_width_mm': '1000-1200', 'min_clear_width_mm': '850', 'clear_opening_min': '850 mm', 'clear_opening_preferred': '900 mm', 'width_min_mm': '800', 'min_door_width': '850 mm'}
  - pages: [43]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Alternate Accessible Routes (Stair Alternatives)** (id: phys_009, conf 1.00)
  - desc: Where escalators or inclined moving walks provide access to a floor, an interior barrier-free path of travel (e.g., elevator, lift) must also be provided to that floor.
  - values: {'curb_ramp_slope': '1:15 to 1:10', 'blended_transition_slope': 'not steeper than 1:20', 'cross_slope': 'not steeper than 1:50', 'turning_space': '1390 mm x 1390 mm', 'text': 'ramps, elevators, or platform lifts required for >13 mm level change', 'additional_space_inward_swing_mm': '900', 'level_area_length': '1,500 mm'}
  - pages: [20]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Mobility Device Space in Meeting Rooms** (id: phys_007, conf 1.00)
  - desc: Assembly occupancies and waiting rooms with fixed seats must provide a minimum number of designated wheelchair spaces as per Table 3.8.2.3.
  - values: {'table': '2–99 seats: 2 spaces; 100–499: 3 + 1/70 over 100; 500–1999: 9 + 1/80 over 500; 2000–7999: 28 + 1/95 over 2000; Over 7999: 91 + 1/100 over 8000', 'percent': '5%', 'max': '20', 'text': '820 mm x 1390 mm (stationary), 1800 mm turning diameter, 1800 mm x 1200 mm x 1200 mm (T-turn)', 'width_min_mm': '900', 'length_min_mm_side_approach_mm': '1700', 'length_min_mm_front_rear_approach_mm': '1350', 'turning_diameter_mm': '1700', 'transfer_space_mm': '900', 'width_mm': '900', 'length_mm_side_approach': '1525', 'length_mm_front_rear_approach': '1220', 'percentage_of_total_seats': '0.005–0.0075', 'clearance_in_swinging_door_mm': '1700', 'clearance_wall_fixture_mm': '1400', 'min_turning_diameter': '1500 mm'}
  - pages: [16, 17]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Accessible Viewing Space Dimensions** (id: phys_new_001, conf 1.00)
  - desc: Accessible viewing spaces in assembly areas must provide a minimum independent seating space of 850 mm by 1390 mm.
  - values: {'min_width_mm': 850, 'min_length_mm': 1390}
  - pages: [18]
  - source: ma-accessibility-design-guide-2024.md

- **Maintain Required Aisle Width Behind Accessible Seating** (id: phys_new_002, conf 1.00)
  - desc: Aisle width behind accessible seating areas must be maintained to ensure unobstructed passage.
  - values: n/a
  - pages: [18]
  - source: ma-accessibility-design-guide-2024.md

- **Limits of Protruding Objects** (id: phys_new_004, conf 1.00)
  - desc: Protruding building elements within 1980 mm of the floor must not project more than 100 mm horizontally into paths of travel unless clearance below is less than 680 mm.
  - values: {'max_projection_mm': 100, 'max_height_mm': 1980, 'exception_clearance_mm': 680}
  - pages: [18, 19]
  - source: ma-accessibility-design-guide-2024.md

- **Wheel Stops to Prevent Vehicle Intrusion** (id: phys_new_006, conf 1.00)
  - desc: Wheel stops should be used to prevent vehicles from intruding onto the barrier-free path of travel on sidewalks.
  - values: n/a
  - pages: [21]
  - source: ma-accessibility-design-guide-2024.md

- **Curb Ramp Detectability** (id: phys_new_007, conf 1.00)
  - desc: Curbs and curb ramps should be designed with colour or texture contrast to be easily detected by people with low vision, blindness, or cognitive impairments.
  - values: n/a
  - pages: [21]
  - source: ma-accessibility-design-guide-2024.md

- **Ramps** (id: phys_002, conf 1.00)
  - desc: Changes in level greater than 13 mm in a barrier-free path must be provided with sloped floors or ramps.
  - values: {'width_mm': '760', 'length_mm': '1500', 'threshold': '13 mm', 'min_width': '1000 mm', 'max_slope': '1:12', 'level_area_top_bottom': '1700 mm x 1700 mm', 'handrail_height': '865-965 mm', 'text': 'ramp for >200 mm level change, 1:10 max slope', 'ramp_slope_threshold': '1:20', 'curb_required_dropoff_mm': '75', 'min_width_mm': '870', 'level_area_mm': '1500x1500', 'landing_size_mm': '1500x1500', 'max_landing_interval_m': '9', 'assembly_care_residential': '1:10', 'mercantile_industrial': '1:6', 'other': '1:8', 'exterior': '1:10', 'threshold_slope': '1:20', 'max_ramp_length': '9 m', 'max_ramp_rise': '750 mm', 'width': '1,140 mm', 'gradient': '1:20', 'level_area': '1,500 mm x 1,500 mm'}
  - pages: [29]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict


## neurodivergent

- **Clear Wayfinding Signage** (id: nd_001, conf 1.00)
  - desc: Clear signage indicating the location of accessible washrooms, elevators, and accessible routes must be provided and be easily visible.
  - values: {'text': 'large print, tonal contrast, pictograms'}
  - pages: [20]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Pattern and Colour Blocking for Key Access** (id: nd_004, conf 1.00)
  - desc: Visual and tactile or textural warning systems should be provided on escalator steps and floor surfaces at the top and bottom of escalators for orientation.
  - values: n/a
  - pages: [20]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Braille, Visual, and Audio Cues** (id: nd_003, conf 0.95)
  - desc: Building directories should be tactile, on a sloping plane 760–900 mm above the floor, with characters raised at least 0.7 mm.
  - values: {'text': 'Braille located 1 015 mm min to 1 525 mm max above floor; dot base diameter 1.5 mm; dot height 0.6–0.8 mm', 'height_range_mm': '760–900', 'character_raise_mm': '0.7'}
  - pages: n/a
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Non-Text Diagrams and Symbols** (id: nd_002, conf 0.95)
  - desc: Signs must incorporate the International Symbol of Access or the International Symbol of Access for Hearing Loss and appropriate graphical or textual information.
  - values: {'text': 'Pictogram field height 150 mm min'}
  - pages: n/a
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Tactile Signs for Doors and Openings** (id: nd_new_004, conf 0.95)
  - desc: Doors and openings from public places should be identified by tactile signs with letters ≥60 mm high, raised 0.7 mm, located 1200 mm above floor, ≤150 mm from door.
  - values: {'letter_height_mm': '60', 'raise_mm': '0.7', 'location_above_floor_mm': '1200', 'distance_from_door_mm': '150'}
  - pages: [56]
  - source: ma-accessibility-design-guide-2024.md

- **Tactile Signage Requirements** (id: nd_new_001, conf 0.95)
  - desc: Tactile signage must be not less than 60 mm high, raised ~0.7 mm, located ≤1200 mm above floor, ≤150 mm from entrance, and contrasting in colour.
  - values: {'text': '60 mm high, 0.7 mm raised, ≤1200 mm height, ≤150 mm from entrance'}
  - pages: [119]
  - source: ma-barrier-free-design-guide-fifth-edition-2017.md

- **Accessible Control Mounting Height** (id: nd_new_001, conf 0.90)
  - desc: Controls must be mounted 900 mm to 1 200 mm above the floor and adjacent to a clear floor space of 1 350 mm by 800 mm.
  - values: {'text': '900–1 200 mm height; 1 350 mm x 800 mm clear space'}
  - pages: [52]
  - source: ma-accessibility-design-guide-2024.md

- **Accessible Control Operation** (id: nd_new_002, conf 0.90)
  - desc: Controls must be operable with one hand in a closed fist position, without tight grasping, pinching, or twisting, and require no more than 22 N of force.
  - values: {'text': '≤ 22 N force'}
  - pages: [52]
  - source: ma-accessibility-design-guide-2024.md

- **Haptic and Tactile Maps** (id: nd_005, conf 0.90)
  - desc: Directions for blind persons can use pre-recorded messages or tactile maps and signs.
  - values: {'text': 'Raised 0.8 mm min; height 13–19 mm (tactile), 16–51 mm (visual)'}
  - pages: [55]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **High Colour Contrast for Orientation Signs** (id: nd_new_002, conf 0.90)
  - desc: Identification of floors and orientation signs for visually disabled users should offer maximum colour contrast, preferably white on black or black on white.
  - values: n/a
  - pages: [56]
  - source: ma-accessibility-design-guide-2024.md

- **Lighting, Audible, Tactile, Colour/Contrast, and Ergonomic Cues** (id: nd_new_005, conf 0.90)
  - desc: Orientation for visually disabled persons should use lighting, audible, tactile, colour/contrast, and ergonomic cues for wayfinding and safety.
  - values: n/a
  - pages: [56]
  - source: ma-accessibility-design-guide-2024.md

- **Quiet Space Availability** (id: nd_new_001, conf 0.90)
  - desc: Ensure sufficient space and quiet space options are provided, including a small table for communication devices, to accommodate persons with neurodiversity and communication/cognitive disorders.
  - values: n/a
  - pages: [94]
  - source: ma-accessibility-design-guide-2024.md


## sensory_alerts

- **Audible and Visual Alerts** (id: sens_001, conf 1.00)
  - desc: If an entrance is equipped with a security system, both visual and audible signals must indicate when the door lock is released.
  - values: {'min_area_m2': '100', 'max_dba': '110', 'min_dba_sleeping_room': '75', 'min_dba_above_ambient': '10', 'min_dba_with_doors_closed': '65'}
  - pages: [46]
  - source: ma-barrier-free-design-guide-fifth-edition-2017.md ⚠ conflict

- **Warning Indicators** (id: sens_003, conf 1.00)
  - desc: Downward changes in elevation in a barrier-free path must be signaled by tactile attention indicator surfaces per CSA B651.
  - values: {'drop_off_threshold': '300 mm', 'platform_offset_mm': '610', 'stair_tread_offset': 'one tread before nosing', 'stair_twsis_min_depth_mm': '920', 'railway_min_distance_mm': '1800', 'railway_max_distance_mm': '4600', 'curb_setback_min_mm': '150', 'curb_setback_max_mm': '200', 'curb_min_depth_mm': '610', 'dome_height_mm': '5±1', 'dome_top_diameter_mm': '12–20', 'dome_base_diameter_offset_mm': '10±1', 'min_base_spacing_mm': '15', 'min_width_mm': '250', 'max_width_mm': '550', 'min_clearance_each_side_mm': '600', 'bar_height_mm': '5±1', 'bar_top_width_mm': '17–30', 'bar_base_offset_mm': '10±1', 'min_crossing_width_mm': '550', 'text': '10 dBA min above ambient, 80 dBA max'}
  - pages: [30]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Tactile Attention Indicator Configuration** (id: sens_new_001, conf 1.00)
  - desc: Tactile attention indicator surfaces must use truncated domes 4–5 mm high, top diameter 12–25 mm, base diameter 10±1 mm greater, in a square grid, with specified spacing.
  - values: {'height': '4–5 mm', 'top_diameter': '12–25 mm', 'base_diameter': 'top+10±1 mm', 'spacing': '42–70 mm'}
  - pages: [30, 31, 32]
  - source: ma-accessibility-design-guide-2024.md

- **Tactile Attention Indicator Installation** (id: sens_new_002, conf 1.00)
  - desc: Tactile attention indicator surfaces must be installed along the full width of the hazard, 600–650 mm deep, with one side against the edge of the hazard.
  - values: {'depth': '600–650 mm'}
  - pages: [32]
  - source: ma-accessibility-design-guide-2024.md

- **Visual Contrast Between Walls and Floors** (id: sens_002, conf 1.00)
  - desc: Tactile attention indicator surfaces must have a luminance (colour) contrast of at least 50% with adjacent surfaces using the Michelson contrast formula.
  - values: {'min_contrast': '50%'}
  - pages: [32]
  - source: ma-accessibility-design-guide-2024.md ⚠ conflict

- **Tactile Direction Indicator Configuration** (id: sens_new_003, conf 1.00)
  - desc: Tactile direction indicator surfaces must use flat-topped, parallel, elongated bars 4–5 mm high, top width 17–30 mm, base width top+10±1 mm, top length ≥270 mm.
  - values: {'height': '4–5 mm', 'top_width': '17–30 mm', 'base_width': 'top+10±1 mm', 'top_length': '≥270 mm'}
  - pages: [33]
  - source: ma-accessibility-design-guide-2024.md

- **Fire Alarm Sound Pressure Levels** (id: sensory_alerts_new_001, conf 0.96)
  - desc: Fire alarm signal sound pressure level must not exceed 110 dBA in any normally occupied area; in sleeping rooms, not less than 75 dBA with doors closed.
  - values: {'max_dba': '110', 'min_dba_sleeping_room': '75'}
  - pages: [108]
  - source: ma-barrier-free-design-guide-fifth-edition-2017.md

- **Visual Signal Device Installation** (id: sensory_alerts_new_004, conf 0.96)
  - desc: Visual signal devices must be installed in addition to audible devices in buildings with fire alarm systems, conforming to CAN/ULC-S526, and be visible within suites.
  - values: n/a
  - pages: [109]
  - source: ma-barrier-free-design-guide-fifth-edition-2017.md

- **Assistive Listening at Service Counters** (id: sens_new_001, conf 0.95)
  - desc: At least one service counter in assembly occupancy buildings must have an assistive listening system or adaptive technology, and amplification if there is a communication barrier.
  - values: n/a
  - pages: [25]
  - source: ma-accessibility-design-guide-2024.md

- **Assistive Listening Systems in Public Areas** (id: sens_new_001, conf 0.95)
  - desc: Install assistive listening devices (ALDs) in all areas where occupancy might be 50 persons or more; public areas requiring PA systems for safety must have magnetic induction loop systems.
  - values: n/a
  - pages: [90]
  - source: ma-accessibility-design-guide-2024.md

- **Induction Loop Receiver Ratio** (id: sens_new_002, conf 0.95)
  - desc: Where an induction loop system is deployed, provide 1 loop receiver for every 50 occupants for those without compatible hearing aids.
  - values: {'ratio': '1 receiver per 50 occupants'}
  - pages: [90]
  - source: ma-accessibility-design-guide-2024.md

- **Annual ALD and Loop System Testing** (id: sens_new_003, conf 0.95)
  - desc: All ALDs and induction loop installations must be checked once per year and a Certificate of Conformity issued in accordance with IEC60118-4 2014 Standard.
  - values: n/a
  - pages: [90]
  - source: ma-accessibility-design-guide-2024.md


## social_health

- **Adult Changing Facility** (id: soc_003, conf 0.98)
  - desc: Adult change tables must have a minimum clear floor space of 900 by 1830 mm in front, and be height adjustable from 450–500 mm (low) to 850–900 mm (high).
  - values: {'clear_space_width_mm': '900', 'clear_space_length_mm': '1830', 'height_low_min_mm': '450', 'height_low_max_mm': '500', 'height_high_min_mm': '850', 'height_high_max_mm': '900'}
  - pages: [69]
  - source: ma-accessibility-design-guide-2024.md

- **Multilingual Signage** (id: soc_004, conf 0.90)
  - desc: Standards must be available in multiple formats, including plain-language, ASL, and LSQ summaries, to ensure accessibility for diverse users.
  - values: {'text': 'plain-language, ASL, LSQ'}
  - pages: [9]
  - source: standard-accessiblereadyhousing-2-8-2025.md ⚠ conflict


