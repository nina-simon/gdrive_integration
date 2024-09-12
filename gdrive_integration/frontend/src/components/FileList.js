import React from "react";

const FileList = ({ files, onDelete, onDownload}) => {
  return (
    <div className="file-list">
      {files.length > 0 ? (
        files.map((file) => (
          <div
            key={file.id}
            className="flex justify-between items-center bg-gray-100 p-4 rounded mb-2"
          >
            <div className="flex-1">
              <span className="text-gray-800">{file.name}</span>
            </div>

            <div className="flex space-x-4">
              <button
                onClick={() => onDownload(file.id)}
                className="bg-blue-500 text-white py-1 px-4 rounded hover:bg-blue-600"
              >
                Download
              </button>

              <button
                onClick={() => onDelete(file.id)}
                className="bg-red-500 text-white py-1 px-4 rounded hover:bg-red-600"
              >
                Delete
              </button>
            </div>
          </div>

        ))
      ) : (
        <p className="text-gray-500">No files available</p>
      )}
    </div>
  );
};

export default FileList;
