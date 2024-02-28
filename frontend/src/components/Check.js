import React, { useState } from 'react';
import "./Check.css";
import DragAndDrop from './DragAndDrop';
import TextDragAndDrop from './TextDragAndDrop';

function Check() {
  const handleFilesSelected = (files) => {
    console.log('Selected files:', files);
    // Process the selected files here
  };

  // State to manage which component to display
  const [showTextDragAndDrop, setShowTextDragAndDrop] = useState(false);

  // Function to toggle between components
  // const toggleComponent = () => {
  //   setShowTextDragAndDrop(!showTextDragAndDrop);
  // };

  return (
    <>
      <div className="check">
        {/* Toggle between components based on state */}
        {/* Click handlers to toggle between components */}
        <div
          className={`image ${!showTextDragAndDrop ? 'active' : ''}`}
          onClick={() => setShowTextDragAndDrop(false)}
        >
          IMAGE
        </div>
        <div
          className={`text ${showTextDragAndDrop ? 'active' : ''}`}
          onClick={() => setShowTextDragAndDrop(true)}
        >
          TEXT
        </div>
      </div>
      {/* Render components based on state */}
      {showTextDragAndDrop ? (<TextDragAndDrop />) : ( <DragAndDrop onFilesSelected={handleFilesSelected} />)}
    </>
  );
}

export default Check;
