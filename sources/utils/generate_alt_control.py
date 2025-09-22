import os

base_dir = f"../../profiles"
for application in os.listdir(base_dir):
    app_dir = f"{base_dir}/{application}"
    if not os.path.isdir(app_dir):
        continue
    for load in os.listdir(app_dir):
        load_dir = f"{app_dir}/{load}"
        if not os.path.isdir(load_dir):
            continue
        control_dir = f"{load_dir}/CONTROL"
        controlv2_dir = f"{load_dir}/ALTCONTROL"
    
        os.makedirs(controlv2_dir, exist_ok=True)

        for fname in os.listdir(control_dir):
            fpath = os.path.join(control_dir, fname)

            if os.path.isfile(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    linhas = f.readlines()

                linhas = [linha.strip() for linha in linhas if linha.strip()]

                metade = len(linhas) // 2

                metade_linhas = linhas[:metade]

                fname_new = fname.replace("CONTROL", "ALTCONTROL", 1)
                fpath_new = os.path.join(controlv2_dir, fname_new)

                # salva preservando as linhas completas
                with open(fpath_new, "w", encoding="utf-8") as f:
                    f.write("\n".join(metade_linhas) + "\n")

                print(f"{fname} -> {fname_new} ({len(metade_linhas)} linhas salvas)")