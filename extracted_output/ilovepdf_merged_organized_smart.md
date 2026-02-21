# Accessibility Extraction Report

- **Source:** `ilovepdf_merged_organized.pdf`
- **Building type:** commercial
- **Input type:** pdf
- **Model:** gpt-4.1

## Notes
The document consists of floor plans for a multi-level public/commercial building (library). Accessibility features such as elevators, ramps, wide corridors, and clear wayfinding are visually present. There is no explicit mention or depiction of tactile, braille, or assistive listening systems. No adult changing facilities are marked. Multilingual signage is inferred from the presence of a 'World Languages' section. Most accessibility features are visually implied rather than explicitly measured or described.

## Found Requirements

### physical_access
- **Accessible Routes** (confidence: 100%)
  - Accessible routes are indicated on all floor plans (pages 2-6) by the presence of elevators, ramps, and wide corridors connecting major rooms and entrances.
- **Ramps** (confidence: 100%)
  - Ramps are visually marked on Level 1 (page 3, 'ACCESS RAMP', 'CUSTOMER SERVICE RAMP') and Level 2 (page 4, 'RAMP').
- **Alternate Accessible Routes (Stair Alternatives)** (confidence: 100%)
  - Elevators are present on every floor plan (pages 2-6), providing alternatives to stairs.
- **Exterior Building Entrances** (confidence: 100%)
  - Main entrances/exits are clearly marked on Level 1 (page 3: 'MAIN ENTRANCE / EXIT', 'SOUTH ENTRANCE / EXIT', 'SECOND CUP ENTRANCE').
- **Door Minimum Width** (confidence: 70%)
  - Doors are visually present throughout all floor plans (pages 2-6), especially at entrances, washrooms, and meeting rooms.
- **Mobility Device Space in Meeting Rooms** (confidence: 70%)
  - Meeting rooms and community rooms are shown with open layouts (pages 2, 4, 6), suggesting space for mobility devices.

### neurodivergent
- **Clear Wayfinding Signage** (confidence: 100%)
  - Wayfinding is supported by labeled rooms, color-coded areas, and map legends on all floor plans (pages 2-6).
- **Pattern and Colour Blocking for Key Access** (confidence: 100%)
  - Distinct color blocks are used to differentiate areas and functions on all floor plans (pages 2-6).
- **Non-Text Diagrams and Symbols** (confidence: 100%)
  - Symbols for elevators, stairs, washrooms, and other features are used throughout the maps (pages 2-6).
- **High Colour Contrast for Orientation Signs** (confidence: 100%)
  - Maps use high-contrast colors for different zones and legends (pages 2-6).

### sensory_alerts
- **Audible and Visual Alerts** (confidence: 100%)
  - Audio Tour icons are present on all floor plans (pages 2-5), indicating the availability of auditory information.
- **Visual Contrast Between Walls and Floors** (confidence: 70%)
  - Floor plans use distinct color zones to differentiate spaces, suggesting visual contrast (pages 2-6).

### social_health
- **Multilingual Signage** (confidence: 70%)
  - Presence of 'WORLD LANGUAGES' section on Level 3 (page 5) implies multilingual resources and likely signage.

## Not Found

### physical_access
- Automatic Door Operation
- Accessible Viewing Space Dimensions
- Maintain Required Aisle Width Behind Accessible Seating
- Limits of Protruding Objects
- Wheel Stops to Prevent Vehicle Intrusion
- Curb Ramp Detectability

### neurodivergent
- Braille, Visual, and Audio Cues
- Tactile Signs for Doors and Openings
- Tactile Signage Requirements
- Accessible Control Mounting Height
- Accessible Control Operation
- Haptic and Tactile Maps
- Lighting, Audible, Tactile, Colour/Contrast, and Ergonomic Cues
- Quiet Space Availability

### sensory_alerts
- Warning Indicators
- Tactile Attention Indicator Configuration
- Tactile Attention Indicator Installation
- Tactile Direction Indicator Configuration
- Fire Alarm Sound Pressure Levels
- Visual Signal Device Installation
- Assistive Listening at Service Counters
- Assistive Listening Systems in Public Areas
- Induction Loop Receiver Ratio
- Annual ALD and Loop System Testing

### social_health
- Adult Changing Facility
