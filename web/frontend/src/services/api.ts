import type { PredictionResult, SinglePredictionResult } from "../types/prediction";

const BASE = "http://127.0.0.1:8000";

export async function uploadCsv(file: File): Promise<PredictionResult> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE}/api/predict/upload-csv`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText} ${text}`);
  }

  return res.json();
}

export async function predictSingle(payload: Record<string, any>): Promise<{ status: string; data: SinglePredictionResult }> {
  const res = await fetch(`${BASE}/api/predict/single`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText} ${text}`);
  }

  return res.json();
}
