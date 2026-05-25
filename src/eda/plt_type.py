import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.config.logs_config import setup_log, auto_logger
from src.config.dir_config import Assets_Dir
from src.utils.file_helpers import is_cache

logger= setup_log(name="Visualization", filename="app")
sns.set_style("whitegrid")

@auto_logger(logger)
def plt_type_transaction(df, button=True, filename="temp"):
    save_path = Assets_Dir / f"dist_{filename}.png"

    if is_cache(save_path, isredraw=button, size=(20,6)):
        return

    logger.info(f"Plotting distributing fraud by type transaction")
    fig, ax = plt.subplots(1,2, figsize=(20,6))

    sns.countplot(x="type", data=df, hue="is_fraud", palette="PuBu", ax=ax[0])
    for container in ax[0].containers:
        ax[0].bar_label(container, fmt="%d", padding=3)

    ax[0].set_yscale('log')
    ax[0].set_title("Figure transaction by type")
    ax[0].set_ylabel("Figure")

    df2 = df.groupby(["type", "is_fraud"]).size().unstack(fill_value=0)
    df2_pct = df2.apply(lambda x: round(x/sum(x)*100, 2), axis=1)

    df2_pct.plot(kind='barh', stacked=True, color=['lightsteelblue', 'steelblue'], ax=ax[1])

    for container in ax[1].containers:
        ax[1].bar_label(container, label_type='center', color='black')

    ax[1].set_title('Precentant of fraud and normal')
    ax[1].set_xlabel('Precent (%)')
    ax[1].set_ylabel('Type transactions (Type)')
    ax[1].legend(title='isFraud', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    logger.info(f"New img at {save_path}")

