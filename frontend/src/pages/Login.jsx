import { Link, useNavigate } from "react-router-dom";
import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import logo from "../assets/images/hacked-logo.png";

function Login() {
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    navigate("/home");
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
      <Link to="/home" aria-label="Go home">
        <img className="login-overlay-logo" src={logo} alt="Hacked logo" />
      </Link>

      <div className="login-overlay-card">
        <h1 className="login-overlay-title">Login</h1>
        <form className="login-overlay-form" onSubmit={handleSubmit}>
          <input
            className="login-overlay-input"
            id="email"
            name="email"
            type="email"
            placeholder="Email"
          />
          <input
            className="login-overlay-input"
            id="password"
            name="password"
            type="password"
            placeholder="Password"
          />
          <button type="button" className="login-overlay-forgot">
            Forgot Password
          </button>
          <button type="submit" className="login-overlay-submit">
            Login
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
