import type { PredictionResult } from "../types/prediction";

export function deriveSummary(pred: PredictionResult | null) {
  if (!pred) return null;
  const eda = (pred.data as any).eda_data ?? {};
  const s = (pred.data as any).summary ?? {};

  const total_transactions = s.total_transactions ?? s.total_rows ?? (eda.data_overview?.total_rows) ?? 0;
  const fraud_detected = s.fraud_detected ?? ((eda.class_distribution && (eda.class_distribution.Fraud ?? eda.class_distribution['Fraud'])) ?? 0);
  const fraud_rate_percent = s.fraud_rate_percent ?? (total_transactions ? Math.round((fraud_detected / total_transactions) * 10000) / 100 : 0);

  return {
    total_transactions,
    fraud_detected,
    fraud_rate_percent,
  };
}

export default deriveSummary;
