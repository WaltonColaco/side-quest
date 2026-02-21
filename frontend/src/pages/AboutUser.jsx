<<<<<<< HEAD
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
=======
import logo from "../../hacked-logo.png";
import avatarImg from "../assets/profile-avatar.svg";

const options = ["Resident/Visitor", "Design Professional", "Business Owner"];

function AboutUser() {
  return (
    <section className="about-user-screen full no-card" aria-label="About user">
      <div className="about-user-content about-user-content--full">
        <div className="about-user-left">
          <h2>Who are you? I am a..</h2>
          <div className="about-user-buttons">
            {options.map((opt) => (
              <button key={opt} className="about-user-btn" type="button">
                {opt}
              </button>
            ))}
          </div>
        </div>
        <div className="about-user-right">
          <img src={avatarImg} alt="Profile avatar" className="about-user-avatar-img" />
        </div>
      </div>
>>>>>>> eb8c5f23cc4cb4c096778272d65ea067584f8ca2
    </section>
  );
}

export default AboutUser;
