from typing import Literal

import requests

URL_TYPE = Literal["raw", "api"]


def get_modified_url(repo_link: str, type: URL_TYPE, branch: str = "main") -> str:
    """returns an structured api url based on the type and branch passed"""
    
    if not repo_link or "github.com" not in repo_link:
        raise Exception("[bold red]Error:[/] Please provide a valid GitHub repository URL.")
    
    parts = repo_link.rstrip("/").replace("https://github.com/", "").split("/")
    if len(parts) < 2:
        raise Exception("[bold red]Error:[/] Invalid repo format. Use 'owner/repo' or the full URL.")
    
    parsed_repo_link = repo_link.replace("https://github.com/", "").split("/")
    owner, repo = parsed_repo_link[0], parsed_repo_link[1]

    match type:
        case "api":
            return f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        case "raw":
            return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}"


def get_repo_structure(url: str):
    """Gets the repo structure from the github public api"""
    try:
        res = requests.get(url)
        data = res.json()

        if "tree" in data:
            return data["tree"]
        return []
    
    except requests.exceptions.HTTPError as e:
        if res.status_code == 404:
            raise Exception("[bold red]Error:[/] Repository or branch not found. Check your URL/Branch.")
        elif res.status_code == 403:
            raise Exception("[bold red]Error:[/] Rate limit exceeded or access denied.")
        else:
            raise Exception(f"[bold red]HTTP Error:[/] {e}")
    except requests.exceptions.ConnectionError:
        raise Exception("[bold red]Error:[/] Could not connect to the internet.")
 


