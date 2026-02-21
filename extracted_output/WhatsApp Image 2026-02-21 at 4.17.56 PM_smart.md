# Accessibility Extraction Report

- **Source:** `WhatsApp Image 2026-02-21 at 4.17.56 PM.jpeg`
- **Building type:** housing
- **Input type:** image
- **Model:** gpt-4.1
- **Address:** 6820 106ST NW, EDMONTON T6H2W2
- **Coordinates:** 53.5054235, -113.5048268

## Notes
This is a residential floor plan for a single-family home. The diagram includes room labels, dimensions, and some features (e.g., showers, tubs, laundry) that may be suitable for accessibility modifications. No explicit accessibility signage, routes, or alert systems are visible. No multilingual signage or sensory alerts are indicated. No explicit measurements for door widths or maneuvering clearances are provided, but doors and open spaces are drawn.

## Found Requirements

### physical_access
- **Door Minimum Width** (confidence: 70%)
  - Multiple doors are drawn and labeled throughout the floor plan, indicating the presence of doors that may be assessed for minimum width.
- **Accessible-Ready Bathroom Showers** (confidence: 70%)
  - Master bathroom shows a shower area labeled 'SHWR' with dimensions (4-0 x 5-6), which may be suitable for accessibility modifications.
  - `shower_size`: 4-0 x 5-6
- **Accessible-Ready Bathroom Bathtubs** (confidence: 70%)
  - Bath 2 includes a labeled 'TUB/SHWR' area, indicating a bathtub/shower combination that could be modified for accessibility.
- **Accessible-Ready Kitchens** (confidence: 70%)
  - Kitchen is clearly labeled and centrally located, with open access from multiple rooms, suggesting potential for accessible design.
  - `kitchen_size`: 10-4 x 18-0
- **Accessible-Ready Bedrooms** (confidence: 70%)
  - Three bedrooms are labeled and appear to have direct access from hallways, which may support accessible design.
  - `master_bedroom`: 13-0 x 15-0
  - `bedroom_2`: 12-0 x 11-0
  - `bedroom_3`: 11-10 x 11-4
- **Accessible-Ready Laundry Rooms** (confidence: 70%)
  - Laundry room is labeled and located near the master bedroom, with a door for access.
  - `laundry_size`: 8-8 x 8-0

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
