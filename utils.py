import os
from typing import Dict, List, Literal

import requests

URL_TYPE = Literal["raw", "api"]


def get_modified_url(repo_link: str, type: URL_TYPE, branch: str = "main") -> str:
    """returns an structured api url based on the type and branch passed"""
    parsed_repo_link = repo_link.replace("https://github.com/", "").split("/")
    owner, repo = parsed_repo_link[0], parsed_repo_link[1]

    match type:
        case "api":
            return f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        case "raw":
            return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}"


def get_repo_structure(url: str):
    """Gets the repo structure from the github public api"""
    res = requests.get(url)
    data = res.json()

    if "tree" in data:
        return data["tree"]
    return []


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


def create_file(raw_repo_link: str, file_name: str, path: str | None = None) -> None:
    """
    sends a request to the raw.githubusercontent api,<br>
    creates the file and dumps the text in the file.

    Args:
        repo_link (str): modified github repo link
        file_name (str): name of the file (extracted from the url)
        path (str | None, optional): where the file should be created. Defaults to current dir.
    """
    result = requests.get(f"{raw_repo_link}/{file_name}")
    file_path = f"{path}/{file_name}" if path else file_name

    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    with open(file=file_path, mode="w", encoding="utf-8") as f:
        f.write(result.text)


def create_folders(path: str, dirs: List) -> None:
    """creates the folders while maintaining the folder structure"""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    for dir in dirs:
        os.makedirs(f"{path}/{dir}", exist_ok=True)
