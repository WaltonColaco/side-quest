# Accessibility Extraction Report

- **Source:** `floorplan4.jpeg`
- **Building type:** housing
- **Input type:** image
- **Model:** gpt-4.1
- **Address:** 10220 104 Ave NW, Edmonton, AB T5J 0H6
- **Coordinates:** 53.546971, -113.4978032

## Notes
The floor plan provides room dimensions and layout, but does not explicitly show accessible routes, door widths, or signage. Stairs are present at the entry and to the basement, which may limit accessibility. No explicit accessibility features or measurements are labeled.

## Found Requirements

### physical_access
- **Accessible-Ready Bathroom Showers** (confidence: 70%)
  - A separate shower (SHWR 4x4) is present in Bath #1, which could potentially be made accessible.
  - `shower_size_ft`: 4x4
- **Accessible-Ready Bathroom Bathtubs** (confidence: 70%)
  - A bathtub is present in Bath #1.
  - `bathroom_size_ft`: 5x14
- **Accessible-Ready Kitchens** (confidence: 70%)
  - Kitchen is labeled and its layout is visible, allowing for potential accessibility modifications.
  - `kitchen_size_ft`: 10x11
- **Accessible-Ready Bedrooms** (confidence: 70%)
  - Bedroom #1 is labeled and its size is provided.
  - `bedroom_size_ft`: 13x14

## Not Found

### social_health
- Multilingual Signage

### physical_access
- Accessible Routes
- Alternate Accessible Routes (Stair Alternatives)
- Door Minimum Width
- Accessible Maneuvering Area at Doors
- Accessible-Ready Bathroom Medicine Cabinets
- Accessible-Ready Laundry Rooms
- Operating Controls Height and Reach
- Mobility Device Space in Meeting Rooms

### sensory_alerts
- Audible and Visual Alerts
