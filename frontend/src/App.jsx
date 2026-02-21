import { Navigate, Route, Routes } from "react-router-dom";
import { useLocation } from "react-router-dom";
import NavButton from "./components/NavButton";
import TopNav from "./components/TopNav";
import About from "./pages/About";
import AboutUser from "./pages/AboutUser";
import Home from "./pages/Home";
import HowItWorks from "./pages/HowItWorks";
import Information from "./pages/Information";
import Login from "./pages/Login";
import Location from "./pages/Location";
import MapHeat from "./pages/MapHeat";
import Name from "./pages/Name";
import NotFound from "./pages/NotFound";
import ScoreProject from "./pages/ScoreProject";
import Signup from "./pages/Signup";

function App() {
  const location = useLocation();
  const showGlobalLogo =
    location.pathname !== "/" &&
    location.pathname !== "/home" &&
    location.pathname !== "/information" &&
    location.pathname !== "/aboutuser" &&
    location.pathname !== "/name" &&
    location.pathname !== "/location" &&
    location.pathname !== "/signup" &&
    location.pathname !== "/login";
  const showTopNav =
    location.pathname !== "/" &&
    location.pathname !== "/information" &&
    location.pathname !== "/aboutuser" &&
    location.pathname !== "/name" &&
    location.pathname !== "/location" &&
    location.pathname !== "/signup" &&
    location.pathname !== "/login";

  return (
    <>
      {showGlobalLogo ? <NavButton /> : null}
      {showTopNav ? <TopNav /> : null}
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/map-heat" element={<MapHeat />} />
        <Route path="/score-project" element={<ScoreProject />} />
        <Route path="/settings" element={<MapHeat showSettings />} />
        <Route path="/about" element={<About />} />
        <Route path="/about-user" element={<AboutUser />} />
        <Route path="/information" element={<Information />} />
        <Route path="/aboutuser" element={<AboutUser />} />
        <Route path="/name" element={<Name />} />
        <Route path="/location" element={<Location />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
        <Route path="/home" element={<Home />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}

export default App;
