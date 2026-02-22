# Accessibility Extraction Report

- **Source:** `floorplan1.jpeg`
- **Building type:** housing
- **Input type:** image
- **Model:** gpt-4.1
- **Address:** 10681, 62 Ave
- **Coordinates:** 53.49894219999999, -113.5086744

## Notes
This is a floor plan for a single-level house with a double garage, three bedrooms, two bathrooms, kitchen, laundry, and patio. No explicit accessibility signage or measurements for door widths, turning radii, or controls are shown. No ramps or alternate stair-free routes are depicted, but the single-level layout may support accessibility. No visual or audible alert systems are indicated.

## Found Requirements

### physical_access
- **Door Minimum Width** (confidence: 70%)
  - Doors are visibly marked on the floor plan; standard swing doors are present throughout.
- **Accessible-Ready Bathroom Showers** (confidence: 70%)
  - Master bath shows a shower area (42"x60") which could be accessible-ready.
  - `shower_size`: 42x60 in
- **Accessible-Ready Bathroom Bathtubs** (confidence: 70%)
  - Master bath includes a bathtub (72x36 in) which could be accessible-ready.
  - `bathtub_size`: 72x36 in
- **Accessible-Ready Kitchens** (confidence: 70%)
  - Kitchen is open-plan with island and clear floor space, potentially accessible.
  - `kitchen_size`: 12'0" x 12'6"
- **Accessible-Ready Bedrooms** (confidence: 70%)
  - Bedrooms have clear floor space and standard doorways.
  - `master_suite`: 16'0" x 19'0"
  - `bedroom_1`: 11'0" x 12'0"
  - `bedroom_2`: 11'0" x 12'0"
- **Accessible-Ready Laundry Rooms** (confidence: 70%)
  - Laundry room is present and appears to have clear floor space.

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
