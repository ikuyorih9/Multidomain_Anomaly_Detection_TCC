import pandas as pd
import os
from utils.boxplot import BoxplotPlot

df = pd.read_csv('../results/all_application_results.csv')
# Criar instância do BoxplotPlot
plotter = BoxplotPlot(
    title="Comparação repetições",
    ylabel="Tempo",
    xlabel="Conjunto de repetições",
    palette="Set2"
)

variation = []
for (app, load, t, comp), group in df.groupby(["application", "load", "type", "compressor"]):
    subset_10 = group[group["repetition"] < 10].copy()
    subset_30 = group[group["repetition"] < 30].copy()

    # Adiciona uma coluna nova identificando qual subset é
    subset_10["subset"] = "0-10 repetições"
    subset_30["subset"] = "0-30 repetições"

    # Junta os dados
    combined = pd.concat([subset_10, subset_30], ignore_index=True)

    # Agora gera boxplot com seu wrapper
    title = f"{app} | {load} | {t} | {comp}"

    # plotter.generate(
    #     data=combined,
    #     x_col="subset",    # eixo x -> conjunto de repetições
    #     y_col="time",      # eixo y -> tempo
    #     title=title,
    #     show_plot=True    # pode desligar se quiser só salvar as imagens
    # )


    # Mostrar estatísticas
    mean = []
    std = []
    # print(f"\n=== {title} ===")
    for subset_name, subdf in combined.groupby("subset"):
        mean.append(subdf['time'].mean())
        std.append(subdf['time'].std())
        # print(f"{subset_name}: média={subdf['time'].mean():.4f}, desvio={subdf['time'].std():.4f}")

    mean_var = (mean[0] - mean[1])/mean[1]
    std_var = (std[0] - std[1])/std[1]
    # print(f"MEAN: {mean_var*100} --- STD: {std_var*100}")

    variation.append({
        'application': app,
        'load':load,
        'type': t,
        'compressor': comp,
        'std(%)': std_var,
        'mean(%)':mean_var
    })

vdf = pd.DataFrame(variation)
print(vdf)