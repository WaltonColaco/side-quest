# Accessibility Extraction Report

- **Source:** `floorplan5.txt`
- **Building type:** housing
- **Input type:** text
- **Model:** gpt-4.1

## Notes
Only basic room types are mentioned; no explicit accessibility features or measurements are provided. Accessibility readiness is inferred based on the presence of kitchen, bathroom, and rooms, but not confirmed.

## Found Requirements

### physical_access
- **Accessible-Ready Kitchens** (confidence: 50%)
  - Kitchen is present in the house layout.
- **Accessible-Ready Bedrooms** (confidence: 50%)
  - 2 rooms are present, which could be bedrooms.
- **Accessible-Ready Bathroom Showers** (confidence: 50%)
  - Bathroom is present in the house layout.

## Not Found

### social_health
- Multilingual Signage

### physical_access
- Accessible Routes
- Alternate Accessible Routes (Stair Alternatives)
- Door Minimum Width
- Accessible Maneuvering Area at Doors
- Accessible-Ready Bathroom Bathtubs
- Accessible-Ready Bathroom Medicine Cabinets
- Accessible-Ready Laundry Rooms
- Operating Controls Height and Reach
- Mobility Device Space in Meeting Rooms

### sensory_alerts
- Audible and Visual Alerts
