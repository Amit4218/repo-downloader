import requests
import os
from typing import Dict, List




def create_folders(path: str, dirs: List) -> None:
    """creates the folders while maintaining the folder structure"""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    for dir in dirs:
        os.makedirs(f"{path}/{dir}", exist_ok=True)



def create_file(raw_repo_link: str, file_name: str, path: str | None = None) -> None:
    """request the raw.githubusercontent api, and create the file"""
    
    result = requests.get(f"{raw_repo_link}/{file_name}")
    result.raise_for_status()
    
    c_type = result.headers.get('Content-Type', '')

    file_path = os.path.join(path, file_name) if path else file_name

    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    # checks if its a streaming files like .mp4, avi, png, pdf etc.
    if "application/octet-stream" or "audio/mpeg" in c_type:
        with open(file_path, "wb") as f:
            f.write(result.content)
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result.text)
            

def filter_results(filter: str, data: List[Dict]) -> Dict:
    """filtes data through the folders for the provider filter"""
    result = {"files": [], "dirs": []}

    for d in data:
        if filter in d["path"].split("/"):
            if d["type"] == "tree":
                result["dirs"].append(d["path"])
            elif d["type"] == "blob":
                result["files"].append(d["path"])

    return result
