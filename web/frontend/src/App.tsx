import { useState, useRef } from "react";
import "./App.css";
import ReactECharts from "echarts-for-react";
import type { EChartsOption } from "echarts";
// Inlined Model Comparison content (was in src/ml_model_comparison.tsx)

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
  const [activeTab, setActiveTab] = useState<'analysis'|'transaction'|'models'>('analysis');
  const [fileName, setFileName] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "success" | "error">("idle");
  const [statusMessage, setStatusMessage] = useState("");
  const [predictions, setPredictions] = useState<PredictionResult | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Transaction form state
  const [txForm, setTxForm] = useState({
    amount: '',
    nameOrig: '',
    oldBalanceOrg: '',
    newBalanceOrig: '',
    nameDest: '',
    oldBalanceDest: '',
    newBalanceDest: '',
    type: 'Transfer'
  });
  const [txMessage, setTxMessage] = useState<string | null>(null);
  const [singleResult, setSingleResult] = useState<any | null>(null);

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

  const handleTxChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setTxForm((s) => ({ ...s, [name]: value }));
  };

  const handleTxSubmit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setTxMessage(null);
    setSingleResult(null);

    // map frontend camelCase names to backend schema field names
    const payload = {
      amount: Number(txForm.amount) || 0,
      nameOrig: txForm.nameOrig,
      oldbalanceOrg: Number(txForm.oldBalanceOrg) || 0,
      newbalanceOrig: Number(txForm.newBalanceOrig) || 0,
      nameDest: txForm.nameDest,
      oldbalanceDest: Number(txForm.oldBalanceDest) || 0,
      newbalanceDest: Number(txForm.newBalanceDest) || 0,
      type: txForm.type
    };

    try {
      setTxMessage('Sending to model...');
      console.log('handleTxSubmit payload:', payload);
      const res = await fetch('http://127.0.0.1:8000/api/predict/single', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`${res.status} ${res.statusText} ${text}`);
      }

      const data = await res.json();
      // expected shape: { status: 'success', data: { ... } }
      if (data && data.status === 'success') {
        setSingleResult(data.data);
        setTxMessage('Prediction received');
      } else {
        setTxMessage('Prediction failed');
      }
    } catch (err) {
      console.error('Single predict error', err);
      setTxMessage(err instanceof Error ? err.message : 'Request failed');
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
      normal_tx?: number[];
      fraud_tx?: number[];
      normal_percent?: number[];
      fraud_percent?: number[];
    } | undefined;

    if (!stacked) return null;

    // prefer counts for stacked bars, but expose percents in tooltip
    const normal = stacked.normal_tx ?? [];
    const fraud = stacked.fraud_tx ?? [];

    return {
      title: { text: "Transaction Distribution by Amount Range" },
      tooltip: {
        trigger: "axis",
        formatter: (params: any) => {
          // params is an array of series entries
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
        {
          name: "Normal Transactions",
          type: "bar",
          data: normal,
          stack: "total",
          itemStyle: { color: "#91cc75" },
        },
        {
          name: "Fraudulent Transactions",
          type: "bar",
          data: fraud,
          stack: "total",
          itemStyle: { color: "#ee6666" },
        },
      ],
    };
  };

  const getCorrelationHeatmapChart = (data: Record<string, unknown>): EChartsOption | null => {
    const corr = data.correlation_matrix as {
      categories: string[];
      heatmap_data: Array<[number, number, number]>;
    } | undefined;

    if (!corr) return null;

    return {
      title: { text: "Correlation Matrix" },
      tooltip: {
        position: 'top',
        formatter: (params: any) => {
          const v = Array.isArray(params.value) ? params.value[2] : params.value;
          if (v === null || v === undefined || Number.isNaN(v)) return '';
          // params.value is [xIndex, yIndex, value]
          if (Array.isArray(params.value)) {
            const xIdx = params.value[0];
            const yIdx = params.value[1];
            const xName = corr.categories?.[xIdx] ?? xIdx;
            const yName = corr.categories?.[yIdx] ?? yIdx;
            return `${xName} × ${yName}<br/>${(Math.round(Number(v) * 1000) / 1000).toString()}`;
          }
          return (Math.round(Number(v) * 1000) / 1000).toString();
        }
      },
      grid: { height: '70%', top: '10%' },
      xAxis: {
        type: 'category',
        data: corr.categories,
        splitArea: { show: true }
      },
      yAxis: {
        type: 'category',
        data: corr.categories,
        splitArea: { show: true }
      },
      visualMap: {
        min: -1,
        max: 1,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        top: '5%'
      },
      series: [
        {
          name: 'correlation',
          type: 'heatmap',
          data: corr.heatmap_data as any,
          label: {
            show: true,
            formatter: (params: any) => {
              const v = Array.isArray(params.value) ? params.value[2] : params.value;
              if (v === null || v === undefined || Number.isNaN(v)) return '';
              return (Math.round(Number(v) * 1000) / 1000).toString();
            },
            color: '#000',
            fontSize: 12
          },
          emphasis: { itemStyle: { borderColor: '#333', borderWidth: 1 } }
        }
      ]
    };
  };

  const getClassDistributionChart = (data: Record<string, unknown>): EChartsOption | null => {
    const dist = data.class_distribution as Record<string, number> | undefined;
    if (!dist) return null;
    const chartData = Object.entries(dist).map(([name, value]) => ({ name, value }));

    return {
      title: { text: 'Class Distribution' },
      tooltip: { trigger: 'item' },
      legend: { orient: 'vertical', left: 'left' },
      series: [
        {
          name: 'Class',
          type: 'pie',
          radius: '55%',
          data: chartData,
          emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' } }
        }
      ]
    };
  };

  const getLogBalanceSegmentChart = (data: Record<string, unknown>): EChartsOption | null => {
    const seg = data.log_balance_segment as {
      categories: string[];
      non_fraud: number[];
      fraud: number[];
    } | undefined;

    if (!seg) return null;

    return {
      title: { text: 'Balance Segment (Log Scale)' },
      tooltip: { trigger: 'axis' },
      legend: { data: ['Non-fraud', 'Fraud'] },
      xAxis: { type: 'category', data: seg.categories },
      yAxis: { type: 'log' },
      series: [
        { name: 'Non-fraud', type: 'bar', data: seg.non_fraud, itemStyle: { color: '#5470c6' } },
        { name: 'Fraud', type: 'bar', data: seg.fraud, itemStyle: { color: '#ee6666' } }
      ]
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

  const getHourlyActivityChart = (data: Record<string, unknown>): EChartsOption | null => {
    // Support two backend shapes:
    // 1) `multi_line_hourly` with hours, normal_activity, fraud_activity (two lines)
    // 2) `hourly_volume_bar` + `hourly_fraud_rate_line` (bar + rate line, dual axis)
    const multi = data.multi_line_hourly as {
      hours: number[];
      normal_activity: number[];
      fraud_activity: number[];
    } | undefined;

    if (multi) {
      return {
        title: { text: "Hourly Transaction Activity" },
        tooltip: { trigger: "axis" },
        legend: { data: ["Normal Activity", "Fraudulent Activity"] },
        xAxis: { type: "category", data: multi.hours.map((h) => `${h}:00`) },
        yAxis: { type: "value" },
        series: [
          {
            name: "Normal Activity",
            type: "line",
            data: multi.normal_activity,
            smooth: true,
            itemStyle: { color: "#5470c6" },
            areaStyle: { color: "rgba(84, 112, 198, 0.3)" },
          },
          {
            name: "Fraudulent Activity",
            type: "line",
            data: multi.fraud_activity,
            smooth: true,
            itemStyle: { color: "#ee6666" },
            areaStyle: { color: "rgba(238, 102, 102, 0.3)" },
          },
        ],
      };
    }

    const vol = data.hourly_volume_bar as {
      hours: number[];
      volume: number[];
    } | undefined;
    const rate = data.hourly_fraud_rate_line as {
      hours: number[];
      rate: number[];
    } | undefined;

    if (vol && rate) {
      return {
        title: { text: "Hourly Volume and Fraud Rate" },
        tooltip: { trigger: 'axis' },
        legend: { data: ['Volume', 'Fraud Rate (%)'] },
        xAxis: { type: 'category', data: vol.hours.map((h) => `${h}:00`) },
        yAxis: [
          { type: 'value', name: 'Volume' },
          { type: 'value', name: 'Fraud Rate (%)', position: 'right' }
        ],
        series: [
          { name: 'Volume', type: 'bar', data: vol.volume, yAxisIndex: 0, itemStyle: { color: '#5470c6' } },
          { name: 'Fraud Rate (%)', type: 'line', data: rate.rate, yAxisIndex: 1, smooth: true, itemStyle: { color: '#ee6666' } }
        ]
      };
    }

    return null;
  };

  // derive a stable summary object from backend shapes
  const deriveSummary = (pred: PredictionResult | null) => {
    if (!pred) return null;
    const eda = (pred.data as any).eda_data ?? {};
    const s = (pred.data as any).summary ?? {};

    const total_transactions = s.total_transactions ?? s.total_rows ?? s.total_rows ?? (eda.data_overview?.total_rows) ?? 0;
    const fraud_detected = s.fraud_detected ?? ((eda.class_distribution && (eda.class_distribution.Fraud ?? eda.class_distribution['Fraud'])) ?? 0);
    const fraud_rate_percent = s.fraud_rate_percent ?? (total_transactions ? Math.round((fraud_detected / total_transactions) * 10000) / 100 : 0);

    return {
      total_transactions,
      fraud_detected,
      fraud_rate_percent,
    };
  };

  return (
    <div className="rain-scene" style={{ minHeight: "100vh", display: "flex", flexDirection: "column", overflowY: "auto" }}>
      <header className="site-header" style={{ textAlign: "center" }}>
        <h1>Analysis tool</h1>
      </header>
      {/* Tabs */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: 12, marginTop: 12 }}>
        <button
          onClick={() => setActiveTab('analysis')}
          className={`tab-button ${activeTab === 'analysis' ? 'active' : ''}`}
        >Analysis</button>
        <button
          onClick={() => setActiveTab('transaction')}
          className={`tab-button ${activeTab === 'transaction' ? 'active' : ''}`}
        >Transaction Input</button>
        <button
          onClick={() => setActiveTab('models')}
          className={`tab-button ${activeTab === 'models' ? 'active' : ''}`}
        >Model Comparison</button>
      </div>
      {/* Window glass grid */}
      <div className="glass" aria-hidden />

      {/* Center file drop area (only show on Analysis tab) */}
      {activeTab === 'analysis' && (
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
      )}

      {/* Model Comparison view (inlined) */}
      {activeTab === 'models' && (
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem', width: '100%' }}>
          <div className="panel" id="panel-cmp" style={{ width: '100%', maxWidth: 1200 }}>
            <div className="section-label" style={{ marginTop: 0 }}>
              Model comparison — online payment fraud detection
            </div>

            <div className="compare-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Criterion</th>
                    <th>Logistic Reg.</th>
                    <th>Random Forest</th>
                    <th>XGBoost</th>
                    <th>CatBoost</th>
                    <th>LightGBM</th>
                  </tr>
                </thead>

                <tbody>
                  <tr>
                    <td><strong>Structure</strong></td>
                    <td>Linear model, sigmoid</td>
                    <td>Parallel bagged trees</td>
                    <td>Sequential boosted trees (2nd order)</td>
                    <td>Sequential symmetric trees</td>
                    <td>Leaf-wise boosted trees</td>
                  </tr>

                  <tr>
                    <td><strong>AUC-ROC (fraud)</strong></td>
                    <td>~0.80–0.85</td>
                    <td>~0.90–0.94</td>
                    <td className="winner">~0.95–0.98</td>
                    <td className="winner">~0.95–0.98</td>
                    <td className="winner">~0.95–0.98</td>
                  </tr>

                  <tr>
                    <td><strong>Precision-Recall</strong></td>
                    <td>Low recall</td>
                    <td>Good</td>
                    <td>Excellent</td>
                    <td>Excellent</td>
                    <td className="winner">Excellent</td>
                  </tr>

                  <tr>
                    <td><strong>Training speed</strong></td>
                    <td className="winner">Fastest</td>
                    <td>Slow (many trees)</td>
                    <td>Medium</td>
                    <td>Medium-slow</td>
                    <td className="winner">Fastest boosting</td>
                  </tr>

                  <tr>
                    <td><strong>Inference speed</strong></td>
                    <td className="winner">Fastest</td>
                    <td>Slow</td>
                    <td>Fast</td>
                    <td className="winner">Fastest (lookup)</td>
                    <td>Fast</td>
                  </tr>

                  <tr>
                    <td><strong>Class imbalance</strong></td>
                    <td>Poor (needs SMOTE)</td>
                    <td>class_weight</td>
                    <td>scale_pos_weight</td>
                    <td>class_weights</td>
                    <td>is_unbalance</td>
                  </tr>

                  <tr>
                    <td><strong>Categorical features</strong></td>
                    <td>Manual encoding</td>
                    <td>Manual encoding</td>
                    <td>Manual encoding</td>
                    <td className="winner">Native (no encoding)</td>
                    <td>Partial native</td>
                  </tr>

                  <tr>
                    <td><strong>Missing values</strong></td>
                    <td>Manual imputation</td>
                    <td>Native</td>
                    <td className="winner">Native</td>
                    <td className="winner">Native</td>
                    <td className="winner">Native</td>
                  </tr>

                  <tr>
                    <td><strong>Overfitting risk</strong></td>
                    <td>Low (regularized)</td>
                    <td>Low</td>
                    <td>Low (λ, α regs)</td>
                    <td>Very low (ordered boosting)</td>
                    <td>Medium (leaf-wise)</td>
                  </tr>

                  <tr>
                    <td><strong>Explainability</strong></td>
                    <td className="winner">High (coefficients)</td>
                    <td>Medium (feat. importance)</td>
                    <td>Medium (SHAP)</td>
                    <td>Medium (SHAP)</td>
                    <td>Medium (SHAP)</td>
                  </tr>

                  <tr>
                    <td><strong>Memory usage</strong></td>
                    <td className="winner">Minimal</td>
                    <td>High</td>
                    <td>Medium-high</td>
                    <td>Medium-high</td>
                    <td className="winner">Low (histogram)</td>
                  </tr>

                  <tr>
                    <td><strong>Best for fraud when…</strong></td>
                    <td>Audit/compliance needed</td>
                    <td>Balanced + explainability</td>
                    <td>Max accuracy, tuned pipeline</td>
                    <td>Rich categorical features</td>
                    <td>High-volume real-time</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <hr className="divider" />

            <div className="section-label">
              Fraud-specific metric scores (relative)
            </div>

            <div
              style={{
                fontSize: "12px",
                color: "var(--color-text-tertiary)",
                marginBottom: "10px",
              }}
            >
              Approximate relative performance on typical imbalanced fraud datasets
            </div>

            <div style={{ marginBottom: "1.5rem" }}>
              {[
                { name: "LightGBM", score: 97, color: "#7F77DD" },
                { name: "XGBoost", score: 96, color: "#EF9F27" },
                { name: "CatBoost", score: 95, color: "#D4537E" },
                { name: "Random Forest", score: 90, color: "#639922" },
                { name: "Logistic Regression", score: 72, color: "#378ADD" },
              ].map((model) => (
                <div className="bar-row" key={model.name}>
                  <div className="bar-label">
                    <span>{model.name}</span>
                    <span>{model.score}</span>
                  </div>

                  <div className="bar-track">
                    <div
                      className="bar-fill"
                      style={{
                        width: `${model.score}%`,
                        background: model.color,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>

            <div className="section-label">Recommended decision tree</div>

            <div className="grid2">
              <div className="adv">
                Use <strong>LightGBM</strong> → millions of transactions/day,
                speed is critical, real-time scoring needed
              </div>

              <div className="adv">
                Use <strong>XGBoost</strong> → maximum accuracy with tuning
                time, need robust well-tested pipeline
              </div>
            </div>

            <div style={{ height: "10px" }} />

            <div className="grid2">
              <div className="adv">
                Use <strong>CatBoost</strong> → many categorical fields
                (merchant, device, country), minimal preprocessing budget
              </div>

              <div className="adv">
                Use <strong>Logistic Reg.</strong> → regulatory audit,
                need weight-level explanation for each decision
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Transaction Input form (only show on Transaction tab) */}
      {activeTab === 'transaction' && (
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem' }}>
          <form onSubmit={(e) => { e.preventDefault(); handleTxSubmit(); }} className="transaction-form" style={{ width: '100%', maxWidth: 900, background: '#000', color: '#fff', padding: 20, borderRadius: 8, boxShadow: '0 6px 18px rgba(0,0,0,0.1)' }}>
            <h3 style={{ marginTop: 0, marginBottom: 16 }}>Transaction Input</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
              <label style={{ display: 'block', color: '#fff' }}>
                Amount
                <input name="amount" value={txForm.amount} onChange={handleTxChange} type="number" step="any" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
              </label>
              <label style={{ display: 'block', color: '#fff' }}>
                Transaction Type
                <select name="type" value={txForm.type} onChange={handleTxChange} style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }}>
                  <option>Cash In</option>
                  <option>Cash Out</option>
                  <option>Transfer</option>
                  <option>Debit</option>
                  <option>Payment</option>
                </select>
              </label>

              <label style={{ display: 'block', color: '#fff' }}>
                Sender Name (nameOrig)
                <input name="nameOrig" value={txForm.nameOrig} onChange={handleTxChange} type="text" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
              </label>
              <label style={{ display: 'block', color: '#fff' }}>
                Receiver Name (nameDest)
                <input name="nameDest" value={txForm.nameDest} onChange={handleTxChange} type="text" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
              </label>

              <label style={{ display: 'block', color: '#fff' }}>
                Sender Old Balance (oldBalanceOrig)
                <input name="oldBalanceOrg" value={txForm.oldBalanceOrg} onChange={handleTxChange} type="number" step="any" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
              </label>
              <label style={{ display: 'block', color: '#fff' }}>
                Sender New Balance (newBalanceOrig)
                <input name="newBalanceOrig" value={txForm.newBalanceOrig} onChange={handleTxChange} type="number" step="any" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
              </label>

              <label style={{ display: 'block', color: '#fff' }}>
                Receiver Old Balance (oldBalanceDest)
                <input name="oldBalanceDest" value={txForm.oldBalanceDest} onChange={handleTxChange} type="number" step="any" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
              </label>
              <label style={{ display: 'block', color: '#fff' }}>
                Receiver New Balance (newBalanceDest)
                <input name="newBalanceDest" value={txForm.newBalanceDest} onChange={handleTxChange} type="number" step="any" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
              </label>
            </div>

            <div style={{ marginTop: 16, display: 'flex', gap: 12 }}>
              <button type="submit" className="tx-submit">Enter</button>
              <button type="button" className="reset-button" onClick={() => { setTxForm({ amount: '', nameOrig: '', oldBalanceOrg: '', newBalanceOrig: '', nameDest: '', oldBalanceDest: '', newBalanceDest: '', type: 'Transfer' }); setTxMessage(null); }}>Reset</button>
              {txMessage && <div style={{ marginLeft: 12, alignSelf: 'center', color: '#4caf50' }}>{txMessage}</div>}
            </div>

            {/* Single prediction result */}
            {singleResult && (
              <div style={{ marginTop: 16, background: '#fff', color: '#000', padding: 12, borderRadius: 8, maxWidth: 900 }}>
                <div style={{ fontWeight: 700 }}>Transaction Result</div>
                <div style={{ marginTop: 8 }}>Decision: <strong>{singleResult.final_decision}</strong></div>
                <div>Voting: {singleResult.voting_ratio}</div>
                <div style={{ marginTop: 8 }}>
                  <div style={{ fontWeight: 600 }}>Model details:</div>
                  <ul>
                    {Array.isArray(singleResult.model_details) && singleResult.model_details.map((m: any, idx: number) => (
                      <li key={idx}>{m.model_name}: {m.is_fraud ? 'FRAUD' : 'SAFE'} ({m.confidence_score}%)</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </form>
        </div>
      )}

      {/* Results Display - Scrollable main window */}
      {predictions && predictions.status === "success" && (
        <div style={{ width: "100%", display: "flex", justifyContent: "center", marginTop: "3rem" }}>
          <div style={{ width: "100%", maxWidth: "2000px", padding: "2rem 0.5rem", boxSizing: "border-box" }}>
            <h3 style={{ marginTop: 0, marginBottom: "1.25rem", color: "#fff", fontSize: "2rem", textAlign: "center" }}>Analysis Results</h3>

            {/* Summary Stats */}
            {(() => {
              const derived = deriveSummary(predictions);
              if (!derived) return null;
              return (
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
                      {derived.total_transactions}
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
                      {derived.fraud_detected}
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
                      {derived.fraud_rate_percent}%
                    </div>
                  </div>
                </div>
              );
            })()}

            {/* Charts Grid (scrollable) */}
            <div style={{ marginTop: "2rem", overflowY: "auto", maxHeight: "calc(100vh - 320px)", paddingRight: "1rem" }}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: "2rem", width: "95%", maxWidth: "1600px", paddingBottom: "3rem" }}>
              {/* Mixed Volume vs Rate Chart */}
              {predictions.data?.eda_data?.mixed_volume_vs_rate && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                  <ReactECharts
                    option={getMixedVolumeVsRateChart(predictions.data.eda_data)}
                    style={{ height: "700px", width: "100%" }}
                  />
                </div>
              )}

              {/* Correlation Heatmap */}
              {predictions.data?.eda_data?.correlation_matrix && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)", display: 'flex', justifyContent: 'center' }}>
                  <div style={{ width: '100%', maxWidth: '1200px', aspectRatio: '1 / 1' }}>
                    <ReactECharts
                      option={getCorrelationHeatmapChart(predictions.data.eda_data)}
                      style={{ height: "100%", width: "100%" }}
                    />
                  </div>
                </div>
              )}

              {/* Class Distribution Pie */}
              {predictions.data?.eda_data?.class_distribution && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                  <ReactECharts
                    option={getClassDistributionChart(predictions.data.eda_data)}
                    style={{ height: "700px", width: "100%" }}
                  />
                </div>
              )}

              {/* Stacked Amount Ranges Chart */}
              {predictions.data?.eda_data?.stacked_amount_ranges && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                  <ReactECharts
                    option={getStackedAmountRangesChart(predictions.data.eda_data)}
                    style={{ height: "700px", width: "100%" }}
                  />
                </div>
              )}

              {/* Log Balance Segment (Grouped Bar, Log Scale) */}
              {predictions.data?.eda_data?.log_balance_segment && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                  <ReactECharts
                    option={getLogBalanceSegmentChart(predictions.data.eda_data)}
                    style={{ height: "700px", width: "100%" }}
                  />
                </div>
              )}

              {/* Zero Balance Chart */}
              {predictions.data?.eda_data?.zero_balance_behavior && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                  <ReactECharts
                    option={getZeroBalanceChart(predictions.data.eda_data)}
                    style={{ height: "700px", width: "100%" }}
                  />
                </div>
              )}

              {/* Accounting Anomalies Chart */}
              {predictions.data?.eda_data?.accounting_anomalies && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
                  <ReactECharts
                    option={getAccountingAnomaliesChart(predictions.data.eda_data)}
                    style={{ height: "700px", width: "100%" }}
                  />
                </div>
              )}

              {/* Hourly Activity Chart - Full width */}
              {(predictions.data?.eda_data?.multi_line_hourly || (predictions.data?.eda_data?.hourly_volume_bar && predictions.data?.eda_data?.hourly_fraud_rate_line)) && (
                <div style={{ backgroundColor: "#fff", borderRadius: "8px", padding: "1rem", boxShadow: "0 4px 12px rgba(0,0,0,0.2)", gridColumn: "1 / -1" }}>
                  <ReactECharts
                    option={getHourlyActivityChart(predictions.data.eda_data)}
                    style={{ height: "700px", width: "100%" }}
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
  );}
