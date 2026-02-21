import { useNavigate } from "react-router-dom";
import MapHeat from "./MapHeat";

function About() {
  const navigate = useNavigate();
  return (
    <section className="info-overlay full-bleed">
      <div className="info-map-backdrop">
        <MapHeat />
      </div>
      <div className="info-card-body compact">
        <div className="info-card-header">
          <h2 className="info-title">About</h2>
          <button className="icon-close" type="button" onClick={() => navigate(-1)} aria-label="Close">
            ×
          </button>
        </div>
        <p>
          Accessibility shouldn’t be a guessing game. Side-Quest bridges the gap between architectural complexity and
          everyday navigation, giving users a clear path to accessible places.
        </p>
        <h3>Why this product?</h3>
        <p>We translate dense standards into actionable insights—so you know where accessibility is strong or missing.</p>
        <h3>Our metrics</h3>
        <p>
          Built on Canadian Accessibility Housing Standards, LEED, and Barrier Free Inclusion, producing easy-to-read
          percentage scores.
        </p>
        <h3>Our team</h3>
        <p>Crafted at HackED 2026 by a team focused on accessibility-first design and explainable compliance.</p>
      </div>
    </section>
  );
}

export default About;
