from pathlib import Path
from typing import List

from . import bpl
from . import check_utils
from . import config

def run_check_empty_folders() -> None:
    print("- Checks empty folders...")
    locations_to_check: List[Path] = []
    locations_to_check += check_utils.get_project_and_plugin_content_paths()
    locations_to_check += check_utils.get_project_and_plugin_source_paths()
    locations_to_check += check_utils.get_project_empty_path_check()
    excluded_dirs = config.exclude_content_check_directory
    empty_directories: List[Path] = []

    for location in locations_to_check:
        location_path = Path(location)
        
        # Depth-first traversal with pathlib, optimized for performance
        def is_excluded(path: Path) -> bool:
            return any(excluded in path.parts for excluded in excluded_dirs)
        
        # Process directories from deepest to shallowest for efficiency
        all_dirs = [d for d in location_path.rglob('*') if d.is_dir() and not is_excluded(d)]
        
        # Sort by depth (deepest first) to process leaf directories first
        all_dirs.sort(key=lambda p: len(p.parts), reverse=True)
        
        for dir_path in all_dirs:
            # Skip root location itself
            if dir_path.resolve() == location_path.resolve():
                continue
                
            # Check if directory is empty
            try:
                # Use next() with StopIteration handling - more efficient than any()
                next(dir_path.iterdir())
            except StopIteration:
                # Directory is empty
                print_empty_directory_warning(dir_path)
                empty_directories.append(dir_path)
            except OSError as e:
                print(f"Error accessing {dir_path}: {e}")

    if empty_directories:
        ask_remove(empty_directories)

def ask_remove(empty_directories: List[Path]) -> None:
    print("\nDo you want to remove the following empty directories?\n")
    for path in empty_directories:
        print(f" - {path}")
    response = input("\nType 'yes' to confirm deletion: ").strip().lower()

    if response in ["yes", "y"]:
        for path in empty_directories:
            try:
                path.rmdir()
                print(f"Deleted directory: {path}")
            except OSError as e:
                print(f"Error deleting {path}: {e}")
    else:
        print("\nNo directories were deleted.")

def print_empty_directory_warning(directory_path: Path) -> None:
    warning_message = f"Warning: Directory '{directory_path}' is empty."
    print(bpl.color_set.yellow(warning_message))
