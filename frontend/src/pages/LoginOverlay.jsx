import { Link } from "react-router-dom";
import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import logo from "../../hacked-logo.png";

function LoginOverlay() {
  return (
    <section className="login-overlay-screen" aria-label="Login overlay page">
      <MapContainer
        center={[53.5461, -113.4938]}
        zoom={11}
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
        <Link className="login-overlay-close" to="/" aria-label="Close login">
          ×
        </Link>
        <h1 className="login-overlay-title">Login</h1>

        <input
          className="login-overlay-input"
          type="email"
          placeholder="Email"
          aria-label="Email"
        />
        <input
          className="login-overlay-input"
          type="password"
          placeholder="Password"
          aria-label="Password"
        />

        <button className="login-overlay-forgot" type="button">
          Forgot Password
        </button>

        <button className="login-overlay-submit" type="button">
          Login
        </button>

        <p className="login-overlay-signup">
          New user? Sign up <a href="#">here</a>
        </p>
      </div>
    </section>
  );
}

export default LoginOverlay;
