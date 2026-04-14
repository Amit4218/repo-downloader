#!/usr/bin/env python3

import time
from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from typer import Option, Typer

from grd.examples import HELP
from grd.utils import (
    create_file,
    create_folders,
    filter_results,
    get_modified_url,
    get_repo_structure,
)

app = Typer(
    help="A simple command line tool, that helps with downloading subfolder and files from github repos",
    rich_markup_mode="rich",
)

console = Console()


@app.command(help="Download a subfolder from the repo")
def folder(
    name: str = Option(None, "--name", "-n", help="Name of the folder"),
    branch: str = Option("main", "--branch", "-b", help="specify a branch"),
    url: str = Option(None, "--link", "-l", help="Link of the github repo"),
    path: Optional[str] = Option(
        None, "--path", "-p", help="Where the file should be created"
    ),
):
    with console.status("Working on it, please wait..."):
        # get the modified url for the api.github
        modified_url = get_modified_url(repo_link=url, type="api", branch=branch)

        # get the full structure of the project
        repo_structure = get_repo_structure(url=modified_url)

        # filter the repo for the specific folder name
        results = filter_results(filter=name, data=repo_structure)

        # make dirs
        if path:
            create_folders(path=path, dirs=results["dirs"])

        # get the modified url for raw.githubusercontent
        raw_url = get_modified_url(repo_link=url, type="raw", branch=branch)

        for file in results["files"]:
            create_file(raw_repo_link=raw_url, file_name=file, path=path)
            time.sleep(0.2)


@app.command(help="Download a single file from the repo")
def single(
    file_name: str = Option(None, "--file", "-f", help="Name of the file"),
    url: str = Option(None, "--link", "-l", help="Link of the github repo"),
):
    with console.status("Creating the file"):
        modified_url = get_modified_url(repo_link=url, type="api")
        repo_structure = get_repo_structure(modified_url)

        for files in repo_structure:
            if file_name in files["path"].split("/") and files["type"] == "blob":
                file = files["path"]
                raw_url = get_modified_url(repo_link=url, type="raw")
                create_file(raw_repo_link=raw_url, file_name=file)
                return
        print("No file found! please check your spelling")


@app.command(help="prints the version of the application")
def version():
    print("version: 0.1.0")


@app.command(help="prints example usages for the command")
def example():
    console.print(Markdown(HELP))


if __name__ == "__main__":
    app()
