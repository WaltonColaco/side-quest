# Accessibility Extraction Report

- **Source:** `floorplan1.jpg`
- **Building type:** housing
- **Input type:** image
- **Model:** gpt-4.1

## Notes
This is a residential floor plan with labeled rooms and fixtures. No explicit accessibility signage, measurements, or alerts are visible. The presence of showers, bathtubs, and labeled rooms allows inference of some accessible-ready features, but no explicit ADA or accessibility standards are indicated.

## Found Requirements

### physical_access
- **Door Minimum Width** (confidence: 70%)
  - Multiple doors are drawn throughout the floor plan, including entry, interior, and bathroom doors.
- **Accessible-Ready Bathroom Showers** (confidence: 70%)
  - Bath 2 is labeled with 'SHOWER', indicating a shower is present.
- **Accessible-Ready Bathroom Bathtubs** (confidence: 70%)
  - Master Bath is labeled with 'TUB', indicating a bathtub is present.
- **Accessible-Ready Kitchens** (confidence: 70%)
  - Kitchen is clearly labeled and centrally located with open access to adjacent rooms.
- **Accessible-Ready Bedrooms** (confidence: 70%)
  - Three bedrooms are labeled and accessible from hallways.
- **Accessible-Ready Laundry Rooms** (confidence: 70%)
  - Laundry room is labeled and located near the entry and master bedroom.

## Not Found

### social_health
- Multilingual Signage

### physical_access
- Accessible Routes
- Alternate Accessible Routes (Stair Alternatives)
- Accessible Maneuvering Area at Doors
- Accessible-Ready Bathroom Medicine Cabinets
- Operating Controls Height and Reach
- Mobility Device Space in Meeting Rooms

### sensory_alerts
- Audible and Visual Alerts
