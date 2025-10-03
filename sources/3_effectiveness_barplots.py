import pandas as pd

def calc_metrics(row):
    VP, VN, FP, FN = row["VP"], row["VN"], row["FP"], row["FN"]
    acc = (VP + VN) / (VP + VN + FP + FN)
    prec = VP / (VP + FP) if (VP+FP) > 0 else 0
    rec = VP / (VP + FN) if (VP+FN) > 0 else 0
    f1 = 2*prec*rec/(prec+rec) if (prec+rec) > 0 else 0
    return pd.Series({"accuracy": acc, "precision": prec, "recall": rec, "f1_score": f1})

data_csv = "../results/application_results_overview.csv"
results_dir = "../results"

df = pd.read_csv(data_csv)

apps = df["application"].unique()

apps_df = []
for app in apps:
    df_app = df[df["application"] == app]
    df_app['type'] = df_app['type'].str.upper()
    df_app['identified'] = df_app['iteration'] != -1
    df_app['is_my_control'] = df_app['type'] == "ALTCONTROL"

    result = []
    grouped = df_app.groupby(["load", "compressor"])
    epsilon = 1e-10
    num_types = len(df_app[df_app['type']!='ALTCONTROL']["type"].unique())

    for (load, compressor), group in grouped:

        VP = ((~group['is_my_control']) & (group['identified'])).sum()
        FP = num_types*((group['is_my_control']) & (group['identified'])).sum()
        FN = ((~group['is_my_control']) & (~group['identified'])).sum()
        VN = num_types*((group['is_my_control']) & (~group['identified'])).sum()

        
        result.append({
            'application': app,
            'compressor': compressor,
            'load': load,
            'VP': VP,
            'FN': FN,
            'VN': VN,
            'FP': FP,
            # 'accuracy': round(accuracy, 4),
            # 'precision': round(precision, 4),
            # 'recall': round(recall, 4),
            # 'f1_score': round(f1_score, 4)
        })
    metrics_df = pd.DataFrame(result)
    df = metrics_df
    df["compressor"] = df["compressor"].str.upper()
    summary = (
        df.groupby(["application","compressor"])[["VP","VN","FP","FN"]]
        .sum()
        .reset_index()
    )
    metrics = summary.join(summary.apply(calc_metrics, axis=1))
    apps_df.append(metrics)

df = pd.concat(apps_df)
df.to_csv(f"{results_dir}/effectiveness_stats.csv", index=False)
print(df)
