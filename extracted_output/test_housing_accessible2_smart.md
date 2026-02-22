# Accessibility Extraction Report

- **Source:** `test_housing_accessible2.txt`
- **Building type:** housing
- **Input type:** text
- **Model:** gpt-4.1

## Notes
The content provides comprehensive details on accessibility features, including specific measurements and future-ready design elements for physical access, sensory alerts, and social inclusivity. All listed requirements are addressed explicitly.

## Found Requirements

### social_health

- **Multilingual Signage** (confidence: 100%)
  - All signage provided in plain language English, ASL video QR codes, LSQ video QR codes; high-contrast, large-font text; Braille labels on room signage.
  - `languages`: English, ASL, LSQ
  - `features`: high-contrast, large-font, Braille

### physical_access

- **Accessible Routes** (confidence: 100%)
  - Exterior pathways minimum 1500 mm width, interior pathways minimum 1200 mm width, no-step entry at main entrance, slip-resistant flooring throughout.
  - `exterior_pathway_width_mm`: 1500
  - `interior_pathway_width_mm`: 1200
  - `no_step_entry`: True
  - `slip_resistant`: True

- **Alternate Accessible Routes (Stair Alternatives)** (confidence: 100%)
  - Structural framing allows future installation of lift/elevating device for second floor; accessible outdoor patio with ramp (1:12 slope).
  - `lift_ready`: True
  - `ramp_slope`: 1:12

- **Door Minimum Width** (confidence: 100%)
  - Minimum clear doorway width: 900 mm (exceeds 860 mm requirement); bedroom door clearance: 900 mm.
  - `door_width_mm`: 900

- **Accessible Maneuvering Area at Doors** (confidence: 100%)
  - Maneuvering clearance: pull side 600 mm, push side 300 mm; level threshold transitions.
  - `pull_side_clearance_mm`: 600
  - `push_side_clearance_mm`: 300
  - `level_threshold`: True

- **Accessible-Ready Bathroom Showers** (confidence: 100%)
  - Bathroom is roll-in shower retrofit-ready; reinforced walls for grab bars.
  - `roll_in_shower_ready`: True
  - `grab_bar_reinforcement`: True

- **Accessible-Ready Bathroom Bathtubs** (confidence: 100%)
  - Bathtub reinforcement for future accessible installation.
  - `bathtub_reinforcement`: True

- **Accessible-Ready Bathroom Medicine Cabinets** (confidence: 100%)
  - Medicine cabinet adjustable height ready.
  - `adjustable_height`: True

- **Accessible-Ready Kitchens** (confidence: 100%)
  - Adjustable-height counters (future retrofit ready), 1200 mm clearance between counters, reinforced walls for grab bars, sink plumbing insulated and positioned for wheelchair access.
  - `adjustable_counters`: True
  - `counter_clearance_mm`: 1200
  - `grab_bar_reinforcement`: True
  - `sink_accessible`: True

- **Accessible-Ready Bedrooms** (confidence: 100%)
  - Door clearance 900 mm, bed clearance on both sides 1200 mm, structural reinforcement for ceiling lift installation.
  - `door_width_mm`: 900
  - `bed_clearance_mm`: 1200
  - `ceiling_lift_ready`: True

- **Accessible-Ready Laundry Rooms** (confidence: 100%)
  - Front-loading washer/dryer space, 1200 mm maneuvering clearance, plumbing/electrical pre-installed for accessible retrofit.
  - `front_loading`: True
  - `maneuvering_clearance_mm`: 1200
  - `retrofit_ready`: True

- **Operating Controls Height and Reach** (confidence: 100%)
  - Light switches, thermostats, and controls installed between 400–1100 mm; display panels at 1000 mm; future relocation possible between 400–1500 mm.
  - `controls_height_mm`: 400–1100
  - `display_panel_height_mm`: 1000
  - `future_range_mm`: 400–1500

- **Mobility Device Space in Meeting Rooms** (confidence: 100%)
  - Meeting/Study Room: 820 mm x 1390 mm stationary space, 1800 mm turning circle, flexible furniture layout.
  - `stationary_space_mm`: 820x1390
  - `turning_circle_mm`: 1800

### sensory_alerts

- **Audible and Visual Alerts** (confidence: 100%)
  - Smoke, fire, and CO detectors include audible and flashing visual alerts; doorbell includes visual strobe signal; smart-home notification system sends alerts to mobile devices.
  - `detectors`: audible and visual
  - `doorbell`: visual strobe
  - `mobile_alerts`: True
