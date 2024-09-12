
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoginPage from "./components/LoginPage";
import FileManager from "./components/FileManager";
import OAuth2Callback from "./components/OAuth2Callback";

const App = () => {
  return (
    <Router>
      <div className="app-container p-8">
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/files" element={<FileManager />} />
          <Route path="/oauth2callback" element={<OAuth2Callback />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

// src/components/LoginPage.js


// src/components/FileManager.js
