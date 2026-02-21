import { useEffect } from "react";
import { Link } from "react-router-dom";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.heat";
import { MapContainer, TileLayer, useMap } from "react-leaflet";

const heatData = [
  [40.7128, -74.006, 0.95],
  [40.7306, -73.9866, 0.88],
  [40.758, -73.9855, 0.91],
  [40.7061, -74.0087, 0.72],
  [40.7484, -73.9857, 0.85],
  [40.7411, -73.9897, 0.68],
  [40.7527, -73.9772, 0.83],
  [40.7295, -73.9965, 0.77],
  [40.7213, -74.0047, 0.66],
  [40.7614, -73.9776, 0.81],
];

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
  return (
    <section className="map-heat-screen" aria-label="Heatmap view">
      <Link className="map-back-link" to="/">
        Back
      </Link>
      <MapContainer
        center={[40.7306, -73.9866]}
        zoom={12}
        scrollWheelZoom
        className="map-heat-canvas"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <HeatLayer />
      </MapContainer>
    </section>
  );
}

export default MapHeat;
