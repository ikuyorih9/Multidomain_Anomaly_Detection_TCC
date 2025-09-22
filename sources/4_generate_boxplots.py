import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from utils.boxplot import BoxplotPlot
from utils.format import *

selected_load = 'CANCER-PHON'

dir = "../results/clustering_results/RESULTS"
images=f"../results"
os.makedirs(images, exist_ok=True)

plotter = BoxplotPlot(
    xlabel="Time (s)",
    ylabel="Compressor",
    title_size=24,
    xlabel_size=16,
    ylabel_size=16,
    ticklabel_size=16,
    figsize=(3, 5),
    rotation_x=45,
    showfliers=False 
)

dfs = []

for load in os.listdir(dir):
    load_dir = f"{dir}/{load}"
    for type in os.listdir(load_dir):
        file_path = f"{load_dir}/{type}"

        df = pd.read_json(file_path)
        df["compressor"] = df["compressor"].str.upper()
        df = order_df_by_compressor(df, ['ZLIB', 'PPMD', 'GZIP','BZ2','ENTROPY'])

        dfs.append(df)

        grouped = df.groupby(['load','type','compressor','iteration'])

df = pd.concat(dfs, ignore_index=True)
# df = df[df['load']==selected_load]
plots = [
    lambda ax: plotter.generate(
        ax=ax,
        data=df[df['type']=='MEMORY'],
        x_col="time",
        y_col="compressor",
        title=f"MEMORY",
        show_plot=False,
        
    ),
    lambda ax: plotter.generate(
        ax=ax,
        data=df[df['type']=='API'],
        x_col="time",
        y_col="compressor",
        title=f"API",
        show_plot=False,
        show_ylabel=False
    ),
    lambda ax: plotter.generate(
        ax=ax,
        data=df[df['type']=='PROCESS'],
        x_col="time",
        y_col="compressor",
        title=f"PROCESS",
        show_plot=False,
        show_ylabel=False
    ),
]

plotter.generate_multiplots(
    plot_functions=plots,
    nrows=1,
    ncols=3,
    title=f"Response Time Distribution",
    output_image_path=f"{images}/time_boxplots.png"
)

df_filtered = df[df["type"].isin(["MEMORY", "PROCESS", "API"])]

# plotter.generate_multiboxplots(
#     data=df_filtered,
#     x_col="time",
#     y_col="compressor",
#     group_col="type",  # Pode ser 'parameter' ou outro, dependendo do dataset
#     title="Boxplots agrupados por Tipo e Compressor",
#     palette="Set2",
#     output_image_path=f"{images}/grouped_boxplots.png"
# )