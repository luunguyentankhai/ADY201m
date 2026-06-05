import { useState, useRef } from "react";
import "./App.css";
import ReactECharts from "echarts-for-react";
import type { EChartsOption } from "echarts";

interface PredictionResult {
  status: string;
  message: string;
  data: {
    summary: {
      total_transactions: number;
      fraud_detected: number;
      fraud_rate_percent: number;
    };
    eda_data: Record<string, unknown>;
  };
}

export default function Rain() {
  const [clicked, setClicked] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "success" | "error">("idle");
  const [statusMessage, setStatusMessage] = useState("");
  const [predictions, setPredictions] = useState<PredictionResult | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate CSV file
    if (!file.name.endsWith(".csv")) {
      setUploadStatus("error");
      setStatusMessage("Please select a CSV file");
      return;
    }

    setFileName(file.name);
    setClicked(true);
    uploadCSV(file);
  };

  const uploadCSV = async (file: File) => {
    try {
      setUploading(true);
      setUploadStatus("idle");
      setStatusMessage("Processing file...");
      setPredictions(null);

      const formData = new FormData();
      formData.append("file", file);

      console.log("Sending file to backend:", file.name);

      const response = await fetch("http://127.0.0.1:8000/api/predict/upload-csv", {
        method: "POST",
        body: formData,
      });

      console.log("Response status:", response.status);

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Upload failed: ${response.statusText} - ${errorText}`);
      }

      const data = await response.json();
      console.log("Backend response:", data);

      setPredictions(data);
      setUploadStatus("success");
      setStatusMessage(`✓ File processed successfully!`);
    } catch (error) {
      setUploadStatus("error");
      setStatusMessage(
        error instanceof Error ? `✗ Error: ${error.message}` : "✗ Failed to upload file"
      );
      console.error("Upload error:", error);
    } finally {
      setUploading(false);
    }
  };

  // Chart rendering functions
  const getMixedVolumeVsRateChart = (data: Record<string, unknown>): EChartsOption | null => {
    const mixed = data.mixed_volume_vs_rate as {
      categories: string[];
      volume_bar: number[];
      rate_line: number[];
    };

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
        {
          name: "Transaction Volume",
          type: "bar",
          data: mixed.volume_bar,
          yAxisIndex: 0,
          itemStyle: { color: "#5470c6" },
        },
        {
          name: "Fraud Rate (%)",
          type: "line",
          data: mixed.rate_line,
          yAxisIndex: 1,
          itemStyle: { color: "#ee6666" },
          smooth: true,
        },
      ],
    };
  };

  const getStackedAmountRangesChart = (data: Record<string, unknown>): EChartsOption | null => {
    const stacked = data.stacked_amount_ranges as {
      categories: string[];
      normal_tx: number[];
      fraud_tx: number[];
    };

    if (!stacked) return null;

    return {
      title: { text: "Transaction Distribution by Amount Range" },
      tooltip: { trigger: "axis" },
      legend: { data: ["Normal Transactions", "Fraudulent Transactions"] },
      xAxis: { type: "category", data: stacked.categories },
      yAxis: { type: "value" },
      series: [
        {
          name: "Normal Transactions",
          type: "bar",
          data: stacked.normal_tx,
          stack: "total",
          itemStyle: { color: "#91cc75" },
        },
        {
          name: "Fraudulent Transactions",
          type: "bar",
          data: stacked.fraud_tx,
          stack: "total",
          itemStyle: { color: "#ee6666" },
        },
      ],
    };
  };

  const getHourlyActivityChart = (data: Record<string, unknown>): EChartsOption | null => {
    const hourly = data.multi_line_hourly as {
      hours: number[];
      normal_activity: number[];
      fraud_activity: number[];
    };

    if (!hourly) return null;

    return {
      title: { text: "Hourly Transaction Activity" },
      tooltip: { trigger: "axis" },
      legend: { data: ["Normal Activity", "Fraudulent Activity"] },
      xAxis: { type: "category", data: hourly.hours.map((h) => `${h}:00`) },
      yAxis: { type: "value" },
      series: [
        {
          name: "Normal Activity",
          type: "line",
          data: hourly.normal_activity,
          smooth: true,
          itemStyle: { color: "#5470c6" },
          areaStyle: { color: "rgba(84, 112, 198, 0.3)" },
        },
        {
          name: "Fraudulent Activity",
          type: "line",
          data: hourly.fraud_activity,
          smooth: true,
          itemStyle: { color: "#ee6666" },
          areaStyle: { color: "rgba(238, 102, 102, 0.3)" },
        },
      ],
    };
  };

  const getZeroBalanceChart = (data: Record<string, unknown>): EChartsOption | null => {
    const zeroBalance = data.zero_balance_behavior as Record<string, number>;

    if (!zeroBalance) return null;

    const chartData = Object.entries(zeroBalance).map(([name, value]) => ({
      name,
      value,
    }));

    return {
      title: { text: "Account Balance Status After Transaction" },
      tooltip: { trigger: "item" },
      legend: { orient: "vertical", left: "left" },
      series: [
        {
          name: "Account Status",
          type: "pie",
          radius: ["40%", "70%"],
          data: chartData,
          itemStyle: {
            borderRadius: 10,
            borderColor: "#fff",
            borderWidth: 2,
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)",
            },
          },
        },
      ],
    };
  };

  const getAccountingAnomaliesChart = (data: Record<string, unknown>): EChartsOption | null => {
    const anomalies = data.accounting_anomalies as Record<string, number>;

    if (!anomalies) return null;

    return {
      title: { text: "Accounting Anomalies Detection" },
      tooltip: { trigger: "axis" },
      legend: { data: Object.keys(anomalies) },
      xAxis: { type: "category", data: Object.keys(anomalies) },
      yAxis: { type: "value" },
      series: [
        {
          data: Object.values(anomalies),
          type: "bar",
          itemStyle: {
            color: "#188df0",
          },
        },
      ],
    };
  };

  return (
    <div className="rain-scene" style={{ minHeight: "100vh", display: "flex", flexDirection: "column", overflowY: "auto" }}>
      <header className="site-header" style={{ textAlign: "center" }}>
        <h1>Analysis tool</h1>
      </header>
      {/* Window glass grid */}
      <div className="glass" aria-hidden />

      {/* Center file drop area */}
      <div className="file-drop-area" aria-label="File drop area" style={{ flexShrink: 0, alignSelf: "center" }}>
        <div className="file-drop-inner">
          <p className="file-drop-title">Add your file</p>
          <span className="file-drop-hint">
            {fileName ? `Selected: ${fileName}` : "Click to upload CSV file"}
          </span>
          <button
            type="button"
            className={`file-drop-button ${clicked ? "clicked" : ""}`}
            onClick={handleUploadClick}
            disabled={uploading}
          >
            {uploading ? "Processing..." : fileName ? "Change file" : "Upload file"}
          </button>
          
          {/* Hidden file input */}
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            style={{ display: "none" }}
            aria-hidden
          />

          {/* Status message */}
          {statusMessage && (
            <p
              style={{
                marginTop: "1rem",
                color: uploadStatus === "success" ? "#4CAF50" : uploadStatus === "error" ? "#f44336" : "#666",
                fontSize: "0.95rem",
                fontWeight: "500",
                textAlign: "center"
              }}
            >
              {statusMessage}
            </p>
          )}
        </div>
      </div>

      {/* Results Display - Scrollable main window */}
      {predictions && predictions.status === "success" && (
        <div style={{ width: "100%", display: "flex", justifyContent: "center", marginTop: "3rem" }}>
          <div style={{ width: "100%", maxWidth: "2000px", padding: "2rem 0.5rem", boxSizing: "border-box" }}>
            <h3 style={{ marginTop: 0, marginBottom: "1.25rem", color: "#fff", fontSize: "2rem", textAlign: "center" }}>Analysis Results</h3>

            {/* Summary Stats */}
            {predictions.data?.summary && (
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
                  gap: "1rem",
                  width: "95%",
                  maxWidth: "1200px",
                }}
              >
                <div
                  style={{
                    padding: "1.5rem",
                    backgroundColor: "#fff",
                    borderRadius: "8px",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
                    textAlign: "center",
                  }}
                >
                  <div style={{ fontSize: "1rem", color: "#666", fontWeight: "500" }}>Total Transactions</div>
                  <div style={{ fontSize: "2.2rem", fontWeight: "bold", color: "#333", marginTop: "0.5rem" }}>
                    {predictions.data.summary.total_transactions}
                  </div>
                </div>
                <div
                  style={{
                    padding: "1.5rem",
                    backgroundColor: "#fff",
                    borderRadius: "8px",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
                    textAlign: "center",
                  }}
                >
                  <div style={{ fontSize: "1rem", color: "#666", fontWeight: "500" }}>Fraud Detected</div>
                  <div style={{ fontSize: "2.2rem", fontWeight: "bold", color: "#ee6666", marginTop: "0.5rem" }}>
                    {predictions.data.summary.fraud_detected}
                  </div>
                </div>
                <div
                  style={{
                    padding: "1.5rem",
                    backgroundColor: "#fff",
                    borderRadius: "8px",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
                    textAlign: "center",
                  }}
                >
                  <div style={{ fontSize: "1rem", color: "#666", fontWeight: "500" }}>Fraud Rate</div>
                  <div style={{ fontSize: "2.2rem", fontWeight: "bold", color: "#ee6666", marginTop: "0.5rem" }}>
                    {predictions.data.summary.fraud_rate_percent}%
                  </div>
                </div>
              </div>
            )}

            {/* Charts Grid (scrollable) */}
            <div style={{ marginTop: "2rem", overflowY: "auto", maxHeight: "calc(100vh - 320px)", paddingRight: "1rem" }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(500px, 1fr))", gap: "2rem", width: "95%", maxWidth: "1400px", paddingBottom: "3rem" }}>
              {/* Mixed Volume vs Rate Chart */}
              {predictions.data?.eda_data?.mixed_volume_vs_rate && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                  <ReactECharts
                    option={getMixedVolumeVsRateChart(predictions.data.eda_data)}
                    style={{ height: "500px" }}
                  />
                </div>
              )}

              {/* Stacked Amount Ranges Chart */}
              {predictions.data?.eda_data?.stacked_amount_ranges && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                  <ReactECharts
                    option={getStackedAmountRangesChart(predictions.data.eda_data)}
                    style={{ height: "500px" }}
                  />
                </div>
              )}

              {/* Zero Balance Chart */}
              {predictions.data?.eda_data?.zero_balance_behavior && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                  <ReactECharts
                    option={getZeroBalanceChart(predictions.data.eda_data)}
                    style={{ height: "500px" }}
                  />
                </div>
              )}

              {/* Accounting Anomalies Chart */}
              {predictions.data?.eda_data?.accounting_anomalies && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                  <ReactECharts
                    option={getAccountingAnomaliesChart(predictions.data.eda_data)}
                    style={{ height: "500px" }}
                  />
                </div>
              )}

              {/* Hourly Activity Chart - Full width */}
              {predictions.data?.eda_data?.multi_line_hourly && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)", gridColumn: "1 / -1" }}>
                  <ReactECharts
                    option={getHourlyActivityChart(predictions.data.eda_data)}
                    style={{ height: "500px" }}
                  />
                </div>
              )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Subtle caption */}
      <p className="label" aria-hidden>
      </p>
    </div>
  );
}