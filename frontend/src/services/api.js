import axios from "axios";

const api = axios.create({
  // Prefer explicit env; otherwise fall back to relative calls so Vite proxy/same-origin works.
  baseURL: import.meta.env.VITE_API_URL || "",
  timeout: 10000,
});

// Attach JWT token from localStorage on every request (if present)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(error);
  }
);

export async function fetchAssessments() {
  const { data } = await api.get("/api/assessments/");
  return data;
}

export async function fetchComparisons() {
  const { data } = await api.get("/api/comparisons/");
  return data;
}

export async function fetchLocations() {
  const { data } = await api.get("/api/location/");
  return data;
}

export async function fetchLocationDetail(id = null) {
  const params = id ? { id } : {};
  const { data } = await api.get("/api/location/detail/", { params });
  return data;
}

export async function geocodeSearch(query) {
  const { data } = await api.get("/api/geocode/", { params: { q: query } });
  return data;
}

export async function extractFile(file, buildingType = null, model = "gpt-4.1") {
  const formData = new FormData();
  formData.append("file", file);
  if (buildingType) formData.append("building_type", buildingType);
  formData.append("model", model);

  const { data } = await api.post("/api/extract/", formData, {
    // Set to undefined so axios removes the default "application/json" and lets
    // the browser auto-set "multipart/form-data" with the correct boundary
    headers: { "Content-Type": undefined },
    timeout: 300000, // 5 minutes — extraction can take a while
  });
  return data;
}

export async function saveLocation({ address, lat, lng, sourceDoc }) {
  const { data } = await api.post("/api/location/save/", {
    address,
    lat,
    lng,
    source_doc: sourceDoc,
  });
  return data;
}

export async function fetchMyLocations() {
  const { data } = await api.get("/api/location/mine/");
  return data;
}

export async function fetchFeatures() {
  const { data } = await api.get("/api/features/");
  return data;
}

export async function fetchMe() {
  const { data } = await api.get("/api/me/");
  return data; // { id, username, name, role, location }
}

export async function registerUser(email, password, name = "", role = "", location = "") {
  const { data } = await api.post("/api/register/", { email, password, name, role, location });
  return data;
}

export async function loginUser(email, password) {
  // Django simplejwt expects { username, password } — we store email as the username
  const { data } = await api.post("/api/token/", { username: email, password });
  return data;
}

export default api;
