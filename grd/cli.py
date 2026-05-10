import time 
import sys
from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from typer import Option, Typer

from grd.examples import HELP
from grd.file_operations import create_file, create_folders, filter_results
from grd.utils import get_modified_url,get_repo_structure

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
    try: 
        with console.status("Working on it, please wait..."):
            # get the modified url for the api.github
            modified_url = get_modified_url(repo_link=url, type="api", branch=branch)

            # get the full structure of the project
            repo_structure = get_repo_structure(url=modified_url)

            # filter the repo for the specific folder name
            results = filter_results(filter=name, data=repo_structure)
            
            if not results["files"] and not results["dirs"]:
                raise Exception(f"[yellow]No files or folders found matching: {name}[/]")

            # make dirs
            if path:
                create_folders(path=path, dirs=results["dirs"])

            # get the modified url for raw.githubusercontent
            raw_url = get_modified_url(repo_link=url, type="raw", branch=branch)

            for file in results["files"]:
                create_file(raw_repo_link=raw_url, file_name=file, path=path)
                time.sleep(0.2)
    
    except Exception as err:
        console.print(f"[bold red]An unexpected error occurred:[/] {err}")
        sys.exit(1)


@app.command(help="Download a single file from the repo")
def single(
    file_name: str = Option(None, "--file", "-f", help="Name of the file"),
    url: str = Option(None, "--link", "-l", help="Link of the github repo"),
):
    try:
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
    except Exception as err:
        console.print(f"[bold red]An unexpected error occurred:[/] {err}")
        sys.exit(1)


@app.command(help="prints the version of the application")
def version():
    print("version: 0.1.3")


@app.command(help="prints example usages for the command")
def example():
    console.print(Markdown(HELP))


if __name__ == "__main__":
    app()
