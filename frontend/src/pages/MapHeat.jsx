import { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.heat";
import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  useMap,
  ZoomControl,
} from "react-leaflet";
import marker2x from "leaflet/dist/images/marker-icon-2x.png";
import marker from "leaflet/dist/images/marker-icon.png";
import shadow from "leaflet/dist/images/marker-shadow.png";
import plusSign from "../assets/images/plus-sign.png";
import minusSign from "../assets/images/minus-sign.png";
import { useSettings } from "../context/SettingsContext";
import SettingsCard from "../components/SettingsCard";
import { fetchFeatures, fetchLocations } from "../services/api";

const heatData = [
  [53.5444, -113.4909, 0.96], // Downtown
  [53.5461, -113.4938, 0.88], // Ice District
  [53.5232, -113.5263, 0.82], // Whyte Ave
  [53.5408, -113.505, 0.78], // River Valley central
  [53.5463, -113.5954, 0.74], // West Edmonton
  [53.5717, -113.428, 0.69], // Northeast Edmonton
  [53.4978, -113.5144, 0.71], // Southgate area
  [53.5585, -113.4186, 0.65], // Highlands
  [53.5157, -113.6158, 0.63], // Callingwood
  [53.5895, -113.4077, 0.6], // Northlands area
];

const basePins = [
  {
    id: "downtown",
    name: "Downtown Edmonton",
    position: [53.5444, -113.4909],
    ramp: false,
    powerDoors: false,
    elevator: false,
  },
  {
    id: "whyte",
    name: "Whyte Avenue",
    position: [53.5232, -113.5263],
    ramp: false,
    powerDoors: false,
    elevator: false,
  },
  {
    id: "west-edmonton",
    name: "West Edmonton",
    position: [53.5463, -113.5954],
    ramp: false,
    powerDoors: false,
    elevator: false,
  },
  {
    id: "southgate",
    name: "Southgate Area",
    position: [53.4978, -113.5144],
    ramp: false,
    powerDoors: false,
    elevator: false,
  },
];

const pinIcon = L.icon({
  iconRetinaUrl: marker2x,
  iconUrl: marker,
  shadowUrl: shadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

function HeatLayer() {
  const map = useMap();

  useEffect(() => {
    const layer = L.heatLayer(heatData, {
      radius: 30,
      blur: 20,
      maxZoom: 17,
      minOpacity: 0.35,
    });

    layer.addTo(map);

    return () => {
      map.removeLayer(layer);
    };
  }, [map]);

  return null;
}

function MapHeat({ showSettings: initialShowSettings = false }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { state } = useSettings();
  const [showSettings, setShowSettings] = useState(
    initialShowSettings || location.pathname === "/settings"
  );
  const [showLegend, setShowLegend] = useState(false);
  const [featureFlags, setFeatureFlags] = useState({ ramp: false, powerDoors: false, elevator: false });
  const [dynamicPins, setDynamicPins] = useState([]);

  useEffect(() => {
    setShowSettings(initialShowSettings || location.pathname === "/settings");
  }, [initialShowSettings, location.pathname]);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchFeatures();
        setFeatureFlags(data);
      } catch (e) {
        console.error("Failed to load features", e);
      }
    };
    load();
  }, []);

  useEffect(() => {
    const loadLocs = async () => {
      try {
        const data = await fetchLocations();
        const pins = (data || [])
          .filter((d) => d.latitude && d.longitude)
          .map((d) => ({
            id: `loc-${d.id}`,
            name: d.name || d.address || d.source_doc || "Analyzed Location",
            address: d.address,
            position: [d.latitude, d.longitude],
            ramp: featureFlags.ramp,
            powerDoors: featureFlags.powerDoors,
            elevator: featureFlags.elevator,
          }));
        setDynamicPins(pins);
      } catch (e) {
        console.error("Failed to load location", e);
      }
    };
    loadLocs();
  }, [featureFlags]);

  const pins = useMemo(() => {
    const mapped = basePins.map((p) => ({
      ...p,
      ramp: featureFlags.ramp,
      powerDoors: featureFlags.powerDoors,
      elevator: featureFlags.elevator,
    }));
    return [...dynamicPins, ...mapped];
  }, [featureFlags, dynamicPins]);

  const filteredPins = useMemo(() => {
    return pins.filter((pin) => {
      if (state.filters.ramp && !pin.ramp) return false;
      if (state.filters.powerDoors && !pin.powerDoors) return false;
      if (state.filters.elevator && !pin.elevator) return false;
      return true;
    });
  }, [state.filters]);

  return (
    <section className="map-heat-screen" aria-label="Heatmap view">
      <button
        type="button"
        className="legend-toggle"
        onClick={() => setShowLegend((prev) => !prev)}
        aria-label={showLegend ? "Hide legend" : "Show legend"}
      >
        <img src={showLegend ? minusSign : plusSign} alt="" aria-hidden="true" />
      </button>

      {showLegend ? (
        <aside className="map-legend" aria-label="Map legend">
          <h2 className="map-legend-title">Legend</h2>
          <div className="map-legend-dots" role="list">
            <div className="map-legend-row" role="listitem">
              <span className="map-legend-dot dot-1" />
              <span className="map-legend-label">0%-20%</span>
            </div>
            <div className="map-legend-row" role="listitem">
              <span className="map-legend-dot dot-2" />
              <span className="map-legend-label">20%-40%</span>
            </div>
            <div className="map-legend-row" role="listitem">
              <span className="map-legend-dot dot-3" />
              <span className="map-legend-label">40%-60%</span>
            </div>
            <div className="map-legend-row" role="listitem">
              <span className="map-legend-dot dot-4" />
              <span className="map-legend-label">60%-80%</span>
            </div>
            <div className="map-legend-row" role="listitem">
              <span className="map-legend-dot dot-5" />
              <span className="map-legend-label">80%-100%</span>
            </div>
          </div>
        </aside>
      ) : null}

      <MapContainer
        center={[53.5461, -113.4938]}
        zoom={12}
        zoomControl={false}
        scrollWheelZoom
        className="map-heat-canvas"
      >
        <ZoomControl position="bottomright" />
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <HeatLayer />
        {filteredPins.map((pin) => (
          <Marker
            key={pin.id}
            position={pin.position}
            icon={pinIcon}
            eventHandlers={{
              click: () => navigate("/information"),
            }}
          >
            <Popup>
              <div className="pin-popup">
                <div className="pin-popup-score">
                  {pin.score !== undefined && pin.score !== null ? `${Math.round(pin.score * 100)}%` : "—"}
                </div>
                <div className="pin-popup-address">{pin.address || pin.name}</div>
                <div className="pin-popup-tags">
                  {pin.ramp ? "✓ Ramp" : "✕ Ramp"}
                  {" • "}
                  {pin.powerDoors ? "✓ Power doors" : "✕ Power doors"}
                  {" • "}
                  {pin.elevator ? "✓ Elevator" : "✕ Elevator"}
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      {showSettings && (
        <div className="settings-overlay">
          <SettingsCard
            onClose={() => {
              setShowSettings(false);
              if (location.pathname === "/settings") navigate("/map-heat");
            }}
          />
        </div>
      )}
    </section>
  );
}

export default MapHeat;
