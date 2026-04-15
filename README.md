# Github Repo Downloader (grd)

**grd** is a lightweight yet powerful Python CLI tool that allows you to download specific files or folders from large GitHub repositories—without cloning the entire repo.

---

## Why Repo Downloader?

Have you ever followed a tutorial and needed just a small example from a GitHub repository—only to end up cloning the entire project?

Repo Downloader solves this problem by letting you:

- Download a **single file**
- Download a **specific folder**
- Avoid unnecessary files and save time

---

## Features

- Download individual files from any GitHub repo
- Download specific folders without cloning the full repository
- Simple and intuitive CLI interface
- Supports custom branches
- Cross-platform (Windows, macOS, Linux)

---

## Installation

### 🔧 Prerequisites

- Python 3.10 or higher
- `pip` installed

- **Alternatively you can use `uv`**.

```bash
# if using uv
uv tool install grd-init
```

- **Tip: If you encounter permission issues, try:**

```bash
pip install --user grd-init
```

---

### Linux

```bash
pip3 install grd-init
```

### MacOs

```bash
pip3 install grd-init
```

### Windows

```bash
pip install grd-init
```

## Usage

### Available Commands

| Command   | Description                         |
| --------- | ----------------------------------- |
| `folder`  | Download a folder from a repository |
| `single`  | Download a single file              |
| `example` | Show example usage                  |
| `version` | Display current version             |

### Available Arguments

| Argument   | Short | Description                                   |
| ---------- | ----- | --------------------------------------------- |
| `--name`   | `-n`  | Folder name (required for folder command)     |
| `--link`   | `-l`  | GitHub repository URL (required)              |
| `--path`   | `-p`  | Destination path (default: current directory) |
| `--branch` | `-b`  | Branch name (default: `main`)                 |
| `--file`   | `-f`  | File name (required for single command)       |

## Verify Download

```bash
grd version
# or
grd --help

# Also install auto-completions (recommended)
grd --install-completion
grd --show-completion
```

## Examples

### Download a Folder

```bash
grd folder --name "repo_folder_name" --link "github_repo_url"

grd folder -n "repo_folder_name" -l "github_repo_url" --path "destination_path"

grd folder -n "repo_folder_name" -l "github_repo_url" -p "destination_path" --branch "branch_name"
```

### Download a Single File

```bash
grd single --file "file_name" --link "github_repo_url"

grd single -f "file_name" -l "github_repo_url"
```

### Example Command Help

```bash
grd example
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
