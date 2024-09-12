import React, { useState, useEffect } from "react";
import { listFiles, uploadFile, deleteFile, downloadFile } from "../services/api";
import FileList from "./FileList";

const FileManager = () => {
  const [files, setFiles] = useState([]);
  const [fileToUpload, setFileToUpload] = useState(null);

  const fetchFiles = async () => {
    try {
      const response = await listFiles();
      console.log("files", response.data);
      setFiles(response.data);
    } catch (error) {
      console.error("Error fetching files:", error);
    }
  };

  const handleFileUpload = async () => {
    try {
      await uploadFile(fileToUpload);
      fetchFiles();
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const handleFileDownload = async (fileId) => {
    try {
      console.log("Download Id", fileId);
      
      const response = await fetch(`http://localhost:8000/download/${fileId}`, {
        method: 'GET',
        credentials: 'include',  // Include session credentials
      });
  
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
  
      const blob = await response.blob();  // Convert the response to a Blob
      const url = window.URL.createObjectURL(blob);  // Create a URL for the Blob
      const a = document.createElement('a');
      a.href = url;
      
      // Extract filename from the Content-Disposition header if available
      const filename = response.headers.get('Content-Disposition')
        ? response.headers.get('Content-Disposition').split('filename=')[1]
        : fileId;
  
      a.download = filename.replace(/['"]/g, '');  // Set filename for download
      document.body.appendChild(a);  // Append the element to the DOM
      a.click();  // Programmatically trigger the click event
      document.body.removeChild(a);  // Clean up the DOM by removing the element
    } catch (error) {
      console.error("Error downloading file:", error);
    }
  };
  
  const handleFileDelete = async (fileId) => {
    try {
      await deleteFile(fileId);
      fetchFiles();
    } catch (error) {
      console.error("Error deleting file:", error);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  return (
    <div className="file-manager">
      <h1 className="text-3xl mb-4">Google Drive File Manager</h1>
      <div className="mb-4">
        <input
          type="file"
          onChange={(e) => setFileToUpload(e.target.files[0])}
          className="mb-2"
        />
        <button
          onClick={handleFileUpload}
          className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
        >
          Upload File
        </button>
      </div>
      <FileList files={files} onDelete={handleFileDelete} onDownload={handleFileDownload} />
    </div>
  );
};

export default FileManager;
