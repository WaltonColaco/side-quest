import { Link } from "react-router-dom";
import logo from "../assets/images/hacked-logo.png";
import areaArt from "../assets/images/hacked-logo-2.png";
import infoLogo from "../assets/images/info-logo.png";
import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";

function Location() {
  const [showInfo, setShowInfo] = useState(false);
  const inputRef = useRef(null);
  const navigate = useNavigate();

  const handleContinue = () => {
    const location = inputRef.current?.value.trim();
    if (location) {
      localStorage.setItem("user_location", location);
    }
    navigate("/signup");
  };

  const handleSkip = () => {
    navigate("/signup");
  };

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
            ref={inputRef}
            className="location-input"
            type="text"
            placeholder="Enter neighbourhood or postal code"
          />

          <div className="location-actions">
            <button
              type="button"
              className="location-continue"
              onClick={handleContinue}
            >
              Continue
            </button>
            <button
              type="button"
              className="location-skip"
              onClick={handleSkip}
            >
              Skip for now
            </button>
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
