import os
from shutil import move
import json
from time import sleep
import requests

from download_file import download


def download_manifest_mods(path):
    with open(path, encoding="UTF-8") as f:
        data = json.load(f)
        print("Starting download of modpack manifest server mods...")
        for mod in data['files']:
            try:
                mod_id = mod['projectID']
                file_id = mod['fileID']
            except:
                print("Error parsing mod download IDs")
            if mod['required'] == False:
                print(f"Detected optional server mod {mod_id}. Skipping download.")
                continue
            if mod_id and file_id:
                # Try and get Mod Download file from our CF API
                try:
                    response = requests.get(f"https://api.hypesrv.net/v2/modpack/fileUrl/{mod_id}/{file_id}", timeout=60, headers={"Authorization": "Bearer "+os.environ['HS_MOD_API_KEY']}).json()["data"]
                    print(f"Downloading {response["name"]} ...")
                    download(response["download_url"])
                except:
                    print(f"Error downloading mod {mod_id}.")

        sleep(1)
        print("Finished downloading all server mods from modpack manifest.")