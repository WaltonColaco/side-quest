import { Link } from "react-router-dom";
import backButton from "../assets/images/back-button.png";
import logo from "../assets/images/hacked-logo.png";
import locationNotFoundIcon from "../assets/images/location-not-found.png";

function LocationNotFound() {
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
        <input className="location-status-input" type="text" placeholder="Enter project address or postal code" />
        <div className="location-status-actions">
          <Link className="location-status-yes" to="/final-score">
            Yes, add to Map
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

export default LocationNotFound;
