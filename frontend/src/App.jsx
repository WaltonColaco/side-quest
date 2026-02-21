import { Navigate, Route, Routes } from "react-router-dom";
import { useLocation } from "react-router-dom";
import NavButton from "./components/NavButton";
import TopNav from "./components/TopNav";
import About from "./pages/About";
import Home from "./pages/Home";
import HowItWorks from "./pages/HowItWorks";
import MapHeat from "./pages/MapHeat";
import NotFound from "./pages/NotFound";
import ScoreProject from "./pages/ScoreProject";
import Settings from "./pages/Settings";

function App() {
  const location = useLocation();
  const showGlobalLogo = location.pathname !== "/";

  return (
    <>
      {showGlobalLogo ? <NavButton /> : null}
      <TopNav />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/map-heat" element={<MapHeat />} />
        <Route path="/score-project" element={<ScoreProject />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/about" element={<About />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
        <Route path="/home" element={<Navigate to="/" replace />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}

export default App;
