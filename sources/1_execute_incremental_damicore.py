# THIS SCRIPT MUST BE RUN ON UBUNTU
import subprocess
import os
import pandas as pd
import numpy as np
import statistics
from utils.format import *
import argparse

data_dir = '../results/clustering_results'
data_results_dir = f'{data_dir}/RESULTS'
types = ['API', 'CONC', 'LOGIC', 'MEMORY', 'MODEL', 'PROCESS', 'TRAIN', 'ALTCONTROL']

loads = {
    "bert": ["CoLA", "MNLI", "MRPC", "SQuADv1", "SQuADv2", "XNLI"],
    "chess": ["EVAL", "OPTSTEP", "OPTTYPE", "SELF", "SL"],
    "voice": ["MIN-LONG", "MIN-MEDIUM", "MIN-SHORT", "SEC-LONG", "SEC-MEDIUM", "SEC-SHORT"],
    "decisiontree":["CANCER-PHON","IONO-SOLAR","WINE-HEART"],
    "yatserver": ["BINCSVH1", "BINCSVH2", "BINCSVH3","BINCSVL1","BINCSVL2","BINCSVL3","BINCSVM1","BINCSVM2","BINCSVM3"]
    # "decisiontree":["BANK-PIMA","CANCER-PHON","IONO-SOLAR","IRIS-HABER","OIL-MAMMO","WINE-HEART"],
    # "yatserver": ["BINCSVH1","BINCSVL1","BINCSVM1", "BINH1", "BINL1", "BINM1", "CSVH1", "CSVL1", "CSVM1"]
    # "yatserver": ["BINCSVH1", "BINCSVH2", "BINCSVH3","BINCSVL1","BINCSVL2","BINCSVL3","BINCSVM1","BINCSVM2","BINCSVM3", "BINH1", "BINL1", "BINM1", "CSVH1", "CSVL1", "CSVM1"]
}



def compute_boxplot_stats(group):
    times = group['time'].tolist()

    avg_time = sum(times) / len(times)
    median_time = statistics.median(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0
    min_time = min(times)
    max_time = max(times)
    q1 = np.percentile(times, 25)
    q3 = np.percentile(times, 75)
    iqr = q3 - q1

    # Whiskers
    lower_whisker = min([v for v in times if v >= q1 - 1.5 * iqr], default=min_time)
    upper_whisker = max([v for v in times if v <= q3 + 1.5 * iqr], default=max_time)

    # Outliers
    outliers = [v for v in times if v < lower_whisker or v > upper_whisker]
    num_outliers = len(outliers)

    return pd.Series({
        'avg_time': avg_time,
        'std_dev': std_dev,
        'min_time': min_time,
        'max_time': max_time,
        'q1': q1,
        'median_time': median_time,
        'q3': q3,
        'iqr': iqr,
        'lower_whisker': lower_whisker,
        'upper_whisker': upper_whisker,
        'num_outliers': num_outliers
    })

applications = os.listdir("../profiles")

# ----------------- ARGUMENT PARSING -----------------
parser = argparse.ArgumentParser(description="Run Damicore and compute incremental stats.")
parser.add_argument(
    "--apps", 
    nargs="+", 
    default=applications, 
    help="List of applications to run (default: all apps defined in loads)"
)
args = parser.parse_args()
selected_apps = args.apps
# -----------------------------------------------------


for app in selected_apps:
    if app not in loads:
        print(f"⚠️ Skipping {app}: not defined in default loads dict")
        continue

    # EXECUTE DAMICORE
    script = "execute_damicore.sh"
    output = ""
    params = [
        '--reps', '30',
        '--input', app,
        '--output', f"clustering_results/{app.upper()}",
        '--loads'
    ]

    for load in loads[app]:
        params.extend([load])

    result = subprocess.run(['bash', script] + params, capture_output=False, text=True)


    # GENERATE INCREMENTAL DF
    all_stats = []
    for load in os.listdir(data_results_dir):
        load_dir = f"{data_results_dir}/{load}"
        for type in os.listdir(load_dir):
            if type not in types:
                continue
            file_path = f"{load_dir}/{type}"

            df = pd.read_json(file_path)
            grouped = df.groupby(['load','type','compressor','iteration'])
            stats_df = grouped.apply(compute_boxplot_stats).reset_index()
            all_stats.append(stats_df)

    # Juntar tudo em um único DataFrame final
    final_df = pd.concat(all_stats, ignore_index=True)
    final_df["compressor"] = final_df["compressor"].str.upper()
    final_df.to_csv(f"../results/incremental_stats.csv")