import sys

import requests


def create_file(repo_link: str, file_name: str, path: str | None = None) -> None:
    """
    sends a request to the raw.githubusercontent api,<br>
    creates the file and dumps the text in the file.

    Args:
        repo_link (str): modified github repo link
        file_name (str): name of the file (extracted from the url)
        path (str | None, optional): where the file should be created. Defaults to current dir.
    """

    url = repo_link.replace("github", "raw.githubusercontent")
    result = requests.get(url)
    file_path = f"{path}/{file_name}" if path else file_name

    with open(file=file_path, mode="w", encoding="utf-8") as f:
        f.write(result.text)


def main():
    if not len(sys.argv) > 0:
        print("No github repo link provided")
        return

    github_repo_link = sys.argv[1].replace("/blob", "")

    # check if its file
    isFile = github_repo_link.split(".")

    if len(isFile) > 0:
        file_name = github_repo_link.split("/")[-1]
        create_file(github_repo_link, file_name)


if __name__ == "__main__":
    main()
