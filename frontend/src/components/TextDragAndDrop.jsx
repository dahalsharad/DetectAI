import React, { useState, useRef } from 'react';
import addtext from '../images/textupload.png';
import TextApiResponseDisplay from "./TextApiResponseDisplay";
import "./TextDragAndDrop.css";

const TextDragAndDrop = ({ onFilesSelected }) => {
  const [highlight, setHighlight] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [apiResponse, setApiResponse] = useState(null);
  const [enteredText, setEnteredText] = useState('');
  const [fileDropped, setFileDropped] = useState(false); // State to track if file is dropped
  const fileInputRef = useRef(null);
  const [showTextDragDrop, setShowTextDragDrop] = useState(true);
  const [showTextAreaDragDrop, setShowTextAreaDragDrop] = useState(true);

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
    setFileDropped(true); // Set fileDropped state to true

    const files = event.dataTransfer.files;
    const filteredFiles = filterFiles(Array.from(files));

    if (filteredFiles.length > 0) {
      const uploadedFile = filteredFiles[0];
      setUploadedFiles([uploadedFile]);

      // Call API with the uploaded text file
      await uploadTextFile(uploadedFile);
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
      setUploadedFiles([uploadedFile]);
      setFileDropped(true); // Set fileDropped state to true

      // Call API with the uploaded text file
      await uploadTextFile(uploadedFile);
    }
  };


  const handleTextareaChange = (event) => {
    setEnteredText(event.target.value);
  };

  const handleSubmitText = async () => {
    if (enteredText.trim() !== '') {
      // Call API with the entered text
      await uploadText(enteredText);
      // Clear the entered text after submission
      setEnteredText('');
    }
  };

  const filterFiles = (files) => {
    return files.filter(file => {
      const fileName = file.name;
      const extension = fileName.split('.').pop().toLowerCase();
      return ['txt', 'docx', 'doc', 'pdf'].includes(extension);
    });
  };

  const uploadTextFile = async (text) => {
    const formData = new FormData();
    formData.append('fileToUpload', text);

    try {
      const response = await fetch('http://127.0.0.1:8000/process_text/', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to upload text file');
      }
    
      const responseData = await response.json();
      setApiResponse(responseData);
      setShowTextDragDrop(false);
      setShowTextAreaDragDrop(false);
    } catch (error) {
      console.error('Error uploading text file:', error);
    }
  };
  const uploadText = async (text) => {
    const formData = new FormData();
    formData.append('inputText', text);

    try {
      const response = await fetch('http://127.0.0.1:8000/process_text/', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to upload text file');
      }
    
      const responseData = await response.json();
      setApiResponse(responseData);
      setShowTextDragDrop(false);
      setShowTextAreaDragDrop(false);
    } catch (error) {
      console.error('Error uploading text file:', error);
    }
  };

  return (
    <div className='container'>    
      {showTextDragDrop && (
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
            accept=".txt,.docx,.pdf,.doc"
            multiple
          />
          <img src={addtext} alt="image failed to load"/>
          <div className="drag-drop-text">
            <p><span className="span1">Drag and drop</span></p>
            <p> or <span className="span2">upload</span> your text file here.</p>
          </div>
        </div>
      )}
      { showTextAreaDragDrop && (
        <div className="text-area">
          <textarea
            value={enteredText}
            onChange={handleTextareaChange}
            placeholder="Enter your text"
          />
          <button onClick={handleSubmitText}>Submit</button>
        </div>
      )}
      {apiResponse && (
        <TextApiResponseDisplay 
          apiResponse={apiResponse} 
          fileDropped={fileDropped} 
        />
      )}
    </div>
  );
};

export default TextDragAndDrop;
