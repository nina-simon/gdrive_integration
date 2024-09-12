import React, { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

const OAuth2Callback = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const success = searchParams.get('success');
    const error = searchParams.get('error');

    if (success === 'true') {
      localStorage.setItem("isAuthenticated", "true");
      navigate("/files");
    } else if (error) {
      console.error("Authentication error:", error);
      navigate("/", { state: { error: "Authentication failed. Please try again." } });
    } else {
      navigate("/", { state: { error: "Invalid authentication response." } });
    }
  }, [location, navigate]);

  return <div>Processing authentication...</div>;
};

export default OAuth2Callback;

