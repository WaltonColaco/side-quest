import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/images/hacked-logo.png";
import mailLogo from "../assets/images/mail-logo.png";
import { useAuth } from "../context/AuthContext";

function Signup() {
  const { signup } = useAuth();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Data collected through the onboarding flow (persisted in localStorage)
  const collectedName = localStorage.getItem("user_name") || "";
  const collectedRole = localStorage.getItem("user_role") || "";
  const collectedLocation = localStorage.getItem("user_location") || "";

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    const form = event.currentTarget;
    const email = form.email.value.trim();
    const password = form.password.value;

    if (!email || !password) {
      setError("Please enter an email and password.");
      return;
    }

    if (!email.includes("@")) {
      setError("Please enter a valid email address.");
      return;
    }

    setLoading(true);
    try {
      await signup(
        email,
        password,
        collectedName,
        collectedRole,
        collectedLocation,
      );
      // user_name / user_role / user_location stay in localStorage intentionally
      // so they're accessible across sessions
    } catch (err) {
      const msg =
        err.response?.data?.error ||
        err.response?.data?.detail ||
        "Could not create account. Please try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="signup-page" aria-label="Sign up">
      <Link to="/home" aria-label="Go home">
        <img className="signup-top-logo" src={logo} alt="Hacked logo" />
      </Link>

      <div className="signup-layout">
        <div className="signup-left">
          <img
            className="signup-mail-logo"
            src={mailLogo}
            alt="Mail illustration"
          />
        </div>

        <div className="signup-right">
          <h1 className="signup-title">Secure your account</h1>
          <form className="signup-form" onSubmit={handleSubmit}>
            <input
              className="signup-input"
              name="email"
              type="email"
              placeholder="Email"
              autoComplete="email"
            />
            <input
              className="signup-input"
              name="password"
              type="password"
              placeholder="Password"
              autoComplete="new-password"
            />
            {error && <p className="signup-error">{error}</p>}
            <button type="submit" className="signup-submit" disabled={loading}>
              {loading ? "Creating account…" : "Create Account"}
            </button>
          </form>
        </div>
      </div>
    </section>
  );
}

export default Signup;
