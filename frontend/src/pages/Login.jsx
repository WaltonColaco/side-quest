import { useState } from "react";
import { Link } from "react-router-dom";
import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import logo from "../../hacked-logo.png";
import { useAuth } from "../context/AuthContext";

function Login() {
  const { login } = useAuth();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    const form = event.currentTarget;
    const email = form.email.value.trim();
    const password = form.password.value;

    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }

    setLoading(true);
    try {
      await login(email, password);
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        err.response?.data?.error ||
        "Invalid email or password.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="login-overlay-screen" aria-label="Login">
      <MapContainer
        center={[53.5461, -113.4938]}
        zoom={11}
        zoomControl={false}
        scrollWheelZoom
        className="login-overlay-map"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
      </MapContainer>

      <div className="login-overlay-dim" />
      <img className="login-overlay-logo" src={logo} alt="Hacked logo" />

      <div className="login-overlay-card">
        <Link className="login-overlay-close" to="/home" aria-label="Close login">
          ×
        </Link>
        <h1 className="login-overlay-title">Login</h1>
        <form className="login-overlay-form" onSubmit={handleSubmit}>
          <input
            className="login-overlay-input"
            id="email"
            name="email"
            type="email"
            placeholder="Email"
            autoComplete="email"
          />
          <input
            className="login-overlay-input"
            id="password"
            name="password"
            type="password"
            placeholder="Password"
            autoComplete="current-password"
          />
          {error && <p className="login-overlay-error">{error}</p>}
          <button type="button" className="login-overlay-forgot">
            Forgot Password
          </button>
          <button type="submit" className="login-overlay-submit" disabled={loading}>
            {loading ? "Logging in…" : "Login"}
          </button>
        </form>
        <p className="login-overlay-signup">
          New user? Sign up <Link to="/aboutuser">here</Link>
        </p>
      </div>
    </section>
  );
}

export default Login;
