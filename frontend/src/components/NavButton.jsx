import { Link } from "react-router-dom";
import hackedLogo from "../assets/images/hacked-logo.png";

function NavButton() {
  return (
    <Link className="global-nav-button" to="/home" aria-label="Go to home">
      <img className="global-nav-image" src={hackedLogo} alt="Hacked logo" />
    </Link>
  );
}

export default NavButton;
