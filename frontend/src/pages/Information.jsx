import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import backButton from "../../back-button.png";
import houseImage from "../../hacked-logo.png";
import checkIcon from "../../tick-mark.png";
import crossIcon from "../../cross-mark.png";
import { fetchLocationDetail } from "../services/api";

function Information() {
  const [location, setLocation] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchLocationDetail();
        setLocation(data);
      } catch (e) {
        console.error("Failed to load locations", e);
      }
    };
    load();
  }, []);

  const scorePct =
    location && location.score != null ? Math.round(location.score * 100) : null;
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
        <Link className="information-back" to="/map-heat" aria-label="Back">
          <img src={backButton} alt="Back" style={{ pointerEvents: "none" }} />
        </Link>
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
                  <img className="information-check-icon" src={checkIcon} alt="Passed criterion" />
                  <span className="info-label">{item.label}</span>
                </div>
              ))}
              {fails.map((item, idx) => (
                <div key={`f-${idx}`} className="info-row">
                  <img className="information-check-icon" src={crossIcon} alt="Failed criterion" />
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
