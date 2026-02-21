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
    </section>
  );
}

export default Login;
