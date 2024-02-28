import React, { useState, useRef } from 'react';
import './DragAndDrop.css';
import addimage from '../images/addimage2.png';

const DragAndDrop = ({ onFilesSelected }) => {
  const [highlight, setHighlight] = useState(false);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [apiResponse, setApiResponse] = useState(null);
  const fileInputRef = useRef(null);

  const handleDragOver = (event) => {
    event.preventDefault();
    setHighlight(true);
  };

  const handleDragLeave = () => {
    setHighlight(false);
  };

  const handleDrop = async (event) => {
    event.preventDefault();
    setHighlight(false);

    const files = event.dataTransfer.files;
    const filteredFiles = filterFiles(Array.from(files));

    if (filteredFiles.length > 0) {
      const uploadedFile = filteredFiles[0];
      setUploadedImage(URL.createObjectURL(uploadedFile));

      // Call API with the uploaded image
      await uploadImage(uploadedFile);
    }
  };

  const openFileDialog = () => {
    fileInputRef.current.click();
  };

  const handleFileInputChange = async (event) => {
    const files = event.target.files;
    const filteredFiles = filterFiles(Array.from(files));

    if (filteredFiles.length > 0) {
      const uploadedFile = filteredFiles[0];
      setUploadedImage(URL.createObjectURL(uploadedFile));

      // Call API with the uploaded image
      await uploadImage(uploadedFile);
    }
  };

  const filterFiles = (files) => {
    return files.filter(file => {
      const fileType = file.type;
      return fileType === 'image/jpeg' || fileType === 'image/png';
    });
  };

  const uploadImage = async (imageFile) => {
    const formData = new FormData();
    formData.append('fileToUpload', imageFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/process_image/', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to upload image');
      }
    
      const responseData = await response.json();
      console.log(response)
      setApiResponse(responseData);
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div
      className={`drag-drop-area ${highlight ? 'highlight' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={openFileDialog}
    >
      <img src={uploadedImage || addimage} alt="Uploaded content"/>
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
      {apiResponse && (
        <div className="api-response">
          <h3>API Response:</h3>
          <pre>{JSON.stringify(apiResponse, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default DragAndDrop;
