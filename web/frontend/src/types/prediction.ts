import type { EChartsOption } from "echarts";

export interface PredictionSummary {
  total_transactions?: number;
  fraud_detected?: number;
  fraud_rate_percent?: number;
}

export interface ModelDetail {
  model_name: string;
  is_fraud: boolean;
  confidence_score: number;
}

export interface SinglePredictionResult {
  final_decision?: string;
  voting_ratio?: string | number;
  model_details?: ModelDetail[];
  [key: string]: any;
}

export interface MixedVolumeVsRate {
  categories: string[];
  volume_bar: number[];
  rate_line: number[];
}

export interface StackedAmountRanges {
  categories: string[];
  normal_tx?: number[];
  fraud_tx?: number[];
  normal_percent?: number[];
  fraud_percent?: number[];
}

export interface CorrelationMatrix {
  categories: string[];
  heatmap_data: Array<[number, number, number]>;
}

export interface LogBalanceSegment {
  categories: string[];
  non_fraud: number[];
  fraud: number[];
}

export interface HourlyMultiLine {
  hours: number[];
  normal_activity: number[];
  fraud_activity: number[];
}

export interface HourlyVolumeBar {
  hours: number[];
  volume: number[];
}

export interface HourlyFraudRateLine {
  hours: number[];
  rate: number[];
}

export interface EDAData {
  mixed_volume_vs_rate?: MixedVolumeVsRate;
  stacked_amount_ranges?: StackedAmountRanges;
  correlation_matrix?: CorrelationMatrix;
  class_distribution?: Record<string, number>;
  log_balance_segment?: LogBalanceSegment;
  zero_balance_behavior?: Record<string, number>;
  accounting_anomalies?: Record<string, number>;
  multi_line_hourly?: HourlyMultiLine;
  hourly_volume_bar?: HourlyVolumeBar;
  hourly_fraud_rate_line?: HourlyFraudRateLine;
  [key: string]: any;
}

export interface PredictionResult {
  status: string;
  message?: string;
  data: {
    summary?: PredictionSummary;
    eda_data?: EDAData;
    [key: string]: any;
  };
}

export type ChartGetter = (data: EDAData) => EChartsOption | null;

export * from "echarts";
