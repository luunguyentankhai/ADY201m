import React, { useRef, useState } from "react";
import type { PredictionResult } from "../types/prediction";
import { uploadCsv } from "../services/api";

interface Props {
  onResult: (p: PredictionResult) => void;
}

export default function AnalysisUpload({ onResult }: Props) {
  const [clicked, setClicked] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "success" | "error">("idle");
  const [statusMessage, setStatusMessage] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUploadClick = () => fileInputRef.current?.click();

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    if (!file.name.endsWith('.csv')) {
      setUploadStatus('error');
      setStatusMessage('Please select a CSV file');
      return;
    }
    setFileName(file.name);
    setClicked(true);
    uploadCSV(file);
  };

  const uploadCSV = async (file: File) => {
    try {
      setUploading(true);
      setUploadStatus('idle');
      setStatusMessage('Processing file...');

      const data = await uploadCsv(file);
      setUploadStatus('success');
      setStatusMessage('✓ File processed successfully!');
      onResult(data);
    } catch (error) {
      setUploadStatus('error');
      setStatusMessage(error instanceof Error ? `✗ Error: ${error.message}` : '✗ Failed to upload file');
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-drop-area" aria-label="File drop area" style={{ flexShrink: 0, alignSelf: "center" }}>
      <div className="file-drop-inner">
        <p className="file-drop-title">Add your file</p>
        <span className="file-drop-hint">{fileName ? `Selected: ${fileName}` : "Click to upload CSV file"}</span>
        <button type="button" className={`file-drop-button ${clicked ? 'clicked' : ''}`} onClick={handleUploadClick} disabled={uploading}>
          {uploading ? 'Processing...' : fileName ? 'Change file' : 'Upload file'}
        </button>

        <input ref={fileInputRef} type="file" accept=".csv" onChange={handleFileSelect} style={{ display: 'none' }} aria-hidden />

        {statusMessage && (
          <p style={{ marginTop: '1rem', color: uploadStatus === 'success' ? '#4CAF50' : uploadStatus === 'error' ? '#f44336' : '#666', fontSize: '0.95rem', fontWeight: 500, textAlign: 'center' }}>{statusMessage}</p>
        )}
      </div>
    </div>
  );
}
