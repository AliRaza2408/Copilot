import React, { useRef, useState } from 'react';
import { processDecision } from '../services/api';
import { UploadCloud, Check, Loader2, FileText } from 'lucide-react';

export default function UploadBox({ onUploadSuccess }) {
  const fileInputRef = useRef(null);
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState('idle');
  const [error, setError] = useState('');

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length > 0) {
      setFiles(selectedFiles);
      setStatus('selected');
      setError('');
    }
  };

  const handleAnalyzeCase = async () => {
    if (files.length === 0) return;

    setStatus('analyzing');
    setError('');

    try {
      const result = await processDecision(files);
      if (onUploadSuccess) onUploadSuccess(result);
    } catch (err) {
      setStatus('error');
      setError(err.message || 'Could not connect to the backend.');
    }
  };

  if (status === 'analyzing') {
    return (
      <div className="flex flex-col items-center gap-6 text-center py-12">
        <div className="text-lg font-bold text-primary">Analyzing Manufacturing Case...</div>
        
        <div className="w-full max-w-sm space-y-3 text-left">
          <div className="flex items-center gap-3 text-sm font-medium text-success">
            <Check className="h-4 w-4" /> Reading documents
          </div>
          <div className="flex items-center gap-3 text-sm font-medium text-success">
            <Check className="h-4 w-4" /> Extracting requirements
          </div>
          <div className="flex items-center gap-3 text-sm font-medium text-success">
            <Check className="h-4 w-4" /> Identifying suppliers
          </div>
          <div className="flex items-center gap-3 text-sm font-medium text-accent animate-pulse">
            <Loader2 className="h-4 w-4 animate-spin" /> Evaluating constraints & creating evidence
          </div>
        </div>
      </div>
    );
  }

  if (status === 'selected') {
    return (
      <div className="flex flex-col items-center gap-6">
        <div className="w-full">
          <div className="mb-4 text-[15px] font-medium text-ink">Selected file(s):</div>
          <div className="mb-6 flex flex-col gap-2">
            {files.map((file, index) => (
              <div key={index} className="flex items-center gap-3 rounded-lg border border-line bg-fog p-3">
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-success/15 text-success">
                  <Check className="h-4 w-4" />
                </div>
                <span className="text-sm font-medium text-ink truncate flex items-center gap-2">
                  <FileText className="h-4 w-4 text-muted" /> {file.name}
                </span>
              </div>
            ))}
          </div>
          
          {error && (
            <div className="mb-4 w-full rounded-lg border border-danger/20 bg-danger/5 p-3 text-center text-sm font-medium text-danger">
              {error}
            </div>
          )}

          <div className="flex flex-col gap-3 sm:flex-row">
            <button
              onClick={() => fileInputRef.current?.click()}
              className="inline-flex flex-1 items-center justify-center gap-2 rounded-lg border border-line bg-white px-6 py-3 text-[15px] font-semibold text-secondary transition-colors hover:bg-mist"
            >
              Change Selection
            </button>
            <button
              onClick={handleAnalyzeCase}
              className="inline-flex flex-1 items-center justify-center gap-2 rounded-lg bg-accent px-6 py-3 text-[15px] font-semibold text-white transition-colors hover:bg-accent/90"
            >
              Analyze Manufacturing Case
            </button>
            <input
              type="file"
              multiple
              ref={fileInputRef}
              className="hidden"
              onChange={handleFileSelect}
            />
          </div>
        </div>
      </div>
    );
  }

  // Status: 'idle' (Default State)
  return (
    <div className="flex flex-col items-center gap-6">
      <div 
        className="flex w-full cursor-pointer flex-col items-center gap-4 rounded-[10px] border-2 border-dashed border-waiting bg-fog px-6 py-12 transition-colors hover:border-accent"
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-accent/10 text-accent">
          <UploadCloud className="h-6 w-6" />
        </div>
        <div className="text-[18px] font-bold text-primary">Upload Documents</div>
        <div className="text-sm text-muted">Drop files here or browse</div>
        <input
          type="file"
          multiple
          ref={fileInputRef}
          className="hidden"
          onChange={handleFileSelect}
        />
      </div>

      <div className="text-[13px] font-medium tracking-[0.02em] text-muted">
        Supported: PDF • DOCX • XLSX • XLS • CSV
      </div>
    </div>
  );
}