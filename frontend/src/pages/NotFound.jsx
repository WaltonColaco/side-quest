import { Link } from "react-router-dom";

function NotFound() {
  return (
    <section className="hero-card">
      <p className="eyebrow">404</p>
      <h1>Page not found</h1>
      <p className="lead">The route you requested does not exist.</p>
      <Link className="nav-link nav-link-active" to="/">
        Return home
      </Link>
    </section>
  );
}

export default NotFound;
