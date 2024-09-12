import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { getAuthUrl } from "../services/api";

const LoginPage = () => {
  const [authUrl, setAuthUrl] = useState("");
  const location = useLocation();

  useEffect(() => {
    const fetchAuthUrl = async () => {
      try {
        const response = await getAuthUrl();
        setAuthUrl(response.data.url);
      } catch (error) {
        console.error("Failed to get auth URL:", error);
      }
    };

    fetchAuthUrl();
  }, []);

  const handleLogin = () => {
    if (authUrl) {
      window.location.href = authUrl;
    }
  };

  return (
    <div className="login-page">
      <h1 className="text-3xl mb-4">Login to Google Drive</h1>
      {location.state?.error && (
        <p className="text-red-500 mb-4">{location.state.error}</p>
      )}
      <button
        onClick={handleLogin}
        className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
      >
        Log in with Google
      </button>
    </div>
  );
};

export default LoginPage;