import { useEffect, useMemo, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.heat";
import { MapContainer, Marker, Popup, TileLayer, useMap } from "react-leaflet";
import marker2x from "leaflet/dist/images/marker-icon-2x.png";
import marker from "leaflet/dist/images/marker-icon.png";
import shadow from "leaflet/dist/images/marker-shadow.png";
import { useSettings } from "../context/SettingsContext";
import SettingsCard from "../components/SettingsCard";
import { fetchFeatures, fetchLocations } from "../services/api";


const pinIcon = L.icon({
  iconRetinaUrl: marker2x,
  iconUrl: marker,
  shadowUrl: shadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

function HeatLayer({ data }) {
  const map = useMap();

  useEffect(() => {
    if (!data.length) return;
    const layer = L.heatLayer(data, {
      radius: 30,
      blur: 20,
      maxZoom: 17,
      minOpacity: 0.35,
    });

    layer.addTo(map);

    return () => {
      map.removeLayer(layer);
    };
  }, [map, data]);

  return null;
}

function MapHeat({ showSettings: initialShowSettings = false }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { state } = useSettings();
  const [showSettings, setShowSettings] = useState(
    initialShowSettings || location.pathname === "/settings"
  );
  const [featureFlags, setFeatureFlags] = useState({ ramp: false, powerDoors: false, elevator: false });
  const [dynamicPins, setDynamicPins] = useState([]);
  const [heatPoints, setHeatPoints] = useState([]);

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
        const located = (data || []).filter((d) => d.latitude && d.longitude);
        const pins = located.map((d) => ({
          id: `loc-${d.id}`,
          name: d.name || d.address || d.source_doc || "Analyzed Location",
          address: d.address,
          score: d.score,
          position: [d.latitude, d.longitude],
          ramp: featureFlags.ramp,
          powerDoors: featureFlags.powerDoors,
          elevator: featureFlags.elevator,
        }));
        const heat = located.map((d) => [d.latitude, d.longitude, d.score ?? 0.5]);
        setDynamicPins(pins);
        setHeatPoints(heat);
      } catch (e) {
        console.error("Failed to load location", e);
      }
    };
    loadLocs();
  }, [featureFlags]);

  const filteredPins = useMemo(() => {
    return dynamicPins.filter((pin) => {
      if (state.filters.ramp && !pin.ramp) return false;
      if (state.filters.powerDoors && !pin.powerDoors) return false;
      if (state.filters.elevator && !pin.elevator) return false;
      return true;
    });
  }, [dynamicPins, state.filters]);

  return (
    <section className="map-heat-screen" aria-label="Heatmap view">
      <Link className="map-back-link" to="/">
        Back
      </Link>
      <button className="floating-settings" type="button" onClick={() => setShowSettings(true)}>
        Settings
      </button>
      <MapContainer
        center={[53.5461, -113.4938]}
        zoom={12}
        scrollWheelZoom
        className="map-heat-canvas"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <HeatLayer data={heatPoints} />
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
