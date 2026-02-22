# Accessibility Extraction Report

- **Source:** `WhatsApp Image 2026-02-21 at 11.12.26 PM.jpeg`
- **Building type:** housing
- **Input type:** image
- **Model:** gpt-4.1
- **Location:** familyhomeplans.com

## Notes
This is a residential floor plan with labeled rooms and dimensions. No explicit accessibility features (such as ramps, grab bars, or signage) are shown, but several rooms (kitchen, bathrooms, bedrooms, laundry) could be adapted for accessibility. No location address or coordinates are present; only the website familyhomeplans.com is visible.

## Found Requirements

### physical_access
- **Door Minimum Width** (confidence: 70%)
  - Multiple doors are drawn throughout the floor plan, including entry, bedroom, bathroom, closet, and garage doors.
- **Accessible-Ready Bathroom Showers** (confidence: 70%)
  - Master bathroom (M. Bath) shows a separate shower area, which could be adapted for accessibility.
- **Accessible-Ready Bathroom Bathtubs** (confidence: 70%)
  - Master bathroom (M. Bath) includes a bathtub, which could be adapted for accessibility.
- **Accessible-Ready Kitchens** (confidence: 70%)
  - Kitchen layout is visible, with counters, sink, and appliances; could be adapted for accessibility.
  - `dimensions`: 12'9" x 13'6"
- **Accessible-Ready Bedrooms** (confidence: 70%)
  - Four bedrooms are shown, with clear doorways and maneuvering space.
  - `bedroom_sizes`: ['11\'6" x 11\'0"', '11\'6" x 10\'4"', '11\'6" x 10\'4"', '14\'6" x 14\'0"']
- **Accessible-Ready Laundry Rooms** (confidence: 70%)
  - Laundry room is labeled and accessible from main hallway and master bedroom.

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
