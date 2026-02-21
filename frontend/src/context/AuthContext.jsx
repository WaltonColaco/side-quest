import { createContext, useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser, registerUser, fetchMe } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("access_token"));
  const [user, setUser] = useState(null); // { id, username, name }
  const navigate = useNavigate();

  // On mount, if a token exists try to restore user info from the backend
  useEffect(() => {
    if (!token) return;
    fetchMe()
      .then((data) => {
        setUser(data);
        // Keep localStorage in sync with the authoritative values from the backend
        if (data.role) localStorage.setItem("user_role", data.role);
        if (data.location) localStorage.setItem("user_location", data.location);
        if (data.name) localStorage.setItem("user_name", data.name);
      })
      .catch(() => {
        // Token is expired or invalid — clear it so the user gets sent to login
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        setToken(null);
      });
  }, [token]);

  async function login(email, password) {
    const data = await loginUser(email, password);
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    setToken(data.access);
    navigate("/home");
  }

  async function signup(email, password, name = "", role = "", location = "") {
    await registerUser(email, password, name, role, location);
    // Auto-login after successful registration
    await login(email, password);
  }

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setToken(null);
    setUser(null);
    navigate("/");
  }

  return (
    <AuthContext.Provider value={{ token, user, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
