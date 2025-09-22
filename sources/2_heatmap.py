import os
import pandas as pd
import numpy as np
import statistics
from utils.format import *
from utils.heatmap import HeatmapPlot

compressor_order = ['ZLIB', 'PPMD', 'GZIP','BZ2', 'ENTROPY']
type_order = ['ANOTHER\nCONTROL', 'MEMORY', 'MODEL', 'LOGIC', 'TRAIN', 'API', 'CONC', 'PROCESS']

input_csv = '../results/incremental_stats.csv'
output_dir = "../results"
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv(input_csv, sep=',', decimal='.')
df["type"] = df["type"].str.replace("-", "\n")
df = order_df_by_type(df, type_order)
df = order_df_by_compressor(df, compressor_order)

# Instancia e configura o heatmap
heatmap = HeatmapPlot(
    xlabel="Anomaly type",
    ylabel="Compressor",
    cmap="RdYlGn_r",
    fmt=".0f",    
    title_size=20, 
    xlabel_size=16, 
    ylabel_size=16,
    exceptions=[-1.0],
    exception_color="#9e9e9e",
    figsize=(8, 4),
    show_xlabel=False
)

heatmap2 = HeatmapPlot(
    xlabel="Anomaly type",
    ylabel="Compressor",
    cmap="RdYlGn_r",
    fmt=".2f",    
    title_size=20, 
    xlabel_size=16, 
    ylabel_size=16,
    exceptions=[-1.0],
    exception_color="#9e9e9e",
    figsize=(8, 6),
    
)

plots = [
    lambda ax: heatmap.generate(
        ax=ax,
        data=df,
        title="Iteration matrix",
        index_col="compressor",
        columns_col="type",
        values_col="iteration",
        show_plot=False
    ),
    lambda ax: heatmap2.generate(
        ax = ax,
        data=df,
        title="Median response time matrix (s)",
        index_col="compressor",
        columns_col="type",
        values_col="median_time",
        show_plot=False,
    )
]

heatmap.generate_multiplots(
    plot_functions=plots, 
    nrows=2,
    ncols=1,
    title="Anomaly identification matrices",
    output_image_path=f"{output_dir}/heatmap_iterative.png"
)

