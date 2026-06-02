import { useState } from "react";
import "./App.css";

export default function Rain() {
  const [clicked, setClicked] = useState(false);

  const handleUploadClick = () => {
    setClicked(true);
  };

  return (
    <div className="rain-scene">
      <header className="site-header">
        <h1>Analysis tool</h1>
      </header>
      {/* Window glass grid */}
      <div className="glass" aria-hidden />

      {/* Center file drop area */}
      <div className="file-drop-area" aria-label="File drop area">
        <div className="file-drop-inner">
          <p className="file-drop-title">Add your file</p>
          <span className="file-drop-hint">
            {clicked ? "File area clicked" : "Drag & drop or click to upload"}
          </span>
          <button
            type="button"
            className={`file-drop-button ${clicked ? "clicked" : ""}`}
            onClick={handleUploadClick}
          >
            {clicked ? "Clicked" : "Upload file"}
          </button>
        </div>
      </div>

      {/* Subtle caption */}
      <p className="label" aria-hidden>
      </p>
    </div>
  );
}