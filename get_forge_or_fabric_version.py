import os
import pathlib
import shutil
import json

def get_forge_or_fabric_version_from_manifest(path):
    with open(path, encoding="UTF-8") as f:
        data = json.load(f)
        modloaders = data["minecraft"]["modLoaders"]
        minecraft_version = data["minecraft"]["version"]
        
        for modloader in modloaders:
            if modloader.get("primary") == True:
                loader_id = modloader["id"].lower()

                # 1. Fabric Check
                if "fabric" in loader_id:
                    return "fabric", minecraft_version

                # 2. NeoForge Check (Wichtig: Vor Forge prüfen, da "forge" in "neoforge" enthalten ist)
                if "neoforge" in loader_id:
                    # Schneidet "neoforge-" ab (9 Zeichen)
                    return "neoforge", minecraft_version + "-" + modloader["id"][9:]

                # 3. Forge Check
                if "forge" in loader_id:
                    # Schneidet "forge-" ab (6 Zeichen)
                    return "forge", minecraft_version + "-" + modloader["id"][6:]

    return None, None