import React from "react";
import ReactECharts from "echarts-for-react";
import type { PredictionResult } from "../types/prediction";
import SummaryCards from "./SummaryCards";
import {
  getMixedVolumeVsRateChart,
  getCorrelationHeatmapChart,
  getClassDistributionChart,
  getStackedAmountRangesChart,
  getLogBalanceSegmentChart,
  getZeroBalanceChart,
  getAccountingAnomaliesChart,
  getHourlyActivityChart,
} from "../utils/chartOptions";

interface Props {
  predictions: PredictionResult;
}

export default function AnalysisResults({ predictions }: Props) {
  if (!predictions || predictions.status !== 'success') return null;

  const eda = predictions.data?.eda_data ?? {};

  return (
    <div style={{ width: "100%", display: "flex", justifyContent: "center", marginTop: "3rem" }}>
      <div style={{ width: "100%", maxWidth: "2000px", padding: "2rem 0.5rem", boxSizing: "border-box" }}>
        <h3 style={{ marginTop: 0, marginBottom: "1.25rem", color: "#fff", fontSize: "2rem", textAlign: "center" }}>Analysis Results</h3>

        <SummaryCards prediction={predictions} />

        <div style={{ marginTop: "2rem", overflowY: "auto", maxHeight: "calc(100vh - 320px)", paddingRight: "1rem" }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: "2rem", width: "95%", maxWidth: "1600px", paddingBottom: "3rem" }}>
            {eda.mixed_volume_vs_rate && (
              <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                <ReactECharts option={getMixedVolumeVsRateChart(eda)} style={{ height: "700px", width: "100%" }} />
              </div>
            )}

            {eda.correlation_matrix && (
              <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)", display: 'flex', justifyContent: 'center' }}>
                <div style={{ width: '100%', maxWidth: '1200px', aspectRatio: '1 / 1' }}>
                  <ReactECharts option={getCorrelationHeatmapChart(eda)} style={{ height: "100%", width: "100%" }} />
                </div>
              </div>
            )}

            {eda.class_distribution && (
              <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                <ReactECharts option={getClassDistributionChart(eda)} style={{ height: "700px", width: "100%" }} />
              </div>
            )}

            {eda.stacked_amount_ranges && (
              <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                <ReactECharts option={getStackedAmountRangesChart(eda)} style={{ height: "700px", width: "100%" }} />
              </div>
            )}

            {eda.log_balance_segment && (
              <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                <ReactECharts option={getLogBalanceSegmentChart(eda)} style={{ height: "700px", width: "100%" }} />
              </div>
            )}

            {eda.zero_balance_behavior && (
              <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                <ReactECharts option={getZeroBalanceChart(eda)} style={{ height: "700px", width: "100%" }} />
              </div>
            )}

            {eda.accounting_anomalies && (
              <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                <ReactECharts option={getAccountingAnomaliesChart(eda)} style={{ height: "700px", width: "100%" }} />
              </div>
            )}

            {(eda.multi_line_hourly || (eda.hourly_volume_bar && eda.hourly_fraud_rate_line)) && (
              <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)", gridColumn: "1 / -1" }}>
                <ReactECharts option={getHourlyActivityChart(eda)} style={{ height: "700px", width: "100%" }} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
