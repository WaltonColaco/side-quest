<<<<<<< HEAD
import logo from "../../hacked-logo.png";
import userImage from "../../user.png.png";

const roles = ["Resident/Visitor", "Design Professional", "Business Owner"];

function Login() {
  return (
    <section className="login-screen" aria-label="Login page">
      <img className="login-logo" src={logo} alt="Hacked logo" />

      <div className="login-content">
        <div className="login-left">
          <h1 className="login-title">Who are you? I am a..</h1>
          <div className="login-role-list">
            {roles.map((role) => (
              <button key={role} type="button" className="login-role-button">
                {role}
              </button>
            ))}
          </div>
        </div>

        <div className="login-right">
          <img className="login-user-image" src={userImage} alt="User profile" />
        </div>
      </div>
      <div className="login-bottom-shape" aria-hidden="true" />
=======
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  return (
    <section className="login-screen" aria-label="Login">
      <div className="login-panel">
        <h1>Login</h1>
        <form className="login-form">
          <label className="sr-only" htmlFor="email">
            Email
          </label>
          <input id="email" name="email" type="email" placeholder="Email" />

          <label className="sr-only" htmlFor="password">
            Password
          </label>
          <input id="password" name="password" type="password" placeholder="Password" />

          <button type="button" className="login-forgot">
            Forgot Password
          </button>

          <button type="submit" className="login-submit">
            Login
          </button>
        </form>

        <p className="login-foot">
          New user?{" "}
          <button type="button" className="login-link" onClick={() => navigate("/signup")}>
            here
          </button>
        </p>
      </div>
>>>>>>> eb8c5f23cc4cb4c096778272d65ea067584f8ca2
    </section>
  );
}

export default Login;
