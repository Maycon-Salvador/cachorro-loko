import axios from "axios";

const api = axios.create({
  baseURL: "https://nxgnr11c1a.execute-api.sa-east-1.amazonaws.com/dev",
});

// Interceptor para adicionar token JWT em todas as requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
