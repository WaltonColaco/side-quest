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

export default api;
