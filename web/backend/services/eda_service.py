import pandas as pd
from web.backend.config.logs_config import logger

class EDA:
    def excute_eda(self, df: pd.DataFrame) -> dict:
        logger.info("Extracting EDA data")
        eda_dict = {}
        target_col = 'is_fraud' if 'is_fraud' in df.columns else None

        # TODO: table data overview
        safe_df = df.head(1000).where(pd.notnull(df), None)
        eda_dict['data_overview'] = {
                "total_rows": len(df),
                "columns": df.columns.tolist(),
                "rows_preview": safe_df.to_dict(orient='records')
                }

        # TODO: Ma trận tương quan
        numberic_df = df.select_dtypes(include=['number'])
        if not numberic_df.empty:
            corr_matrix = numberic_df.corr().round(3)
            features = corr_matrix.columns.tolist()
            heatmap_data = []

            for i in range(len(features)):
                for j in range(i + 1):
                    val = corr_matrix.iloc[i, j]
                    if pd.notna(val):
                        heatmap_data.append([j, i, float(val)])

            eda_dict['correlation_matrix']= {
                    "categories": features,
                    "heatmap_data": heatmap_data
                    }

        # TODO: pie chart class distribution
        if target_col:
            fraud_count = df[target_col].value_counts()
            eda_dict['class_distribution'] = {
                    "Non-fraud": int(fraud_count.get(0,0)),
                    "Fraud": int(fraud_count.get(1,0))
                    }

        # TODO: mixed charts (bar + line) Khối lượng và tỉ lệ lừa đảo theo giao dịch
        if 'type' in df.columns:
            logger.info(f"Volume vs Fraud Rate by transaction")
            if target_col:
                grouped_type = df.groupby('type').agg(
                        total_volume=(target_col, 'count'),
                        fraud_case=(target_col, 'sum')
                        )
                grouped_type['fraud_rate']=(grouped_type['fraud_case'] / grouped_type['total_volume']) * 100
                eda_dict['mixed_volume_vs_rate']= {
                        "categories": grouped_type.index.tolist(),
                        "volume_bar": grouped_type['total_volume'].tolist(),
                        "rate_line": grouped_type['fraud_case'].round(2).tolist()
                        }
            else:
                type_counts=df['type'].value_counts()
                eda_dict['mixed_volume_vs_rate']={
                        "categories": type_counts.index.tolist(),
                        "volume_bar": type_counts.tolist(),
                        "rate_line": [0] * len(type_counts)
                        }

        # TODO: volumns xài bar và fraud_rate xài line
        if 'hour_of_day' in df.columns:
            if target_col:
                grouped_hour = df.groupby('hour_of_day').agg(
                        total=(target_col, 'count'),
                        fraud=(target_col, 'sum')
                        )
                grouped_hour['fraud_rate'] = (grouped_hour['fraud'] / grouped_hour['total']) * 100

                full_hours = pd.DataFrame(index=range(24))
                grouped_hour = full_hours.join(grouped_hour).fillna(0)

                # Đã tách biệt hoàn toàn thành 2 cụm dữ liệu độc lập cho UI
                eda_dict['hourly_volume_bar'] = {
                        "hours": list(range(24)),
                        "volume": grouped_hour['total'].tolist()
                        }
                eda_dict['hourly_fraud_rate_line'] = {
                        "hours": list(range(24)),
                        "rate": grouped_hour['fraud_rate'].round(2).tolist()
                        }
            else:
                hour_counts = df['hour_of_day'].value_counts().sort_index()
                full_hours = pd.Series(0, index=range(24))
                full_hours.update(hour_counts)

                eda_dict['hourly_volume_bar'] = {
                        "hours": list(range(24)),
                        "volume": full_hours.tolist()
                        }
                eda_dict['hourly_fraud_rate_line'] = {
                        "hours": list(range(24)),
                        "rate": [0] * 24
                        }

        # TODO: fix stackbar sao cho hiện to ra
        if 'amount' in df.columns:
            bins = [-1, 10000, 100000, 500000, float('inf')]
            labels = ['<10K', '10K - 100K', '100K - 500K', '>500K']

            df_amt = df.copy()
            df_amt['amount_range'] = pd.cut(df_amt['amount'], bins=bins, labels=labels)

            if target_col:
                grouped_amt = df_amt.groupby('amount_range', observed=False).agg(
                        total=(target_col, 'count'),
                        fraud=(target_col, 'sum')
                        )
                grouped_amt['normal'] = grouped_amt['total'] - grouped_amt['fraud']

                # TÍNH TOÁN PHẦN TRĂM ĐỂ VẼ 100% STACKED BAR (Giúp phần lừa đảo luôn hiện rõ)
                grouped_amt['fraud_percent'] = (grouped_amt['fraud'] / grouped_amt['total']) * 100
                grouped_amt['normal_percent'] = (grouped_amt['normal'] / grouped_amt['total']) * 100

                eda_dict['stacked_amount_ranges'] = {
                        "categories": labels,
                        "normal_tx": grouped_amt['normal'].tolist(),
                        "fraud_tx": grouped_amt['fraud'].tolist(),
                        # Trả thêm % cho Frontend vẽ cột
                        "normal_percent": grouped_amt['normal_percent'].round(2).fillna(0).tolist(),
                        "fraud_percent": grouped_amt['fraud_percent'].round(2).fillna(0).tolist()
                        }
            else:
                amt_counts = df_amt['amount_range'].value_counts(sort=False)
                eda_dict['stacked_amount_ranges'] = {
                        "categories": labels,
                        "normal_tx": amt_counts.tolist(),
                        "fraud_tx": [0] * len(labels),
                        "normal_percent": [100.0] * len(labels),
                        "fraud_percent": [0.0] * len(labels)
                        }

        # TODO: bar charts phân thống giao địch người gửi (CHART MỚI - Grouped Bar Log Scale)
        if 'oldbalance_orig' in df.columns:
            bins = [-1, 10000, 100000, 500000, 5000000, float('inf')]
            labels = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']

            df_seg = df.copy()
            df_seg['balance_segment'] = pd.cut(df_seg['oldbalance_orig'], bins=bins, labels=labels)

            if target_col:
                grouped_seg = df_seg.groupby('balance_segment', observed=False).agg(
                        total=(target_col, 'count'),
                        fraud=(target_col, 'sum')
                        )
                grouped_seg['normal'] = grouped_seg['total'] - grouped_seg['fraud']

                eda_dict['log_balance_segment'] = {
                        "categories": labels,
                        "non_fraud": grouped_seg['normal'].tolist(),
                        "fraud": grouped_seg['fraud'].tolist()
                        }
            else:
                seg_counts = df_seg['balance_segment'].value_counts(sort=False)
                eda_dict['log_balance_segment'] = {
                        "categories": labels,
                        "non_fraud": seg_counts.tolist(),
                        "fraud": [0] * len(labels)
                        }

        # TODO: Donut chart phân tích hành vi làm trống số dư
        col_new_bal = 'newbalanceOrig' if 'newbalanceOrig' in df.columns else 'newbalance_orig'
        if col_new_bal in df.columns:
            logger.info(f"Analyzing zero-balance behavior on origin accounts")
            zero_count = int((df[col_new_bal] == 0).sum())
            non_zero_count = int((df[col_new_bal] != 0).sum())
            eda_dict['zero_balance_behavior'] = {
                    "Account_Empty": zero_count,
                    "Account_Has_Money": non_zero_count
                    }

        # TODO: Bar chart bất cân đối kế toán (giải thích lại)
        col_old_bal = 'oldbalanceOrg' if 'oldbalanceOrg' in df.columns else 'oldbalance_orig'
        if all(c in df.columns for c in ['amount', col_old_bal, col_new_bal]):
            logger.info(f"Detecting accounting anomalies based on balance changes")
            error_margin = (df[col_old_bal] - df[col_new_bal]) - df['amount']
            anomalies_count = int((error_margin.round(2) != 0).sum())
            normal_count = int(len(df) - anomalies_count)

            eda_dict['accounting_anomalies'] = {
                    "Perfect_Math": normal_count,
                    "Suspicious_Anomaly": anomalies_count
                    }

        eda_dict['summary'] = {
                "total_rows": len(df),
                "total_volume": float(df['amount'].sum()) if 'amount' in df.columns else 0.0
                }

        logger.info(f"XONG")
        return eda_dict

eda_service = EDA()
