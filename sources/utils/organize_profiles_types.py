import os
profile_dir = "../../profiles"

for application in os.listdir(profile_dir):
    app_dir = f"{profile_dir}/{application}"

    for load in os.listdir(app_dir):
        load_dir = f"{app_dir}/{load}"
        if not os.path.isdir(load_dir):
            continue
        for profile in os.listdir(load_dir):
            profile_path = f"{load_dir}/{profile}"
            if os.path.isdir(profile_path):
                continue

            if application in ['yatserver', 'chess']:
                type = profile.split("_")[2]
            else:
                type = profile.split("_")[3]

            if type in ['py', 'exe']:
                continue
            
            profile = profile.replace(type, type.upper())
            type = type.upper()

            type_dir = f"{load_dir}/{type}"
            os.makedirs(type_dir, exist_ok=True)
            os.rename(profile_path, f"{type_dir}/{profile}")
            print(f"Movido de {profile_path} para {type_dir}/{profile}")
            