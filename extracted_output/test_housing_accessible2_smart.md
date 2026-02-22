# Accessibility Extraction Report

- **Source:** `test_housing_accessible2.txt`
- **Building type:** housing
- **Input type:** text
- **Model:** gpt-4.1

## Notes
All listed accessibility features meet or exceed Canadian accessibility standards (CSA B651, CSA B652, NBC). The home is designed for future accessibility upgrades, with structural, electrical, and plumbing provisions for retrofits. Additional enhancements such as lever handles, smart controls, non-glare lighting, color-contrast edges, accessible patio ramp (1:12), and wide parking space further support accessibility. No address or location information was provided.

## Found Requirements

### social_health

- **Multilingual Signage** (confidence: 100%)
  - All signage provided in plain language English, ASL and LSQ video QR codes, high-contrast large-font text, and Braille labels on room signage.
  - `languages`: English, ASL, LSQ
  - `braille`: yes
  - `high_contrast`: yes

### physical_access

- **Accessible Routes** (confidence: 100%)
  - Exterior pathways minimum 1500 mm width, interior pathways minimum 1200 mm width, no-step entry at main entrance, slip-resistant flooring.
  - `exterior_pathway_width_mm`: 1500
  - `interior_pathway_width_mm`: 1200
  - `no_step_entry`: yes

- **Alternate Accessible Routes (Stair Alternatives)** (confidence: 100%)
  - Structural framing allows future installation of lift/elevating device for second floor; electrical and plumbing pre-routed for retrofit.
  - `future_lift_ready`: yes

- **Door Minimum Width** (confidence: 100%)
  - Minimum clear doorway width 900 mm (exceeds 860 mm requirement); bedrooms have 900 mm door clearance.
  - `door_width_mm`: 900

- **Accessible Maneuvering Area at Doors** (confidence: 100%)
  - Maneuvering clearance: pull side 600 mm, push side 300 mm; level threshold transitions.
  - `pull_side_clearance_mm`: 600
  - `push_side_clearance_mm`: 300

- **Accessible-Ready Bathroom Showers** (confidence: 100%)
  - Bathroom is retrofit-ready for roll-in shower; reinforced walls for grab bars.
  - `roll_in_shower_ready`: yes

- **Accessible-Ready Bathroom Bathtubs** (confidence: 100%)
  - Bathtub reinforcement for future accessible installation.
  - `bathtub_reinforced`: yes

- **Accessible-Ready Bathroom Medicine Cabinets** (confidence: 100%)
  - Medicine cabinet adjustable height ready.
  - `adjustable_height`: yes

- **Accessible-Ready Kitchens** (confidence: 100%)
  - Kitchen has adjustable-height counters (future retrofit ready), 1200 mm clearance between counters, reinforced walls for grab bars, insulated and accessible sink plumbing.
  - `counter_clearance_mm`: 1200
  - `adjustable_counters`: future ready

- **Accessible-Ready Bedrooms** (confidence: 100%)
  - Bedrooms have 900 mm door clearance, 1200 mm bed clearance on both sides, structural reinforcement for ceiling lift installation.
  - `bed_clearance_mm`: 1200
  - `ceiling_lift_ready`: yes

- **Accessible-Ready Laundry Rooms** (confidence: 100%)
  - Laundry room has front-loading washer/dryer space, 1200 mm maneuvering clearance, plumbing/electrical pre-installed for accessible retrofit.
  - `maneuvering_clearance_mm`: 1200
  - `front_loading`: yes

- **Operating Controls Height and Reach** (confidence: 100%)
  - Light switches, thermostats, and controls installed between 400–1100 mm; display panels at 1000 mm; future relocation possible between 400–1500 mm.
  - `controls_height_mm`: 400–1100
  - `display_panel_height_mm`: 1000

- **Mobility Device Space in Meeting Rooms** (confidence: 100%)
  - Meeting/Study Room: 820 mm x 1390 mm stationary space, 1800 mm turning circle, flexible furniture layout.
  - `stationary_space_mm`: 820x1390
  - `turning_circle_mm`: 1800

### sensory_alerts

- **Audible and Visual Alerts** (confidence: 100%)
  - Smoke, fire, and CO detectors include audible + flashing visual alerts; doorbell includes visual strobe; smart-home notification system sends alerts to mobile devices.
  - `detectors`: audible and visual
  - `doorbell`: visual strobe
  - `mobile_alerts`: yes
