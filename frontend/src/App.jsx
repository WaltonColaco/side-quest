import { Navigate, Route, Routes } from "react-router-dom";
import { useLocation } from "react-router-dom";
import NavButton from "./components/NavButton";
import TopNav from "./components/TopNav";
import About from "./pages/About";
import AboutUser from "./pages/AboutUser";
import Home from "./pages/Home";
import HowItWorks from "./pages/HowItWorks";
import Information from "./pages/Information";
import LoginOverlay from "./pages/LoginOverlay";
import MapHeat from "./pages/MapHeat";
import Name from "./pages/Name";
import NotFound from "./pages/NotFound";
import ScoreProject from "./pages/ScoreProject";
import AboutUser from "./pages/AboutUser";
import Login from "./pages/Login";

function App() {
  const location = useLocation();
  const showGlobalLogo =
    location.pathname !== "/" &&
    location.pathname !== "/information" &&
    location.pathname !== "/aboutuser" &&
    location.pathname !== "/name" &&
    location.pathname !== "/login-overlay";
  const showTopNav =
    location.pathname !== "/information" &&
    location.pathname !== "/aboutuser" &&
    location.pathname !== "/name" &&
    location.pathname !== "/login-overlay";

  return (
    <>
      {showGlobalLogo ? <NavButton /> : null}
      {showTopNav ? <TopNav /> : null}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/map-heat" element={<MapHeat />} />
        <Route path="/score-project" element={<ScoreProject />} />
        <Route path="/settings" element={<MapHeat showSettings />} />
        <Route path="/about" element={<About />} />
        <Route path="/about-user" element={<AboutUser />} />
        <Route path="/login" element={<Login />} />
        <Route path="/information" element={<Information />} />
        <Route path="/aboutuser" element={<AboutUser />} />
        <Route path="/name" element={<Name />} />
        <Route path="/login" element={<Navigate to="/aboutuser" replace />} />
        <Route path="/login-overlay" element={<LoginOverlay />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
        <Route path="/home" element={<Navigate to="/" replace />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}

export default App;
