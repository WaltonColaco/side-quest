import { Link } from "react-router-dom";
import backButton from "../assets/images/back-button.png";
import logo from "../assets/images/hacked-logo.png";
import checkIcon from "../assets/images/tick-mark.png";

const bars = [
  { found: 34, missing: 16 },
  { found: 52, missing: 14 },
  { found: 21, missing: 38 },
  { found: 25, missing: 6 },
  { found: 22, missing: 20 },
  { found: 4, missing: 12 },
  { found: 30, missing: 28 },
];

function FinalScore() {
  return (
    <section className="final-score-page" aria-label="Final score page">
      <Link
        className="location-status-back"
        to="/score-project"
        aria-label="Back to score project"
      >
        <img src={backButton} alt="Back" />
      </Link>

      <div className="final-score-wrap">
        <div className="final-score-left">
          <div className="final-score-legend">
            <div className="final-score-legend-item">
              <span className="legend-box legend-missing" />
              <span>Criteria Not Found</span>
            </div>
            <div className="final-score-legend-item">
              <span className="legend-box legend-found" />
              <span>Criteria Found</span>
            </div>
          </div>

          <div className="final-score-chart">
            {bars.map((bar, index) => (
              <div key={index} className="final-score-bar">
                <div
                  className="bar-found"
                  style={{ height: `${bar.found * 7}px` }}
                />
                <div
                  className="bar-missing"
                  style={{ height: `${bar.missing * 7}px` }}
                />
              </div>
            ))}
          </div>
          <div className="final-score-base" />
        </div>

        <div className="final-score-right">
          <div className="final-score-percent-row">
            <h1>95%</h1>
          </div>
          <h2>Address of home</h2>
          <div className="final-score-reasons">
            {[1, 2, 3].map((item) => (
              <div key={item} className="reason-row">
                <img src={checkIcon} alt="Criteria met" />
                <span>in depth reason</span>
              </div>
            ))}
          </div>

          <div className="final-score-actions">
            <Link className="final-score-home" to="/home">
              Return to Home
            </Link>
            <button type="button" className="final-score-download">
              Download PDF
            </button>
          </div>
        </div>
      </div>

      <img className="location-status-logo" src={logo} alt="Hacked logo" />
    </section>
  );
}

export default FinalScore;
