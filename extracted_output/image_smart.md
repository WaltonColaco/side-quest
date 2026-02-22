# Accessibility Extraction Report

- **Source:** `image.jpg`
- **Building type:** housing
- **Input type:** image
- **Model:** gpt-4.1
- **Address:** 6820 106ST NW, EDMONTON T6H2W2
- **Coordinates:** 53.5054235, -113.5048268

## Notes
This is a residential floor plan with labeled rooms and measurements. No explicit accessibility signage, routes, or alert systems are visible. Door widths and maneuvering spaces are inferred from the layout, but not explicitly dimensioned for accessibility. No multilingual signage or sensory alerts are present.

## Found Requirements

### physical_access
- **Door Minimum Width** (confidence: 70%)
  - Doors are visibly marked on the floor plan; standard door symbols are present throughout the house, including entry, bedrooms, bathrooms, and closets.
- **Accessible-Ready Bathroom Showers** (confidence: 70%)
  - Master bathroom includes a shower area labeled 'SHWR', which could potentially be made accessible.
- **Accessible-Ready Bathroom Bathtubs** (confidence: 70%)
  - Master bathroom and Bath 2 both show bathtub locations.
- **Accessible-Ready Kitchens** (confidence: 70%)
  - Kitchen is clearly labeled and centrally located with open access to adjacent rooms.
- **Accessible-Ready Bedrooms** (confidence: 70%)
  - Three bedrooms are labeled and accessible from main hallways.
- **Accessible-Ready Laundry Rooms** (confidence: 70%)
  - Laundry room is labeled and located near the master bedroom and entry.
- **Accessible Maneuvering Area at Doors** (confidence: 70%)
  - Entryways and rooms appear to have sufficient maneuvering space based on drawn layout.

## Not Found

### social_health
- Multilingual Signage

### physical_access
- Accessible Routes
- Alternate Accessible Routes (Stair Alternatives)
- Accessible-Ready Bathroom Medicine Cabinets
- Operating Controls Height and Reach
- Mobility Device Space in Meeting Rooms

### sensory_alerts
- Audible and Visual Alerts
