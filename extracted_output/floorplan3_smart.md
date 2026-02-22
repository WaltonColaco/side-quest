# Accessibility Extraction Report

- **Source:** `floorplan3.jpg`
- **Building type:** housing
- **Input type:** image
- **Model:** gpt-4.1

## Notes
This is a residential floor plan with labeled rooms and measurements. No explicit accessibility measurements, signage, or alert systems are visible. No location information is present.

## Found Requirements

### physical_access
- **Door Minimum Width** (confidence: 70%)
  - Multiple doors are drawn throughout the floor plan, indicating the presence of doorways. Exact widths are not labeled.
- **Accessible-Ready Bathroom Showers** (confidence: 70%)
  - Bathrooms are present in the Suite and near Bedrooms 2 and 3. Showers are visually indicated in the Suite bathroom.
- **Accessible-Ready Bathroom Bathtubs** (confidence: 70%)
  - Bathtubs are visually indicated in the bathrooms near Bedrooms 2 and 3.
- **Accessible-Ready Kitchens** (confidence: 70%)
  - Kitchen area is clearly labeled and centrally located, with open access to dining and family rooms.
- **Accessible-Ready Bedrooms** (confidence: 70%)
  - Bedrooms (Suite, Br.2, Br.3) are labeled and accessible from main hallways.
- **Accessible-Ready Laundry Rooms** (confidence: 70%)
  - Laundry area (labeled 'D W T') is present near the garage and kitchen.
- **Accessible Routes** (confidence: 70%)
  - Continuous hallways and open spaces connect major rooms, suggesting accessible routes.

## Not Found

### social_health
- Multilingual Signage

### physical_access
- Alternate Accessible Routes (Stair Alternatives)
- Accessible Maneuvering Area at Doors
- Accessible-Ready Bathroom Medicine Cabinets
- Operating Controls Height and Reach
- Mobility Device Space in Meeting Rooms

### sensory_alerts
- Audible and Visual Alerts
