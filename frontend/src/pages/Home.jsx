import { Link } from "react-router-dom";
import logo from "../assets/images/hacked-logo.png";

function Home() {
  return (
    <section className="landing-shell" aria-label="Starting view">
      <div className="landing-art">
        <img className="landing-logo" src={logo} alt="Hacked project logo" />
      </div>
      <div className="landing-panel">
        <h1 className="landing-title">Choose your view</h1>
        <div className="landing-actions">
          <Link className="landing-action" to="/map-heat">
            Explore the Map
          </Link>
          <Link className="landing-action" to="/score-project">
            Audit A Project
          </Link>
          <Link className="landing-action" to="/reports">
            View Reports
          </Link>
        </div>
      </div>
    </section>
  );
}

export default Home;
