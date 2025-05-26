import axios from "axios";
import { Environment } from "src/environment/environment";

const axiosService = axios.create({
  baseURL: Environment.baseUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add request interceptor to handle authentication
axiosService.interceptors.request.use(
  (config) => {
    // Get auth token from localStorage if available
    const authData = localStorage.getItem("UInify-auth");
    if (authData) {
      try {
        const parsedAuth = JSON.parse(authData);
        const token = parsedAuth?.user?.token || Environment.token;
        if (token) {
          config.headers.Authorization = `Token ${token}`;
        }
      } catch (error) {
        console.warn("Error parsing auth data:", error);
      }
    } else if (Environment.token) {
      config.headers.Authorization = `Token ${Environment.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle errors
axiosService.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Unauthorized - clear auth and redirect to login
      localStorage.removeItem("UInify-auth");
      window.location.href = "/login";
    }

    // Log error for debugging
    console.error("API Error:", {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      message: error.response?.data?.message || error.message,
    });

    return Promise.reject(error);
  }
);

export default axiosService;
