# Accessibility Extraction Report

- **Source:** `floorplan4.jpeg`
- **Building type:** housing
- **Input type:** image
- **Model:** gpt-4.1
- **Address:** 10220 104 Ave NW, Edmonton, AB T5J 0H6
- **Coordinates:** 53.546971, -113.4978032

## Notes
This is a main level floor plan for a residential building. Some features such as door widths, maneuvering clearances, and specific accessibility fixtures are not explicitly labeled. There are stairs indicated (DN to basement, DN at porch), but no ramps or alternate accessible routes are shown. No signage or sensory alert systems are visible.

## Found Requirements

### physical_access
- **Accessible-Ready Bathroom Showers** (confidence: 70%)
  - A shower (SHWR 4x4) is present in the bathroom area, which could potentially be accessible-ready.
  - `shower_size_ft`: 4x4
- **Accessible-Ready Bathroom Bathtubs** (confidence: 70%)
  - A bathtub is present in Bath #1 (5x14), which could potentially be accessible-ready.
  - `bathroom_size_ft`: 5x14
- **Accessible-Ready Kitchens** (confidence: 70%)
  - Kitchen (10x11) is labeled and shown with open space, potentially allowing for accessible design.
  - `kitchen_size_ft`: 10x11
- **Accessible-Ready Bedrooms** (confidence: 70%)
  - Bedroom #1 (13x14) is labeled and appears to have maneuvering space.
  - `bedroom_size_ft`: 13x14
- **Accessible Routes** (confidence: 50%)
  - Hallways and open connections between rooms suggest possible accessible routes.

## Not Found

### social_health
- Multilingual Signage

### physical_access
- Alternate Accessible Routes (Stair Alternatives)
- Door Minimum Width
- Accessible Maneuvering Area at Doors
- Accessible-Ready Bathroom Medicine Cabinets
- Accessible-Ready Laundry Rooms
- Operating Controls Height and Reach
- Mobility Device Space in Meeting Rooms

### sensory_alerts
- Audible and Visual Alerts
