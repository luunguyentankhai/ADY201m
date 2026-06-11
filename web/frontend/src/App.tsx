import React, { useState } from "react";
import "./App.css";
import Tabs from "./components/Tabs";
import AnalysisUpload from "./components/AnalysisUpload";
import AnalysisResults from "./components/AnalysisResults";
import TransactionForm from "./components/TransactionForm";
import ModelComparison from "./components/ModelComparison";
import type { PredictionResult } from "./types/prediction";

export default function App() {
  const [activeTab, setActiveTab] = useState<'analysis' | 'transaction' | 'models'>('analysis');
  const [predictions, setPredictions] = useState<PredictionResult | null>(null);

  return (
    <div className="rain-scene" style={{ minHeight: "100vh", display: "flex", flexDirection: "column", overflowY: "auto" }}>
      <header className="site-header" style={{ textAlign: "center" }}>
        <h1>Analysis tool</h1>
      </header>

      <Tabs active={activeTab} onChange={setActiveTab} />
      <div className="glass" aria-hidden />

      {activeTab === 'analysis' && (
        <AnalysisUpload onResult={(p) => setPredictions(p)} />
      )}

      {activeTab === 'models' && <ModelComparison />}

      {activeTab === 'transaction' && <TransactionForm />}

      {predictions && predictions.status === 'success' && <AnalysisResults predictions={predictions} />}

      <p className="label" aria-hidden></p>
    </div>
  );
}
