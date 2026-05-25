import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.config.logs_config import setup_log, auto_logger
from src.config.dir_config import Assets_Dir
from src.utils.file_helpers import is_cache

logger = setup_log(name="Visualization", filename="app")

@auto_logger(logger)
def plt_corr_matrix(df, button=True, filename="temp"):
    
    save_path = Assets_Dir / f"{filename}.png"

    if is_cache(save_path, isredraw=button):
        return

    logger.info(f"Plotting correlation heatmap")
    plt.figure(figsize=(12, 10))
        
    # Filter numerical columns only
    numberic_cols = df.select_dtypes(include=['number']).columns
    # Drop identifier columns
    corr_matrix = df[numberic_cols].corr('spearman')
    sns.heatmap(corr_matrix, cbar= True, annot=True, fmt='.3f', cmap= 'PuBu', mask= np.triu(np.ones_like(corr_matrix, dtype= bool)))
    plt.title('Matrix Correlation', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    logger.info(f"New img at {save_path}")
