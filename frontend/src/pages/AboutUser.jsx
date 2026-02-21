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
    </section>
  );
}

export default AboutUser;
