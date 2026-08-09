import React, { useState } from 'react';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import ChallengePack from './components/ChallengePack';
import SystemStatus from './components/SystemStatus';
import ResultsDashboard from './components/ResultsDashboard';

export default function App() {
  const [evidenceReceived, setEvidenceReceived] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);

  const handleUploadSuccess = (result) => {
    // The result is now the real JSON coming back from FastAPI!
    // It contains the actual extracted requirements, suppliers, ranking, etc.
    setEvidenceReceived(true);
    setAnalysisData(result);
  };

  const handleReset = () => {
    setAnalysisData(null);
    setEvidenceReceived(false);
  };

  return (
    <div className="mx-auto flex max-w-[1200px] flex-col gap-12 px-6 py-8">
      <Header />
      
      {analysisData ? (
        <ResultsDashboard data={analysisData} onReset={handleReset} />
      ) : (
        <>
          <HeroSection />
          <ChallengePack onUploadSuccess={handleUploadSuccess} />
          <SystemStatus evidenceReceived={evidenceReceived} />
        </>
      )}
    </div>
  );
}