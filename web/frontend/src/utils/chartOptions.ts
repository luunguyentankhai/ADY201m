import type { EChartsOption } from "echarts";
import type { EDAData } from "../types/prediction";

export const getMixedVolumeVsRateChart = (data: EDAData): EChartsOption | null => {
  const mixed = data.mixed_volume_vs_rate as any;
  if (!mixed) return null;

  return {
    title: { text: "Volume vs Fraud Rate by Transaction Type" },
    tooltip: { trigger: "axis", axisPointer: { type: "cross" } },
    legend: { data: ["Transaction Volume", "Fraud Rate (%)"] },
    xAxis: { type: "category", data: mixed.categories },
    yAxis: [
      { type: "value", name: "Volume", position: "left" },
      { type: "value", name: "Fraud Rate (%)", position: "right" },
    ],
    series: [
      { name: "Transaction Volume", type: "bar", data: mixed.volume_bar, yAxisIndex: 0, itemStyle: { color: "#5470c6" } },
      { name: "Fraud Rate (%)", type: "line", data: mixed.rate_line, yAxisIndex: 1, itemStyle: { color: "#ee6666" }, smooth: true },
    ],
  };
};

export const getStackedAmountRangesChart = (data: EDAData): EChartsOption | null => {
  const stacked = data.stacked_amount_ranges as any;
  if (!stacked) return null;

  const normal = stacked.normal_tx ?? [];
  const fraud = stacked.fraud_tx ?? [];

  return {
    title: { text: "Transaction Distribution by Amount Range" },
    tooltip: {
      trigger: "axis",
      formatter: (params: any) => {
        const lines = params.map((p: any) => {
          const name = p.seriesName;
          const val = p.value;
          const idx = p.dataIndex;
          const percentArr = name === "Normal Transactions" ? stacked.normal_percent : stacked.fraud_percent;
          const percent = percentArr ? ` (${percentArr[idx]}%)` : "";
          return `${name}: ${val}${percent}`;
        });
        return params[0].axisValue + "<br/>" + lines.join("<br/>");
      },
    },
    legend: { data: ["Normal Transactions", "Fraudulent Transactions"] },
    xAxis: { type: "category", data: stacked.categories },
    yAxis: { type: "value" },
    series: [
      { name: "Normal Transactions", type: "bar", data: normal, stack: "total", itemStyle: { color: "#91cc75" } },
      { name: "Fraudulent Transactions", type: "bar", data: fraud, stack: "total", itemStyle: { color: "#ee6666" } },
    ],
  };
};

export const getCorrelationHeatmapChart = (data: EDAData): EChartsOption | null => {
  const corr = data.correlation_matrix as any;
  if (!corr) return null;

  return {
    title: { text: "Correlation Matrix" },
    tooltip: {
      position: "top",
      formatter: (params: any) => {
        const v = Array.isArray(params.value) ? params.value[2] : params.value;
        if (v === null || v === undefined || Number.isNaN(v)) return "";
        if (Array.isArray(params.value)) {
          const xIdx = params.value[0];
          const yIdx = params.value[1];
          const xName = corr.categories?.[xIdx] ?? xIdx;
          const yName = corr.categories?.[yIdx] ?? yIdx;
          return `${xName} × ${yName}<br/>${(Math.round(Number(v) * 1000) / 1000).toString()}`;
        }
        return (Math.round(Number(v) * 1000) / 1000).toString();
      },
    },
    grid: { height: "70%", top: "10%" },
    xAxis: { type: "category", data: corr.categories, splitArea: { show: true } },
    yAxis: { type: "category", data: corr.categories, splitArea: { show: true } },
    visualMap: { min: -1, max: 1, calculable: true, orient: "horizontal", left: "center", top: "5%" },
    series: [
      {
        name: "correlation",
        type: "heatmap",
        data: corr.heatmap_data as any,
        label: {
          show: true,
          formatter: (params: any) => {
            const v = Array.isArray(params.value) ? params.value[2] : params.value;
            if (v === null || v === undefined || Number.isNaN(v)) return "";
            return (Math.round(Number(v) * 1000) / 1000).toString();
          },
          color: "#000",
          fontSize: 12,
        },
        emphasis: { itemStyle: { borderColor: "#333", borderWidth: 1 } },
      },
    ],
  };
};

export const getClassDistributionChart = (data: EDAData): EChartsOption | null => {
  const dist = data.class_distribution as Record<string, number> | undefined;
  if (!dist) return null;
  const chartData = Object.entries(dist).map(([name, value]) => ({ name, value }));

  return {
    title: { text: "Class Distribution" },
    tooltip: { trigger: "item" },
    legend: { orient: "vertical", left: "left" },
    series: [{ name: "Class", type: "pie", radius: "55%", data: chartData, emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: "rgba(0,0,0,0.5)" } } }],
  };
};

export const getLogBalanceSegmentChart = (data: EDAData): EChartsOption | null => {
  const seg = data.log_balance_segment as any;
  if (!seg) return null;

  return {
    title: { text: "Balance Segment (Log Scale)" },
    tooltip: { trigger: "axis" },
    legend: { data: ["Non-fraud", "Fraud"] },
    xAxis: { type: "category", data: seg.categories },
    yAxis: { type: "log" },
    series: [
      { name: "Non-fraud", type: "bar", data: seg.non_fraud, itemStyle: { color: "#5470c6" } },
      { name: "Fraud", type: "bar", data: seg.fraud, itemStyle: { color: "#ee6666" } },
    ],
  };
};

export const getZeroBalanceChart = (data: EDAData): EChartsOption | null => {
  const zeroBalance = data.zero_balance_behavior as Record<string, number> | undefined;
  if (!zeroBalance) return null;

  const chartData = Object.entries(zeroBalance).map(([name, value]) => ({ name, value }));

  return {
    title: { text: "Account Balance Status After Transaction" },
    tooltip: { trigger: "item" },
    legend: { orient: "vertical", left: "left" },
    series: [
      { name: "Account Status", type: "pie", radius: ["40%", "70%"], data: chartData, itemStyle: { borderRadius: 10, borderColor: "#fff", borderWidth: 2 }, emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: "rgba(0, 0, 0, 0.5)" } } },
    ],
  };
};

export const getAccountingAnomaliesChart = (data: EDAData): EChartsOption | null => {
  const anomalies = data.accounting_anomalies as Record<string, number> | undefined;
  if (!anomalies) return null;

  return {
    title: { text: "Accounting Anomalies Detection" },
    tooltip: { trigger: "axis" },
    legend: { data: Object.keys(anomalies) },
    xAxis: { type: "category", data: Object.keys(anomalies) },
    yAxis: { type: "value" },
    series: [{ data: Object.values(anomalies), type: "bar", itemStyle: { color: "#188df0" } }],
  };
};

export const getHourlyActivityChart = (data: EDAData): EChartsOption | null => {
  const multi = data.multi_line_hourly as any;
  if (multi) {
    return {
      title: { text: "Hourly Transaction Activity" },
      tooltip: { trigger: "axis" },
      legend: { data: ["Normal Activity", "Fraudulent Activity"] },
      xAxis: { type: "category", data: multi.hours.map((h: number) => `${h}:00`) },
      yAxis: { type: "value" },
      series: [
        { name: "Normal Activity", type: "line", data: multi.normal_activity, smooth: true, itemStyle: { color: "#5470c6" }, areaStyle: { color: "rgba(84, 112, 198, 0.3)" } },
        { name: "Fraudulent Activity", type: "line", data: multi.fraud_activity, smooth: true, itemStyle: { color: "#ee6666" }, areaStyle: { color: "rgba(238, 102, 102, 0.3)" } },
      ],
    };
  }

  const vol = data.hourly_volume_bar as any;
  const rate = data.hourly_fraud_rate_line as any;

  if (vol && rate) {
    return {
      title: { text: "Hourly Volume and Fraud Rate" },
      tooltip: { trigger: "axis" },
      legend: { data: ["Volume", "Fraud Rate (%)"] },
      xAxis: { type: "category", data: vol.hours.map((h: number) => `${h}:00`) },
      yAxis: [{ type: "value", name: "Volume" }, { type: "value", name: "Fraud Rate (%)", position: "right" }],
      series: [
        { name: "Volume", type: "bar", data: vol.volume, yAxisIndex: 0, itemStyle: { color: "#5470c6" } },
        { name: "Fraud Rate (%)", type: "line", data: rate.rate, yAxisIndex: 1, smooth: true, itemStyle: { color: "#ee6666" } },
      ],
    };
  }

  return null;
};

export default {
  getMixedVolumeVsRateChart,
  getStackedAmountRangesChart,
  getCorrelationHeatmapChart,
  getClassDistributionChart,
  getLogBalanceSegmentChart,
  getZeroBalanceChart,
  getAccountingAnomaliesChart,
  getHourlyActivityChart,
};
