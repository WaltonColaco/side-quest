import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import backButton from "../assets/images/back-button.png";
import hackedLogo from "../assets/images/hacked-logo.png";
import navLogo from "../assets/images/nav-button.png";
import SettingsCard from "./SettingsCard";

function PostAuthChrome() {
  const location = useLocation();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [activePanel, setActivePanel] = useState(null);
  const hideBackButton = location.pathname === "/map-heat" || location.pathname === "/settings";
  const hideLeftChrome = location.pathname === "/information";
  const hideBrand = location.pathname === "/score-project";
  const isScoreProject = location.pathname === "/score-project";
  const navItems = isScoreProject
    ? [
        { id: "my-reports", label: "My Reports" },
        { id: "new-audits", label: "New Audits", path: "/score-project" },
        { id: "settings", label: "Settings" },
      ]
    : [
        { id: "about", label: "About" },
        { id: "how-it-works", label: "How It Works" },
        { id: "settings", label: "Settings" },
      ];

  const handleBack = () => {
    if (window.history.length > 1) {
      navigate(-1);
      return;
    }
    navigate("/home");
  };

  return (
    <div className="post-auth-chrome">
      {!hideLeftChrome ? (
        <div className="post-auth-left">
          {!hideBackButton ? (
            <button type="button" className="post-auth-back" onClick={handleBack}>
              <img src={backButton} alt="Back" />
            </button>
          ) : null}
          {!hideBrand ? (
            <button
              type="button"
              className="post-auth-brand-button"
              onClick={() => navigate("/home")}
              aria-label="Go home"
            >
              <img className="post-auth-brand" src={hackedLogo} alt="Hacked logo" />
            </button>
          ) : null}
        </div>
      ) : null}

      <div className="post-auth-right">
        <button
          type="button"
          className="post-auth-nav-trigger"
          onClick={() => setOpen((prev) => !prev)}
          aria-expanded={open}
          aria-label="Open navigation menu"
        >
          <img src={navLogo} alt="" aria-hidden="true" />
        </button>
        {open ? (
          <div className="post-auth-menu">
            {navItems.map((item) => (
              <button
                key={item.id}
                type="button"
                className="post-auth-menu-item"
                onClick={() => {
                  setOpen(false);
                  if (item.path) {
                    navigate(item.path);
                    return;
                  }
                  setActivePanel(item.id);
                }}
              >
                {item.label}
              </button>
            ))}
          </div>
        ) : null}
      </div>

      {activePanel ? (
        <div className="post-auth-modal" onClick={() => setActivePanel(null)}>
          <div
            className={`post-auth-modal-card ${activePanel === "settings" ? "settings-modal-card" : ""}`}
            onClick={(event) => event.stopPropagation()}
          >
            {activePanel === "settings" ? (
              <SettingsCard onClose={() => setActivePanel(null)} />
            ) : (
              <div className="post-auth-panel-content">
                <button
                  type="button"
                  className="post-auth-modal-close"
                  onClick={() => setActivePanel(null)}
                  aria-label="Close panel"
                >
                  x
                </button>
                <h2 className="post-auth-modal-title">
                  {activePanel === "about"
                    ? "About"
                    : activePanel === "how-it-works"
                      ? "How it works"
                      : "My Reports"}
                </h2>
                {activePanel === "about" ? (
                  <>
                    <p>
                      Accessibility should not be a guessing game. Side-Quest bridges architectural complexity and
                      everyday navigation so people can find accessible places faster.
                    </p>
                    <h3>Why this product?</h3>
                    <p>
                      We turn dense standards into practical insights, making it easier to spot where accessibility is
                      strong and where it needs improvement.
                    </p>
                    <h3>Our metrics</h3>
                    <p>
                      Scores are based on Canadian Accessibility Housing Standards, LEED, and Barrier Free Inclusion.
                    </p>
                    <h3>Our team</h3>
                    <p>Built at HackED 2026 by a team focused on accessibility-first, explainable design.</p>
                  </>
                ) : activePanel === "how-it-works" ? (
                  <>
                    <h3>The Big Picture</h3>
                    <p>
                      We guide users to more accessible places to live, work, and explore by turning complex urban
                      data into clear, visual guidance.
                    </p>
                    <h3>Reading the Heatmap</h3>
                    <p>
                      Blue zones indicate lower accessibility while yellow zones indicate stronger inclusion.
                      Accessibility filters let users focus on specific needs.
                    </p>
                    <h3>Scoring</h3>
                    <p>
                      Plans and place details are compared against standards (for example CSA B651) to produce clear,
                      explainable coverage scores.
                    </p>
                  </>
                ) : (
                  <>
                    <p>Your saved audit reports will appear here.</p>
                    <h3>Coming soon</h3>
                    <p>Report history, filters, and export options are being added next.</p>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default PostAuthChrome;
