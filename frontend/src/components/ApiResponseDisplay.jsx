import React from 'react';
import "./ApiResponseDisplay.css"
const ApiResponseDisplay = ({ apiResponse }) => {
  const { path, confidence, final_prediction } = apiResponse;

  // Calculate the confidence percentage
  const confidencePercentage = confidence;

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
      {/* Construct the URL to the image using the relative path */}
      {path && <img src={`${path}`} style={{width: "400px", display: "block",margin: "10px auto"}} alt="Uploaded content" />}
    </div>
  );
};

export default ApiResponseDisplay;
