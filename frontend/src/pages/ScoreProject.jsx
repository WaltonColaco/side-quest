import { Link } from "react-router-dom";

function ScoreProject() {
  return (
    <section className="hero-card score-shell">
      <p className="eyebrow">Coming Next</p>
      <h1>Score a project</h1>
      <p className="lead">
        This screen is ready for your scoring form, weights, and evaluation logic.
      </p>
      <Link className="landing-action score-back" to="/">
        back to home
      </Link>
    </section>
  );
}

export default ScoreProject;
