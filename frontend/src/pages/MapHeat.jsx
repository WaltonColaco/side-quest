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
import { fetchFeatures, fetchLocations, geocodeSearch } from "../services/api";

function getScoreColor(score) {
  if (score === null || score === undefined) return "#274b7b";
  if (score < 0.2) return "#274b7b";
  if (score < 0.4) return "#80b7cf";
  if (score < 0.6) return "#a5be83";
  if (score < 0.8) return "#ccc272";
  return "#e8c84f";
}

function createColoredIcon(color) {
  return L.divIcon({
    className: "",
    html: `<svg xmlns="http://www.w3.org/2000/svg" width="25" height="41" viewBox="0 0 25 41">
      <path d="M12.5 0C5.596 0 0 5.596 0 12.5c0 9.375 12.5 28.5 12.5 28.5S25 21.875 25 12.5C25 5.596 19.404 0 12.5 0z" fill="${color}" stroke="#fff" stroke-width="1.5"/>
      <circle cx="12.5" cy="12.5" r="5" fill="#fff" opacity="0.7"/>
    </svg>`,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [0, -41],
  });
}

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

function SearchZoomController({ query, pins, onSearchResult }) {
  const map = useMap();

  useEffect(() => {
    const q = (query || "").trim();
    if (!q) return;

    const normalized = q.toLowerCase();
    const localMatch = pins.find((pin) => {
      const address = (pin.address || "").toLowerCase();
      const name = (pin.name || "").toLowerCase();
      return address.includes(normalized) || name.includes(normalized);
    });

    if (localMatch) {
      map.setView(localMatch.position, 15, { animate: true });
      onSearchResult?.({ ok: true });
      return;
    }

    const bounds = map.getBounds();
    const south = bounds.getSouth();
    const west = bounds.getWest();
    const north = bounds.getNorth();
    const east = bounds.getEast();
    const boundedQuery = `${q} within ${south.toFixed(4)},${west.toFixed(4)} to ${north.toFixed(4)},${east.toFixed(4)}`;

    let cancelled = false;
    const runGeocode = async () => {
      try {
        let result = null;
        try {
          result = await geocodeSearch(q);
        } catch {
          result = await geocodeSearch(boundedQuery);
        }
        if (cancelled || !result) return;

        const lat = Number.parseFloat(result.lat);
        const lon = Number.parseFloat(result.lng);
        if (Number.isNaN(lat) || Number.isNaN(lon)) return;
        map.setView([lat, lon], 14, { animate: true });
        onSearchResult?.({ ok: true });
      } catch (error) {
        const statusCode = error?.response?.status;
        if (statusCode === 404) {
          onSearchResult?.({
            ok: false,
            message: "Location not found. Try a full address or postal code.",
          });
          return;
        }
        onSearchResult?.({
          ok: false,
          message: "Search failed. Please try again.",
        });
        console.error("Search geocoding failed", error);
      }
    };
    runGeocode();
    return () => {
      cancelled = true;
    };
  }, [map, pins, query]);

  return null;
}

function MapHeat({ showSettings: initialShowSettings = false }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { state } = useSettings();
  const [showSettings, setShowSettings] = useState(
    initialShowSettings || location.pathname === "/settings",
  );
  const [showLegend, setShowLegend] = useState(false);
  const [featureFlags, setFeatureFlags] = useState({
    ramp: false,
    powerDoors: false,
    elevator: false,
  });
  const [dynamicPins, setDynamicPins] = useState([]);
  const [heatPoints, setHeatPoints] = useState([]);
  const [searchMessage, setSearchMessage] = useState("");

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
        const heat = located.map((d) => [
          d.latitude,
          d.longitude,
          d.score ?? 0.5,
        ]);
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

  const themeClass = [
    state.theme.darkMode ? "map-dark" : "",
    state.theme.highContrast ? "map-high-contrast" : "",
  ]
    .filter(Boolean)
    .join(" ");
  const searchQuery = useMemo(() => new URLSearchParams(location.search).get("q") || "", [location.search]);

  useEffect(() => {
    if (!searchMessage) return;
    const timer = setTimeout(() => setSearchMessage(""), 3000);
    return () => clearTimeout(timer);
  }, [searchMessage]);

  return (
    <section
      className={`map-heat-screen${themeClass ? ` ${themeClass}` : ""}`}
      aria-label="Heatmap view"
    >
      <button
        type="button"
        className="legend-toggle"
        onClick={() => setShowLegend((prev) => !prev)}
        aria-label={showLegend ? "Hide legend" : "Show legend"}
      >
        <img
          src={showLegend ? minusSign : plusSign}
          alt=""
          aria-hidden="true"
        />
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

      {searchMessage ? (
        <div className="map-search-message" role="status" aria-live="polite">
          {searchMessage}
        </div>
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
        <SearchZoomController
          query={searchQuery}
          pins={filteredPins}
          onSearchResult={({ ok, message }) => {
            if (ok) setSearchMessage("");
            else setSearchMessage(message || "Location not found.");
          }}
        />
        <HeatLayer data={heatPoints} />
        {filteredPins.map((pin) => (
          <Marker
            key={pin.id}
            position={pin.position}
            icon={createColoredIcon(getScoreColor(pin.score))}
              eventHandlers={{
                click: () =>
                  navigate(`/information?id=${pin.id.replace("loc-", "")}`, {
                    state: { score: pin.score, address: pin.address || null },
                  }),
              }}
            >
            <Popup>
              <div className="pin-popup">
                <div className="pin-popup-score">
                  {pin.score !== undefined && pin.score !== null
                    ? `${Math.round(pin.score * 100)}%`
                    : "—"}
                </div>
                <div className="pin-popup-address">
                  {pin.address || pin.name}
                </div>
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
