import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import backButton from "../assets/images/back-button.png";
import houseImage from "../assets/images/hacked-logo.png";
import checkIcon from "../assets/images/tick-mark.png";
import crossIcon from "../assets/images/cross-mark.png";
import { Link, useSearchParams } from "react-router-dom";
import { fetchLocationDetail } from "../services/api";

function Information() {
  const navigate = useNavigate();
  const [location, setLocation] = useState(null);
  const [searchParams] = useSearchParams();
  const locationId = searchParams.get("id");

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchLocationDetail(locationId);
        setLocation(data);
      } catch (e) {
        console.error("Failed to load locations", e);
      }
    };
    load();
  }, [locationId]);

  const scorePct =
    location && location.score != null
      ? Math.round(location.score * 100)
      : null;
  const address =
    location?.address ||
    location?.name ||
    location?.source ||
    "Address not available";

  const passes = location?.passes || [];
  const fails = location?.fails || [];

  return (
    <section className="information-screen" aria-label="Information page">
      <div className="information-frame">
        <button
          className="information-back"
          type="button"
          onClick={() => navigate("/map-heat")}
          aria-label="Back"
        >
          <img src={backButton} alt="Back" />
        </button>
        <div className="information-main">
          <div className="information-art">
            <img src={houseImage} alt="House" />
          </div>
          <div className="information-side">
            <div className="information-score-row">
              <p className="information-score">
                {scorePct !== null ? `${scorePct}%` : "—"}
              </p>
            </div>
            <h2 className="information-address">{address}</h2>
            <div className="information-checklist" aria-label="Checklist">
              {passes.map((item, idx) => (
                <div key={`p-${idx}`} className="info-row">
                  <img
                    className="information-check-icon"
                    src={checkIcon}
                    alt="Passed criterion"
                  />
                  <span className="info-label">{item.label}</span>
                </div>
              ))}
              {fails.map((item, idx) => (
                <div key={`f-${idx}`} className="info-row">
                  <img
                    className="information-check-icon"
                    src={crossIcon}
                    alt="Failed criterion"
                  />
                  <span className="info-label">{item.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Information;
