HELP = """
Here are the example usages:

## Command: folder

### Available shorthands:
- **--name** -> `-n` (folder name required)
- **--link** -> `-l` (repo URL required)
- **--path** -> `-p` (optional, default: current directory)
- **--branch** -> `-b` (default: main)
- **--file** -> `-f` (file name to be searched (only for single))

### Examples
```bash
grd folder --name "repo_folder_name" -link "github_repo_url"
grd folder -n "repo_folder_name" -l "github_repo_url" --path "where_to_create"
grd folder -n "repo_folder_name" -l "github_repo_url" --p "where_to_create" --branch "branch_name"
```

## Command: single

### Examples
```bash
grd single --file "file_name" --link "github_repo_url"
grd single -f "file_name" -l "github_repo_url"
```
"""
