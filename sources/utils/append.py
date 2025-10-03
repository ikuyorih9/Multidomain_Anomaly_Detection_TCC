"""
This script merges JSON result files from two input directories.
For each pair of JSON files (with the same name and subfolder structure),
it loads the data, concatenates the records using pandas, removes duplicate
entries based on a composite key ("load", "type", "compressor", "repetition"),
and writes the cleaned JSON output to a specified directory.

Usage:
    python merge_json_results.py --dir1 <path_to_first_input_dir> \
                                 --dir2 <path_to_second_input_dir> \
                                 --out <path_to_output_dir>
"""

import os
import json
import pandas as pd
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Merge JSON result files removing duplicates.")
parser.add_argument("--dir1", required=True, help="Path to the first input directory")
parser.add_argument("--dir2", required=True, help="Path to the second input directory")
parser.add_argument("--out", required=True, help="Path to the output directory")
args = parser.parse_args()

# Directories from CLI arguments
dir1 = args.dir1
dir2 = args.dir2
dir_out = args.out
os.makedirs(dir_out, exist_ok=True)

# Iterate through subdirectories (e.g., "load")
for load in os.listdir(dir1):
    load_path1 = os.path.join(dir1, load)
    load_path2 = os.path.join(dir2, load)
    load_out = os.path.join(dir_out, load)
    
    # Ensure output subdir exists
    os.makedirs(load_out, exist_ok=True)

    # Iterate through JSON files in current folder
    for fname in os.listdir(load_path1):
        file1 = os.path.join(load_path1, fname)
        file2 = os.path.join(load_path2, fname)
        file_out = os.path.join(load_out, fname)

        # Load JSON contents
        with open(file1, "r", encoding="utf-8") as f1:
            data1 = json.load(f1)
        with open(file2, "r", encoding="utf-8") as f2:
            data2 = json.load(f2)

        # Ensure the data is a list of dicts
        if isinstance(data1, dict):
            data1 = [data1]
        if isinstance(data2, dict):
            data2 = [data2]

        # Create DataFrames
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)

        # Concatenate and remove duplicates by composite key
        df = pd.concat([df1, df2], ignore_index=True)
        df = df.drop_duplicates(subset=["load", "type", "compressor", "repetition"])

        # Convert back to list of dicts
        data_out = df.to_dict(orient="records")

        # Write merged JSON to output directory
        with open(file_out, "w", encoding="utf-8") as f_out:
            json.dump(data_out, f_out, indent=4, ensure_ascii=False)

        print(f"✅ Merged file saved: {file_out}")
