import { NavLink } from "react-router-dom";

const items = [
  { to: "/about", label: "About" },
  { to: "/how-it-works", label: "How It Works" },
  { to: "/settings", label: "Settings" },
];

function TopNav() {
  return (
    <nav className="top-nav" aria-label="Top navigation">
      {items.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) =>
            isActive ? "top-nav-link top-nav-link-active" : "top-nav-link"
          }
        >
          {item.label}
        </NavLink>
      ))}
    </nav>
  );
}

export default TopNav;
