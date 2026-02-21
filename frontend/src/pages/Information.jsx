import { Link } from "react-router-dom";
import backButton from "../../back-button.png";
import houseImage from "../../hacked-logo.png";
import navMenu from "../../nav-button.png";
import tickMark from "../../tick-mark.png";
import crossMark from "../../cross-mark.png";

function Information() {
  return (
    <section className="information-screen" aria-label="Information page">
      <div className="information-frame">
        <Link className="information-back" to="/map-heat" aria-label="Back">
          <img src={backButton} alt="Back" />
        </Link>
        <img className="information-menu" src={navMenu} alt="Menu" />
        <div className="information-main">
          <div className="information-art">
            <img src={houseImage} alt="House" />
          </div>
          <div className="information-side">
            <div className="information-score-row">
              <p className="information-score">95%</p>
            </div>
            <h2 className="information-address">Address of home</h2>
            <div className="information-checklist" aria-label="Checklist">
              <img className="information-check-icon" src={tickMark} alt="Passed criterion" />
              <img className="information-check-icon" src={tickMark} alt="Passed criterion" />
              <img className="information-check-icon" src={crossMark} alt="Failed criterion" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Information;
