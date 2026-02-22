# Accessibility Extraction Report

- **Source:** `test_housing_inaccessible2.txt`
- **Building type:** housing
- **Input type:** text
- **Model:** gpt-4.1

## Notes
Some accessibility features are present but do not meet full Canadian accessibility standards. Hallways and doors are narrower than required, ramp slope is steeper than standard, and maneuvering spaces are limited. Visual alarms are incomplete. Signage is only in English and lacks braille or multilingual support.

## Found Requirements

### physical_access

- **Accessible Routes** (confidence: 70%)
  - Rear entrance has small ramp (1:10 slope); exterior path width 1100 mm.
  - `ramp_slope`: 1:10
  - `exterior_path_width_mm`: 1100

- **Accessible-Ready Kitchens** (confidence: 70%)
  - Lowered section of counter at 800 mm height; sink cabinet removable for wheelchair access.
  - `counter_height_mm`: 800
  - `sink_cabinet_removable`: yes

- **Accessible-Ready Bathroom Showers** (confidence: 70%)
  - Walk-in shower planned (900 mm wide), grab bar backing installed near toilet.
  - `shower_width_mm`: 900
  - `grab_bar_backing`: yes

- **Accessible-Ready Laundry Rooms** (confidence: 70%)
  - Front-loading washer/dryer.
  - `front_loading`: yes

- **Operating Controls Height and Reach** (confidence: 70%)
  - Some switches at 1100 mm; thermostat at 1200 mm.
  - `switch_height_mm`: 1100
  - `thermostat_height_mm`: 1200

## Not Found

### social_health
- Multilingual Signage

### physical_access
- Alternate Accessible Routes (Stair Alternatives)
- Door Minimum Width
- Accessible Maneuvering Area at Doors
- Accessible-Ready Bathroom Bathtubs
- Accessible-Ready Bathroom Medicine Cabinets
- Accessible-Ready Bedrooms
- Mobility Device Space in Meeting Rooms

### sensory_alerts
- Audible and Visual Alerts
