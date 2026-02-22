import { Link } from "react-router-dom";
import logo from "../assets/images/hacked-logo.png";
import userImage from "../assets/images/user.png.png";
import { useRef } from "react";
import { useNavigate } from "react-router-dom";

function Name() {
  const inputRef = useRef(null);
  const navigate = useNavigate();

  const handleContinue = () => {
    const name = inputRef.current?.value.trim();
    if (name) {
      localStorage.setItem("user_name", name);
    }
    navigate("/location");
  };

  return (
    <section className="login-screen name-page" aria-label="Name page">
      <Link to="/home" aria-label="Go home">
        <img className="login-logo" src={logo} alt="Hacked logo" />
      </Link>

      <div className="login-content">
        <div className="login-left name-left">
          <h1 className="login-title name-title">What is your name?</h1>
          <div className="name-form">
            <input
              ref={inputRef}
              className="name-input"
              type="text"
              placeholder="Your name"
            />
            <button
              type="button"
              className="name-next-button"
              onClick={handleContinue}
            >
              Continue
            </button>
          </div>
        </div>

        <div className="login-right">
          <img
            className="login-user-image"
            src={userImage}
            alt="User profile"
          />
        </div>
      </div>
      <div className="login-bottom-shape" aria-hidden="true" />
    </section>
  );
}

export default Name;
