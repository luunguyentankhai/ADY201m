import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.config.logs_config import setup_log, auto_logger
from src.config.dir_config import Assets_Dir
from src.utils.file_helpers import is_cache

logger = setup_log(name="Visualization", filename="app")
sns.set_style("whitegrid")

@auto_logger(logger)
def plt_top_fraud_entities(df, button=True, filename="temp"):
    save_path = Assets_Dir / f"{filename}.png"

    if is_cache(save_path, isredraw=button, size=(18, 6)):
        return

    logger.info("Analyzing top 10 occurrences for step, nameOrig, and nameDest in fraud data")

    df_fraud = df[df['is_fraud'] == 1]

    top_step = df_fraud['step'].value_counts().head(10)
    top_orig = df_fraud['name_orig'].value_counts().head(10)
    top_dest = df_fraud['name_dest'].value_counts().head(10)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    

    data_list = [
        (top_step, 'step', 'Top 10 Steps in Fraudulent Transactions'),
        (top_orig, 'nameOrig', 'Top 10 Origin Accounts (Throwaway)'),
        (top_dest, 'nameDest', 'Top 10 Destination Accounts (Mule)')
    ]

    for i, (data, col_name, title) in enumerate(data_list):
        ax = data.plot(kind='bar', color='lightsteelblue', ax=axes[i])
        
        for container in ax.containers:
            ax.bar_label(container, padding=3)
            
        axes[i].set_xlabel(col_name, fontsize=12, fontweight='bold', labelpad=10)
        axes[i].set_ylabel('Number of transactions')
        axes[i].set_title(title)
        
        axes[i].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    logger.info(f"New img at {save_path}")
