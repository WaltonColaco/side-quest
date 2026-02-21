import { Link } from "react-router-dom";
import logo from "../../hacked-logo.png";
import userImage from "../../user.png.png";

const roles = ["Resident/Visitor", "Design Professional", "Business Owner"];

function AboutUser() {
  return (
    <section className="login-screen" aria-label="About user page">
      <img className="login-logo" src={logo} alt="Hacked logo" />

      <div className="login-content">
        <div className="login-left">
          <h1 className="login-title">Who are you? I am a..</h1>
          <div className="login-role-list">
            {roles.map((role) => (
              <Link key={role} to="/name" className="login-role-link">
                {role}
              </Link>
            ))}
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

export default AboutUser;
