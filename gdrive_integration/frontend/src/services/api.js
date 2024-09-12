// src/services/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
});

export const getAuthUrl = () => api.get("/auth/login");

export const listFiles = () => api.get("/drive/list");

export const downloadFile = (fileId) => api.get(`/drive/download/${fileId}`);

export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/drive/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const deleteFile = (fileId) => api.delete(`/drive/delete/${fileId}`);

export default api;