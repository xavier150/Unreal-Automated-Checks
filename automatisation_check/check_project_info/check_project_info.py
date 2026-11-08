import os
from pathlib import Path
from typing import List, Tuple

from .. import config
from .. import plugin_utils


# Root of your Unreal project
PROJECT_ROOT_PATH: Path = config.project_path.parent

# Folders to scan
TARGET_FOLDERS: List[str] = ["Source", "Plugins"]

# File extensions to count
VALID_EXTENSIONS: List[str] = [".h", ".cpp", ".cs"]

# Folders to ignore
IGNORED_FOLDERS: List[str] = ["Intermediate", "Binaries", "DerivedDataCache", ".svn", ".git", ".vs", "Saved", "Build", "ThirdParty"]

EXCLUDED_PLUGIN_PATHS: List[Path] = plugin_utils.get_excluded_plugin_root_path_list(config.project_path)

def should_ignore(path: Path) -> bool:
    for ignored in IGNORED_FOLDERS:
        if ignored.lower() in str(path).lower():
            return True
        
    for excluded_plugin in EXCLUDED_PLUGIN_PATHS:
        if excluded_plugin in path.parents or excluded_plugin == path:
            return True
    return False

def check_code_info() -> None:
    # Count the number of lines of code in the Source folder



    total_lines = 0
    total_non_empty_lines = 0
    file_count = 0
    total_size_bytes = 0


    
    ## Please update to PATHLIB
    for folder in TARGET_FOLDERS:
        folder_path = PROJECT_ROOT_PATH / folder

        if not folder_path.exists():
            continue

        for root, _, files in os.walk(folder_path):
            root_path = Path(root)
            if should_ignore(root_path):
                continue

            for file in files:
                if any(file.endswith(ext) for ext in VALID_EXTENSIONS):
                    file_path = root_path / file

                    try:
                        file_size = file_path.stat().st_size
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            lines = f.readlines()

                            total_lines += len(lines)
                            total_non_empty_lines += sum(1 for l in lines if l.strip())

                            file_count += 1
                            total_size_bytes += file_size

                    except OSError as e:
                        print(f"Error reading {file_path}: {e}")


    print("===== Unreal Code Stats =====")
    print(f"Files counted: {file_count}")
    print(f"Total lines: {total_lines}")
    print(f"Non-empty lines: {total_non_empty_lines}")
    total_size_mb = total_size_bytes / (1024 * 1024)
    print(f"Total weight: {total_size_mb:.2f} MB ({total_size_bytes:>12,} bytes)")


def get_largest_code_files(limit: int = 10) -> None:
    """Display the largest code files in the Source and Plugins folders"""


    files_with_sizes: List[Tuple[Path, int]] = []

    for folder in TARGET_FOLDERS:
        folder_path = PROJECT_ROOT_PATH / folder

        if not folder_path.exists():
            continue

        for root, _, files in os.walk(folder_path):
            root_path = Path(root)
            if should_ignore(root_path):
                continue

            for file in files:
                # Only include valid code file extensions
                if any(file.endswith(ext) for ext in VALID_EXTENSIONS):
                    file_path = root_path / file
                    try:
                        file_size = file_path.stat().st_size
                        files_with_sizes.append((file_path, file_size))
                    except OSError as e:
                        print(f"Error reading {file_path}: {e}")

    # Sort by size in descending order and take the top 'limit'
    largest_files = sorted(files_with_sizes, key=lambda x: x[1], reverse=True)[:limit]

    print(f"\n===== Top {limit} Largest Code Files =====")
    for idx, (file_path, size) in enumerate(largest_files, 1):
        size_mb = size / (1024 * 1024)
        relative_path = file_path.relative_to(PROJECT_ROOT_PATH)
        print(f"{idx:2d}. {str(relative_path):<60} {size_mb:>10.2f} MB ({size:>12,} bytes)")


def run_check_project_info() -> None:

    print("- Checking project information...")
    check_code_info()
    get_largest_code_files()
