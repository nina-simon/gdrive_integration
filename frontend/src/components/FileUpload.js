import React, { useState } from "react";
import axios from "axios";

const FileUpload = ({ fetchFiles }) => {
  const [fileToUpload, setFileToUpload] = useState(null);

  const handleFileUpload = async () => {
    if (!fileToUpload) return;

    const formData = new FormData();
    formData.append("file", fileToUpload);

    try {
      await axios.post("http://localhost:8000/upload", formData);
      alert("File uploaded successfully");
      fetchFiles();
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="file-upload mb-8">
      <input
        type="file"
        className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer focus:outline-none focus:ring"
        onChange={(e) => setFileToUpload(e.target.files[0])}
      />
      <button
        onClick={handleFileUpload}
        className="mt-2 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
      >
        Upload File
      </button>
    </div>
  );
};

export default FileUpload;
