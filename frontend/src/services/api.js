import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
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

export async function fetchFeatures() {
  const { data } = await api.get("/api/features/");
  return data;
}

export default api;
