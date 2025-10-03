import os
import pandas as pd

results_dir = "../results"
clustering_results = f"{results_dir}/clustering_results"

apps_df = []

for app in os.listdir(clustering_results):

    app_dir = f"{clustering_results}/{app}/RESULTS"

    for load in os.listdir(app_dir): 
        load_data = f"{app_dir}/{load}"

        for type in os.listdir(load_data):
            type_data = f"{load_data}/{type}"
            type_df = pd.read_json(type_data)
            type_df['application'] = app.split('_')[0].upper()
            # Reordenar colocando "application" na frente
            cols = ["application"] + [c for c in type_df.columns if c != "application"]
            type_df = type_df[cols]
            apps_df.append(type_df)
    
df = pd.concat(apps_df)
df.to_csv(f"{results_dir}/all_application_results.csv", index=False)

grouped = (
    df.groupby(["application", "load", "type", "compressor", "iteration"])["time"]
      .mean()
      .reset_index(name="mean_time")
)
grouped.to_csv(f"{results_dir}/application_results_overview.csv", index=False)

        
