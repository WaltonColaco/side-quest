import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.heat";
import { MapContainer, Marker, Popup, TileLayer, useMap } from "react-leaflet";
import marker2x from "leaflet/dist/images/marker-icon-2x.png";
import marker from "leaflet/dist/images/marker-icon.png";
import shadow from "leaflet/dist/images/marker-shadow.png";

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

const pins = [
  { id: "downtown", name: "Downtown Edmonton", position: [53.5444, -113.4909] },
  { id: "whyte", name: "Whyte Avenue", position: [53.5232, -113.5263] },
  { id: "west-edmonton", name: "West Edmonton", position: [53.5463, -113.5954] },
  { id: "southgate", name: "Southgate Area", position: [53.4978, -113.5144] },
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

function MapHeat() {
  const navigate = useNavigate();

  return (
    <section className="map-heat-screen" aria-label="Heatmap view">
      <Link className="map-back-link" to="/">
        Back
      </Link>
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
        <HeatLayer />
        {pins.map((pin) => (
          <Marker
            key={pin.id}
            position={pin.position}
            icon={pinIcon}
            eventHandlers={{
              click: () => navigate("/information"),
            }}
          >
            <Popup>
              {pin.name}
              <br />
              Tap pin to open information.
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </section>
  );
}

export default MapHeat;
