import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.config.logs_config import setup_log, auto_logger
from src.config.dir_config import Assets_Dir
from src.utils.file_helpers import is_cache

logger = setup_log(name="Visualization", filename="app")
sns.set_style('whitegrid')

@auto_logger(logger)
def plt_transaction(df, money_cols, button=True, filename="temp"):
    
    for col in money_cols:
        save_path = Assets_Dir / f"{filename}_{col}.png"

        if is_cache(save_path, isredraw=button, size=(14,6)):
            continue
        logger.info("Plotting boxplot and histogram")
    
        # Chỗ này ép về logarit
        log_data = np.log1p(df[col])


        fig, axes = plt.subplots(1,2,figsize=(14, 6))
        
        # này vẽ boxplot
        sns.boxplot(x=log_data, ax=axes[0], color='skyblue')
        axes[0].set_title(f"Boxplot of log(1 + {col})")
        axes[0].set_xlabel("Log Scale Value")
        
        # này vẽ histogram
        sns.histplot(x=log_data, kde=True, bins=50, ax=axes[1], color='coral')
        axes[1].set_title(f"Histogram of log(1 + {col})")
        axes[1].set_xlabel("Log Scale Value")

        # căn chỉnh lại
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()
        logger.info(f"New img at {save_path}")

    
