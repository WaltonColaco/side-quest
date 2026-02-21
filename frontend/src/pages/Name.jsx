import { Link } from "react-router-dom";
import logo from "../../hacked-logo.png";
import userImage from "../../user.png.png";

function Name() {
  return (
    <section className="login-screen name-page" aria-label="Name page">
      <Link to="/home" aria-label="Go home">
        <img className="login-logo" src={logo} alt="Hacked logo" />
      </Link>

      <div className="login-content">
        <div className="login-left name-left">
          <h1 className="login-title name-title">What is your name?</h1>
          <div className="name-form">
            <input className="name-input" type="text" placeholder="Your name" />
            <Link className="name-next-button" to="/location">
              Continue
            </Link>
          </div>
        </div>

        <div className="login-right">
          <img className="login-user-image" src={userImage} alt="User profile" />
        </div>
      </div>
      <div className="login-bottom-shape" aria-hidden="true" />
    </section>
  );
}

export default Name;
