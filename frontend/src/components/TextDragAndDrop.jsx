import React, { useState, useRef } from 'react';
import addtext from '../images/textupload.png';
const TextDragAndDrop = ({ onFilesSelected }) => {
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
  };

  const openFileDialog = () => {
    fileInputRef.current.click();
  };

  const handleFileInputChange = (event) => {
    const files = event.target.files;
    const filteredFiles = filterFiles(Array.from(files));
    setUploadedFiles(filteredFiles);
    onFilesSelected(filteredFiles);
  };

  const filterFiles = (files) => {
    return files.filter(file => {
      const fileType = file.type;
      return fileType === 'text/plain';
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
      <input
        ref={fileInputRef}
        className="file-input"
        type="file"
        onChange={handleFileInputChange}
        accept=".txt" // Accept only text files
        multiple
      />
      <img src={addtext} alt="image failed to load"/>
      <div className="drag-drop-text">
        <p><span className="span1">Drag and drop</span></p>
        <p> or <span className="span2">upload</span> your text file here.</p>
      </div>
      {uploadedFiles.length > 0 && (
        <div className="uploaded-files">
          <h3>Uploaded Text Files:</h3>
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

export default TextDragAndDrop;
