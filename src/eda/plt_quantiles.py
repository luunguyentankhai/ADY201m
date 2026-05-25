import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.config.logs_config import setup_log, auto_logger
from src.config.dir_config import Assets_Dir
from src.utils.file_helpers import is_cache

logger = setup_log(name="Visualization", filename="app")
sns.set_style("whitegrid")

@auto_logger(logger)
def plt_quantiles_analysis(df, cols, button=True, filename="temp"):
    for col in cols:
        save_path = Assets_Dir / f"{filename}_{col}.png"

        if is_cache(save_path, isredraw=button, size=(10,6)):
            continue

        logger.info(f"Analyzing quantity qcut for {col} column")

        bin_col_name = f"{col}_quantity"

        full_labels = ['very low', 'low', 'moderate', 'high', 'very high']
        _, bin_edges = pd.qcut(df[col], q=5, duplicates='drop', retbins=True)
        actual_bin_count = len(bin_edges) - 1
        dynamic_labels = full_labels[:actual_bin_count]

        df[bin_col_name] = pd.qcut(df[col], q=5, labels=dynamic_labels, duplicates="drop")

        plt.figure(figsize=(10,6))
        ax=sns.countplot(data=df, x=bin_col_name, hue="is_fraud", palette="PuBu")

        for container in ax.containers:
            ax.bar_label(container, fmt='%d', padding=3)

        ax.set_yscale("log")

        plt.title(f'Fraud Ratio by {col} Quantiles (Log Scale)')
        plt.xlabel(f'{col} Quantiles')
        plt.ylabel('Number of transactions (Log)')

        plt.legend(title='isFraud', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()
        logger.info(f"New img at {save_path}")

        df.drop(columns=[bin_col_name], inplace=True)
