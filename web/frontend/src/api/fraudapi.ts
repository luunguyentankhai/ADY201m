import axios from 'axios';

export interface EDAData {
    mixed_volume_vs_rate: {
        categories: string[];
        volume_bar: number[];
        rate_line: number[];
    };
    stacked_amount_ranges: {
        categories: string[];
        normal_tx: number[];
        fraud_tx: number[];
    };
    multi_line_hourly: {
        hours: number[];
        normal_activity: number[];
        fraud_activity: number[];
    };
    zero_balance_behavior: {
        Account_Empty: number;
        Account_Has_Money: number;
    };
    accounting_anomalies: {
        Perfect_Math: number;
        Suspicious_Anomaly: number;
    };
    summary: {
        total_rows: number;
        total_volume: number;
    };
}

export interface PredictResponseData {
    summary: {
        total_transactions: number;
        fraud_detected: number;
        fraud_rate_percent: number;
    };
    eda_data: EDAData;
}

export interface PredictApiResponse {
  status: string;
  message: string;
  data: PredictResponseData;
}

export const uploadCsvToBackend = async (file: File): Promise<PredictResponseData | null> => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post<PredictApiResponse>(
      "http://127.0.0.1:8000/api/predict/upload-csv",
      formData
    );
    return response.data.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error("[API_ERROR] Backend server connection failed:", error.response?.data?.detail || error.message);
      
      alert(`Lỗi: ${error.response?.data?.detail || "Không thể kết nối tới máy chủ"}`);
    }
    return null;
  }
};
