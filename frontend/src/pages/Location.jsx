import { useState } from "react";
import { Link } from "react-router-dom";
import logo from "../../hacked-logo.png";
import areaArt from "../../hacked-logo-2.png";
import infoLogo from "../../info-logo.png";

function Location() {
  const [showInfo, setShowInfo] = useState(false);

  return (
    <section className="location-page" aria-label="Location page">
      <Link to="/home" aria-label="Go home">
        <img className="location-top-logo" src={logo} alt="Hacked logo" />
      </Link>

      <div className="location-layout">
        <div className="location-left">
          <button
            type="button"
            className="location-info-button"
            aria-label="Location help"
            onClick={() => setShowInfo((prev) => !prev)}
          >
            <img src={infoLogo} alt="" aria-hidden="true" />
          </button>

          {showInfo ? (
            <div className="location-info-popup" role="status">
              Sharing your location helps us show you the most accessible spots
              in your immediate neighbourhood
            </div>
          ) : null}

          <h1 className="location-title">Where are you based?</h1>

          <input
            className="location-input"
            type="text"
            placeholder="Enter neighbourhood or postal code"
          />

          <div className="location-actions">
            <Link className="location-continue" to="/signup">
              Continue
            </Link>
            <Link className="location-skip" to="/signup">
              Skip for now
            </Link>
          </div>
        </div>

        <div className="location-right">
          <img
            className="location-art"
            src={areaArt}
            alt="Location illustration"
          />
        </div>
      </div>
    </section>
  );
}

export default Location;
