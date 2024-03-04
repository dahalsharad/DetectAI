import React from 'react';
import "./ApiResponseDisplay.css"

const TextApiResponseDisplay = ({ apiResponse, fileDropped }) => {
  const { confidence, final_prediction } = apiResponse;

  const confidencePercentage = confidence;

  const handleDownload = () => {
    const downloadUrl = 'http://127.0.0.1:8000/aidetector/static/highlighted_output.pdf';

    window.open(downloadUrl, '_blank');
  };

  return (
    <div className="api-response">
      <p>Final Prediction: {final_prediction}</p>
      {/* Progress bar for confidence */}
      <p>Confidence: {confidence}%</p>
      <div className="progress">
        <div
          className="progress-bar"
          role="progressbar"
          style={{ width: `${confidencePercentage}%` }}
          aria-valuenow={confidencePercentage}
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>
      {fileDropped && (
        <button onClick={handleDownload}>View Highlighted PDF</button>
      )}
    </div>
  );
};

export default TextApiResponseDisplay;
