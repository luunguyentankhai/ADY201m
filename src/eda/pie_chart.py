import matplotlib.pyplot as plt
import pandas as pd
from src.config.dir_config import Assets_Dir
from src.utils.file_helpers import is_cache
from src.config.logs_config import setup_log, auto_logger

logger = setup_log(name="Visualization", filename="app")

@auto_logger(logger)
def plt_pie_class_distribution(df, button=True, filename="temp"):
    save_path = Assets_Dir / f"{filename}.png"

    if is_cache(save_path, isredraw=button, size=(8,8)):
        return

    logger.info("Generating Pie Chart for isFraud class distribution")

    counts = df["is_fraud"].value_counts()
    
    plt.figure(figsize=(8, 8))
    
    colors = ['#4CAF50', '#F44336']
    
    explode = [0 if label == 0 else 0.2 for label in counts.index]
    
    plt.pie(counts, labels=['Non-Fraud (0)\n', 'Fraud (1)\n'], colors=colors, 
            autopct='%1.2f%%', startangle=90, explode=explode,
            textprops={'fontsize': 12})
            
    plt.xlabel('Class Distribution (is_fraud)', fontsize=14, labelpad=20, fontweight='bold')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    logger.info(f"New img at {save_path}")
