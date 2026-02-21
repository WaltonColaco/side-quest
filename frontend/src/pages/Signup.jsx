import { useNavigate } from "react-router-dom";
import logo from "../../hacked-logo.png";
import mailLogo from "../../mail-logo.png";

function Signup() {
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    navigate("/home");
  };

  return (
    <section className="signup-page" aria-label="Sign up">
      <img className="signup-top-logo" src={logo} alt="Hacked logo" />

      <div className="signup-layout">
        <div className="signup-left">
          <img className="signup-mail-logo" src={mailLogo} alt="Mail illustration" />
        </div>

        <div className="signup-right">
          <h1 className="signup-title">Secure your account</h1>
          <form className="signup-form" onSubmit={handleSubmit}>
            <input className="signup-input" type="text" placeholder="Username" />
            <input className="signup-input" type="password" placeholder="Password" />
            <button type="submit" className="signup-submit">
              Create Account
            </button>
          </form>
        </div>
      </div>
    </section>
  );
}

export default Signup;
