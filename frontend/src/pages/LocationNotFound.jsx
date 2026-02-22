import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import backButton from "../assets/images/back-button.png";
import logo from "../assets/images/hacked-logo.png";
import locationNotFoundIcon from "../assets/images/location-not-found.png";
import { saveLocation } from "../services/api";

function LocationNotFound() {
  const location = useLocation();
  const navigate = useNavigate();
  const { fileName: stateFileName, address: extractedAddress } = location.state || {};
  // Fall back to sessionStorage so the filename survives a page refresh
  const fileName = stateFileName || sessionStorage.getItem("sidequest_pending_filename") || undefined;
  // Pre-populate with whatever the AI extracted (so the user can confirm/correct it)
  const [address, setAddress] = useState(extractedAddress || "");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const handleAddToMap = async () => {
    if (!address.trim()) return;
    setSaving(true);
    setError(null);
    try {
      const result = await saveLocation({ address: address.trim(), lat: null, lng: null, sourceDoc: fileName });
      navigate(`/final-score?id=${result.id}`);
    } catch (e) {
      console.error("Failed to save location", e);
      setError(
        e.response?.data?.error ||
          "Could not find that address. Please try a more specific address (e.g. include city and province).",
      );
    } finally {
      setSaving(false);
    }
  };

  return (
    <section className="location-status-page" aria-label="Location not found">
      <Link className="location-status-back" to="/score-project" aria-label="Back to score project">
        <img src={backButton} alt="Back" />
      </Link>

      <div className="location-status-content">
        <img className="location-status-icon" src={locationNotFoundIcon} alt="" aria-hidden="true" />
        <h1 className="location-status-title">Location Required for Heatmap</h1>
        <h2 className="location-status-address">[address not detected]</h2>
        <p className="location-status-copy">
          We couldn't find an address in your file. To contribute this audit to the public accessibility map, please
          enter the project location below.
        </p>
        <input
          className="location-status-input"
          type="text"
          placeholder="Enter project address or postal code"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
        />
        {error ? <p className="location-status-error">{error}</p> : null}
        <div className="location-status-actions">
          <button
            className="location-status-yes"
            type="button"
            onClick={handleAddToMap}
            disabled={saving || !address.trim()}
          >
            {saving ? "Saving…" : "Yes, add to Map"}
          </button>
          <Link className="location-status-private" to="/home">
            Keep private
          </Link>
        </div>
      </div>

      <img className="location-status-logo" src={logo} alt="Hacked logo" />
    </section>
  );
}

export default LocationNotFound;
