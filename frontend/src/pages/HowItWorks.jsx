import { useNavigate } from "react-router-dom";
import MapHeat from "./MapHeat";

function HowItWorks() {
  const navigate = useNavigate();
  return (
    <section className="info-overlay full-bleed">
      <div className="info-map-backdrop">
        <MapHeat />
      </div>
      <div className="info-card-body compact">
        <div className="info-card-header">
          <h2 className="info-title">How it works</h2>
          <button className="icon-close" type="button" onClick={() => navigate(-1)} aria-label="Close">
            ×
          </button>
        </div>
        <h3>The Big Picture</h3>
        <p>
          We guide users to the most accessible places to live, work, and explore—turning complex urban data into a
          clear path.
        </p>
        <h3>Reading the Heatmap</h3>
        <p>
          Blue zones show where accessibility is lacking; yellow zones highlight gold-standard inclusion. Filters let
          you focus on ramps, power doors, and elevators.
        </p>
        <h3>Scoring</h3>
        <p>
          We bridge blueprints and reality. By comparing extracted plans against standards (e.g., CSA B651), we give you
          explainable coverage scores.
        </p>
      </div>
    </section>
  );
}

export default HowItWorks;
