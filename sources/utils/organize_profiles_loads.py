import os
profile_dir = "../../profiles"

for application in os.listdir(profile_dir):
    app_dir = f"{profile_dir}/{application}"

    for profile in os.listdir(app_dir):
        profile_path = f"{app_dir}/{profile}"
        if os.path.isdir(profile_path):
            continue

        if application == 'bert':
            load = profile.split('_')[0]
            load_dir = f"{app_dir}/{load}"
            os.makedirs(load_dir, exist_ok=True)
            os.rename(profile_path, f"{load_dir}/{profile}")
            print(f"Movido arquivo BERT {profile} para o load {load}")
        elif application == 'chess':
            load = profile.split('_')[0].upper()
            load_dir = f"{app_dir}/{load}"
            os.makedirs(load_dir, exist_ok=True)
            os.rename(profile_path, f"{load_dir}/{profile}")
            splits = profile.split('_')
            splits[0] = splits[0].upper()
            new_name = "_".join(splits)
            os.rename(f"{load_dir}/{profile}", f"{load_dir}/{new_name}")
            print(f"Movido arquivo CHESS {profile} para o load {load}")
        elif application == 'voice':
            load = profile.split('_')[0]+'-'+profile.split('_')[1]
            load_dir = f"{app_dir}/{load}"
            os.makedirs(load_dir, exist_ok=True)
            os.rename(profile_path, f"{load_dir}/{profile}")
            new_name = profile.replace("_", "-", 1)
            os.rename(f"{load_dir}/{profile}", f"{load_dir}/{new_name}")
            print(f"Movido arquivo VOICE {profile} para o load {load}") 
        elif application == 'yatserver':
            load = profile.split('_')[0]
            load_dir = f"{app_dir}/{load}"
            os.makedirs(load_dir, exist_ok=True)
            os.rename(profile_path, f"{load_dir}/{profile}")
            print(f"Movido arquivo YATSERVER {profile} para o load {load}")
            
