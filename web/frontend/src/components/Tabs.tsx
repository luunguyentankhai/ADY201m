import React from "react";

export type TabKey = "analysis" | "transaction" | "models";

interface Props {
  active: TabKey;
  onChange: (t: TabKey) => void;
}

export default function Tabs({ active, onChange }: Props) {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', gap: 12, marginTop: 12 }}>
      <button onClick={() => onChange('analysis')} className={`tab-button ${active === 'analysis' ? 'active' : ''}`}>Analysis</button>
      <button onClick={() => onChange('transaction')} className={`tab-button ${active === 'transaction' ? 'active' : ''}`}>Transaction Input</button>
      <button onClick={() => onChange('models')} className={`tab-button ${active === 'models' ? 'active' : ''}`}>Model Comparison</button>
    </div>
  );
}
