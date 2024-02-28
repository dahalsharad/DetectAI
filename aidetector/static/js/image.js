import React, { useState, useRef } from 'react';
import axios from 'axios';
import './DragAndDrop.css';
import addimage from '../images/addimage2.png';

const DragAndDrop = ({ onFilesSelected }) => {
  const [highlight, setHighlight] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const fileInputRef = useRef(null);

  const handleDragOver = (event) => {
    event.preventDefault();
    setHighlight(true);
  };

  const handleDragLeave = () => {
    setHighlight(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setHighlight(false);

    const files = event.dataTransfer.files;
    const filteredFiles = filterFiles(Array.from(files));
    setUploadedFiles(filteredFiles);
    onFilesSelected(filteredFiles);

    filteredFiles.forEach(file => {
      uploadImage(file);
    });
  };

  const openFileDialog = () => {
    fileInputRef.current.click();
  };

  const handleFileInputChange = (event) => {
    const files = event.target.files;
    const filteredFiles = filterFiles(Array.from(files));
    setUploadedFiles(filteredFiles);
    onFilesSelected(filteredFiles);

    filteredFiles.forEach(file => {
      uploadImage(file);
    });
  };

  const filterFiles = (files) => {
    return files.filter(file => {
      const fileType = file.type;
      return fileType === 'image/jpeg' || fileType === 'image/png';
    });
  };

  const uploadImage = (file) => {
    const formData = new FormData();
    formData.append('fileToUpload', file);

    axios.post('http://127.0.0.1:8000/process_image/', formData)
      .then(response => {
        console.log('API Response:', response.data);
        // Handle the API response data here
        // For example, update state or display the result to the user
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  return (
    <div
      className={`drag-drop-area ${highlight ? 'highlight' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={openFileDialog}
    >
      <img src={addimage} alt="image failed to load"/>
      <input
        ref={fileInputRef}
        className="file-input"
        type="file"
        onChange={handleFileInputChange}
        accept=".jpg,.jpeg,.png"
        multiple
      />
      <div className="drag-drop-text">
        <p><span className="span1">Drag and drop</span></p>
        <p> or <span className="span2">upload</span> your image here.</p>
      </div>
      {uploadedFiles.length > 0 && (
        <div className="uploaded-files">
          <h3>Uploaded Images:</h3>
          <ul>
            {uploadedFiles.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DragAndDrop;
