import { Link, useLocation } from "react-router-dom";
import backButton from "../assets/images/back-button.png";
import logo from "../assets/images/hacked-logo.png";
import locationFoundIcon from "../assets/images/location-found.png";

function LocationFound() {
  const location = useLocation();
  const rawAddress = location.state?.address;
  const address =
    rawAddress && rawAddress !== "Location not detected"
      ? rawAddress
      : "[address detected]";

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
        <h2 className="location-status-address">{address}</h2>
        <p className="location-status-copy">
          We have detected this project location. Would you like to include this
          audit in the public accessibility heatmap?
        </p>
        <div className="location-status-actions">
          <Link className="location-status-yes" to="/final-score">
            Yes, Add to Map
          </Link>
          <Link className="location-status-private" to="/final-score">
            Keep private
          </Link>
        </div>
      </div>

      <img className="location-status-logo" src={logo} alt="Hacked logo" />
    </section>
  );
}

export default LocationFound;
