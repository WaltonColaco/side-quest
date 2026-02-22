# Accessibility Extraction Report

- **Source:** `floorplan2.png`
- **Building type:** housing
- **Input type:** image
- **Model:** gpt-4.1
- **Location:** AdvancedHousePlans.com (visible on plan), no specific address or city

## Notes
This is a residential floor plan with labeled rooms and dimensions. No explicit accessibility features (ramps, signage, alert systems) are shown, but the layout suggests possible accessible-ready spaces. No location/address is provided beyond the plan source.

## Found Requirements

### physical_access
- **Door Minimum Width** (confidence: 70%)
  - Multiple doors are drawn throughout the floor plan, including entry, interior, and bathroom doors.
- **Accessible-Ready Kitchens** (confidence: 70%)
  - Kitchen (K.) is labeled and shown with open space and counters/island, which could allow for accessible design.
  - `dimensions`: 12 x 12
- **Accessible-Ready Bedrooms** (confidence: 70%)
  - Three bedrooms (Mbr., Br.2, Br.3) are labeled and shown with open space for maneuvering.
  - `Mbr.`: 14 x 14
  - `Br.2`: 11 x 11
  - `Br.3`: 11 x 11
- **Accessible-Ready Laundry Rooms** (confidence: 70%)
  - Laundry room is labeled and shown with washer/dryer space.
- **Accessible-Ready Bathroom Showers** (confidence: 70%)
  - Master bathroom (Mbr.) shows a separate shower area.
- **Accessible-Ready Bathroom Bathtubs** (confidence: 70%)
  - Master bathroom (Mbr.) shows a bathtub labeled 'Tub'.
- **Accessible-Ready Bathroom Medicine Cabinets** (confidence: 50%)
  - Bathrooms are labeled with vanities and storage, which could include medicine cabinets.
- **Accessible-Ready Laundry Rooms** (confidence: 70%)
  - Laundry room labeled with washer/dryer (W/D) and shelves.
- **Accessible-Ready Pantry** (confidence: 70%)
  - Pantry labeled and shown adjacent to kitchen.
  - `dimensions`: 7 x 4

## Not Found

### social_health
- Multilingual Signage

### physical_access
- Accessible Routes
- Alternate Accessible Routes (Stair Alternatives)
- Accessible Maneuvering Area at Doors
- Operating Controls Height and Reach
- Mobility Device Space in Meeting Rooms

### sensory_alerts
- Audible and Visual Alerts
