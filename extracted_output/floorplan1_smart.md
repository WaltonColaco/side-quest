# Accessibility Extraction Report

- **Source:** `floorplan1.jpg`
- **Building type:** housing
- **Input type:** image
- **Model:** gpt-4.1

## Notes
This is a residential floor plan with labeled rooms and some features that could potentially be made accessible, but no explicit accessibility measurements, signage, or compliance details are provided. No location information is visible.

## Found Requirements

### physical_access

- **Accessible-Ready Bathroom Showers** (confidence: 70%)
  - Master bath includes a labeled shower area, which could potentially be made accessible.
  - `room_label`: M. BATH
  - `shower_present`: True

- **Accessible-Ready Bathroom Bathtubs** (confidence: 70%)
  - Master bath includes a labeled tub area, which could potentially be made accessible.
  - `room_label`: M. BATH
  - `tub_present`: True

- **Accessible-Ready Kitchens** (confidence: 70%)
  - Kitchen is labeled and centrally located, with open access to adjacent rooms.
  - `room_label`: KITCHEN
  - `open_access`: True

- **Accessible-Ready Bedrooms** (confidence: 70%)
  - Multiple bedrooms are labeled and appear to have direct access from hallways.
  - `bedrooms`: 3

- **Accessible-Ready Laundry Rooms** (confidence: 70%)
  - Laundry room is labeled and accessible from main hallway.
  - `room_label`: LAUNDRY

## Not Found

### social_health
- Multilingual Signage

### physical_access
- Accessible Routes
- Alternate Accessible Routes (Stair Alternatives)
- Door Minimum Width
- Accessible Maneuvering Area at Doors
- Accessible-Ready Bathroom Medicine Cabinets
- Operating Controls Height and Reach
- Mobility Device Space in Meeting Rooms

### sensory_alerts
- Audible and Visual Alerts
