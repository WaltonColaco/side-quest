import { useNavigate } from "react-router-dom";
import logo from "../../hacked-logo.png";
import userImage from "../../user.png.png";

const roles = ["Resident/Visitor", "Design Professional", "Business Owner"];

function AboutUser() {
  const navigate = useNavigate();

  const handleRoleSelect = (role) => {
    localStorage.setItem("user_role", role);
    navigate("/name");
  };

  return (
    <section className="login-screen" aria-label="About user page">
      <img className="login-logo" src={logo} alt="Hacked logo" />

      <div className="login-content">
        <div className="login-left">
          <h1 className="login-title">Who are you? I am a..</h1>
          <div className="login-role-list">
            {roles.map((role) => (
              <button
                key={role}
                type="button"
                className="login-role-link"
                onClick={() => handleRoleSelect(role)}
              >
                {role}
              </button>
            ))}
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

export default AboutUser;
