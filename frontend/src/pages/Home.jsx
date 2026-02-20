import Button from "../components/Button";

function Home() {
  return (
    <section className="hero-card">
      <p className="eyebrow">Hackathon Starter</p>
      <h1>Build fast, ship clean.</h1>
      <p className="lead">
        This starter gives you routing, layout, API client setup, and reusable UI
        patterns so you can focus on product features.
      </p>
      <div className="hero-actions">
        <Button>Get Started</Button>
        <Button variant="ghost">Open Docs</Button>
      </div>
    </section>
  );
}

export default Home;
