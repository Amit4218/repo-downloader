from typing import Literal

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


