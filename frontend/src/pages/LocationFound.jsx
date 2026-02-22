import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import backButton from "../assets/images/back-button.png";
import logo from "../assets/images/hacked-logo.png";
import locationFoundIcon from "../assets/images/location-found.png";
import { saveLocation } from "../services/api";

function LocationFound() {
  const location = useLocation();
  const navigate = useNavigate();
  const { address, lat, lng, fileName: stateFileName } = location.state || {};
  const fileName = stateFileName || sessionStorage.getItem("sidequest_pending_filename") || undefined;
  const [saving, setSaving] = useState(false);
  const [savingPrivate, setSavingPrivate] = useState(false);
  const [error, setError] = useState(null);

  const handleAddToMap = async () => {
    setSaving(true);
    setError(null);
    try {
      const result = await saveLocation({ address, lat, lng, sourceDoc: fileName });
      navigate(`/final-score?id=${result.id}`);
    } catch (e) {
      console.error("Failed to save location", e);
      setError(e.response?.data?.error || "Failed to save location. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  const handleKeepPrivate = async () => {
    setSavingPrivate(true);
    setError(null);
    try {
      // Save a hidden/private report record using sentinel coords so it won't render on the map.
      const result = await saveLocation({
        address: address || null,
        lat: 0,
        lng: 0,
        sourceDoc: fileName,
      });
      navigate(`/final-score?id=${result.id}`);
    } catch (e) {
      console.error("Failed to save private report", e);
      setError(e.response?.data?.error || "Failed to save report. Please try again.");
    } finally {
      setSavingPrivate(false);
    }
  };

  return (
    <section
      className="location-status-page location-found-page"
      aria-label="Location found"
    >
      <Link
        className="location-status-back"
        to="/score-project"
        aria-label="Back to score project"
      >
        <img src={backButton} alt="Back" />
      </Link>

      <div className="location-status-content">
        <img
          className="location-status-icon"
          src={locationFoundIcon}
          alt=""
          aria-hidden="true"
        />
        <h1 className="location-status-title">Location Found</h1>
        <h2 className="location-status-address">{address || "[address detected]"}</h2>
        <p className="location-status-copy">
          We have detected this project location. Would you like to include this
          audit in the public accessibility heatmap?
        </p>
        {error ? <p className="location-status-error">{error}</p> : null}
        <div className="location-status-actions">
          <button
            className="location-status-yes"
            type="button"
            onClick={handleAddToMap}
            disabled={saving || savingPrivate}
          >
            {saving ? "Saving…" : "Yes, Add to Map"}
          </button>
          <button
            className="location-status-private"
            type="button"
            onClick={handleKeepPrivate}
            disabled={saving || savingPrivate}
          >
            {savingPrivate ? "Saving…" : "Keep private"}
          </button>
        </div>
      </div>

      <img className="location-status-logo" src={logo} alt="Hacked logo" />
    </section>
  );
}

export default LocationFound;
