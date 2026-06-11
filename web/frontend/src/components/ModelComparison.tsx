import React from "react";

export default function ModelComparison() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem', width: '100%' }}>
      <div className="panel" id="panel-cmp" style={{ width: '100%', maxWidth: 1200 }}>
        <div className="section-label" style={{ marginTop: 0 }}>Model comparison — online payment fraud detection</div>

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

        <div className="section-label">Fraud-specific metric scores (relative)</div>

        <div style={{ fontSize: "12px", color: "var(--color-text-tertiary)", marginBottom: "10px" }}>Approximate relative performance on typical imbalanced fraud datasets</div>

        <div style={{ marginBottom: "1.5rem" }}>
          {[{ name: "LightGBM", score: 97, color: "#7F77DD" }, { name: "XGBoost", score: 96, color: "#EF9F27" }, { name: "CatBoost", score: 95, color: "#D4537E" }, { name: "Random Forest", score: 90, color: "#639922" }, { name: "Logistic Regression", score: 72, color: "#378ADD" }].map((model) => (
            <div className="bar-row" key={model.name}>
              <div className="bar-label"><span>{model.name}</span><span>{model.score}</span></div>
              <div className="bar-track"><div className="bar-fill" style={{ width: `${model.score}%`, background: model.color }} /></div>
            </div>
          ))}
        </div>

        <div className="section-label">Recommended decision tree</div>

        <div className="grid2">
          <div className="adv">Use <strong>LightGBM</strong> → millions of transactions/day, speed is critical, real-time scoring needed</div>
          <div className="adv">Use <strong>XGBoost</strong> → maximum accuracy with tuning time, need robust well-tested pipeline</div>
        </div>

        <div style={{ height: "10px" }} />

        <div className="grid2">
          <div className="adv">Use <strong>CatBoost</strong> → many categorical fields (merchant, device, country), minimal preprocessing budget</div>
          <div className="adv">Use <strong>Logistic Reg.</strong> → regulatory audit, need weight-level explanation for each decision</div>
        </div>
      </div>
    </div>
  );
}
