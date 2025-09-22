import pandas as pd
import numpy as np
import os
from utils.XYPlot import XYPlot, Legend

selected_load = 'OIL-MAMMO'

color_map = {
    "BZ2": "#1f77b4",
    "GZIP": "#1f77b4",
    "ENTROPY": "#1f77b4",
    "PPMD": "#1f77b4",
    "ZLIB": "#1f77b4"
}

marker_map = {
    "MEMORY": "o",
    "API": "X",
    "PROCESS": "*"
}

output_dir="../results/"
os.makedirs(output_dir, exist_ok=True)

times_data = "../results/incremental_stats.csv"
perf_data = "../results/incremental_performance_stats.csv"


df_times = pd.read_csv(times_data)
df_times = df_times[df_times['load']==selected_load]

df_perf = pd.read_csv(perf_data).drop(columns=['Unnamed: 0'])
df_perf = df_perf[df_perf['load']==selected_load]

df_eficacia = df_perf[['compressor','accuracy']]
df_eficiencia = df_times[['compressor', 'type', 'median_time']]
df = pd.merge(df_eficiencia, df_eficacia, on='compressor')

df['inv_median_time'] = 1 / df['median_time']

types = df_times['type'].unique()
df["efficiency"] = np.nan
df["efficacy"] = np.nan

for t in types:
    mask = df["type"] == t
    subset = df[mask]
    min_inv = subset["inv_median_time"].min()
    max_inv = subset["inv_median_time"].max()

    # Normalização dentro do grupo e atribuição apenas nas linhas do grupo
    df.loc[mask, "efficiency"] = (
        (subset["inv_median_time"] - min_inv) / (max_inv - min_inv)
    )

    min_f1 = subset["accuracy"].min()
    max_f1 = subset["accuracy"].max()
    
    if max_f1 - min_f1 == 0:
        df.loc[mask, "efficacy"] = max_f1  # valor neutro se todos iguais
    else:
        df.loc[mask, "efficacy"] = (
            (subset["accuracy"] - min_f1) / (max_f1 - min_f1)
        )

df = df[['type','compressor', 'efficacy','efficiency']]
df["color"] = df["compressor"].map(color_map)
    
print(df)
input()
legend = Legend(
    "Tipo de compressor", 
    ["#d62728", "#1f77b4"], 
    ["Imagem", "Texto"],
    fontsize= 12,
)
plot = XYPlot(
    title_size=32,
    ylabel="Effectiveness",
    xlabel_size=24,
    xlabel="Efficiency",
    ylim=(-0.05, 1.075),
    ylabel_size=24,
    rotation_x=0,
    rotation_y=0,
    legend = legend,
    figsize=(6,6)
)

plots = [
    lambda ax: plot.scatterplot(
        data=df[df['type']=='MEMORY'],
        x="efficiency",
        y="efficacy",
        label_col="compressor",
        # color_col="color",
        use_adjust_text=True,
        show_grid=True,
        point_style=dict(s=25),
        text_style=dict(fontsize=14, color="black", fontweight="bold"),
        show_legend=False,
        pound_x=3,
        pound_y=2,
        offset_x=0.25,
        offset_y=0.05,
        title="MEMORY",
        ax=ax,
        show_plot=False
    ),
    lambda ax: plot.scatterplot(
        data=df[df['type']=='API'],
        x="efficiency",
        y="efficacy",
        label_col="compressor",
        # color_col="color",
        pound_x=1,
        pound_y=1,
        offset_x=0.1,
        offset_y=0.05,
        use_adjust_text=True,
        show_grid=True,
        point_style=dict(s=25),
        text_style=dict(fontsize=14, color="black", fontweight="bold"),
        show_legend=False,
        title="API",
        ax=ax,
        show_xlabel=False,
        show_plot=False
    ),
    lambda ax: plot.scatterplot(
        data=df[df['type']=='PROCESS'],
        y="efficacy",
        x="efficiency",
        label_col="compressor",
        pound_x=1,
        pound_y=3,
        offset_x=0.05,
        offset_y=0.08,
        use_adjust_text=True,
        show_grid=True,
        point_style=dict(s=25),
        text_style=dict(fontsize=14, color="black", fontweight="bold"),
        show_legend=False,
        title="PROCESS",
        ax=ax,
        show_plot=False,
        show_xlabel=False
    ),
]



plot.generate_multiplots(
    plot_functions=plots,
    title=f"Effectiveness versus efficiency map by anomaly types",
    nrows=3,
    ncols=1,
    output_image_path=f"{output_dir}/{selected_load}_efficiency_effectiveness.png"
)
