import React from "react";
import type { PredictionResult } from "../types/prediction";
import { deriveSummary } from "../utils/summary";

interface Props {
  prediction: PredictionResult;
}

export default function SummaryCards({ prediction }: Props) {
  const derived = deriveSummary(prediction as PredictionResult);
  if (!derived) return null;

  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: "1rem", width: "95%", maxWidth: "1200px" }}>
      <div style={{ padding: "1.5rem", backgroundColor: "#fff", borderRadius: "8px", boxShadow: "0 4px 12px rgba(0,0,0,0.2)", textAlign: "center" }}>
        <div style={{ fontSize: "1rem", color: "#666", fontWeight: "500" }}>Total Transactions</div>
        <div style={{ fontSize: "2.2rem", fontWeight: "bold", color: "#333", marginTop: "0.5rem" }}>{derived.total_transactions}</div>
      </div>

      <div style={{ padding: "1.5rem", backgroundColor: "#fff", borderRadius: "8px", boxShadow: "0 4px 12px rgba(0,0,0,0.2)", textAlign: "center" }}>
        <div style={{ fontSize: "1rem", color: "#666", fontWeight: "500" }}>Fraud Detected</div>
        <div style={{ fontSize: "2.2rem", fontWeight: "bold", color: "#ee6666", marginTop: "0.5rem" }}>{derived.fraud_detected}</div>
      </div>

      <div style={{ padding: "1.5rem", backgroundColor: "#fff", borderRadius: "8px", boxShadow: "0 4px 12px rgba(0,0,0,0.2)", textAlign: "center" }}>
        <div style={{ fontSize: "1rem", color: "#666", fontWeight: "500" }}>Fraud Rate</div>
        <div style={{ fontSize: "2.2rem", fontWeight: "bold", color: "#ee6666", marginTop: "0.5rem" }}>{derived.fraud_rate_percent}%</div>
      </div>
    </div>
  );
}
