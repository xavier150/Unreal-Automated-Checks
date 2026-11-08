import os
from pathlib import Path
from typing import List

from .. import bpl
from .. import check_utils
from .. import config
from .. import project_utils

def run_check_copyright_files() -> None:
    """Check copyright information in source files using pathlib for file system operations."""
    print("- Checking source file copyright...")
    project_default_game_data = project_utils.get_project_default_game_data(config.project_path)
    copyright_notice = project_default_game_data['/Script/EngineSettings.GeneralProjectSettings']['CopyrightNotice']
    locations_to_check: List[Path] = []
    locations_to_check += check_utils.get_project_and_plugin_source_paths()
    invalid_files: List[Path] = []

    for location in locations_to_check:
        location_path = Path(location)
        
        # Use pathlib's rglob to recursively find source files
        for file_path in location_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in ('.h', '.cpp') or file_path.name.endswith('.Build.cs'):
                # Invalid utf-8 bytes are reported by the encoding check, not here
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    first_line = file.readline().strip()
                if copyright_notice not in first_line:
                    warning_message = f"Warning! {file_path.name} in '{file_path}' does not contain the expected copyright line."
                    print(bpl.color_set.yellow(warning_message))
                    print(f"first_line: {first_line} expected: {copyright_notice}")
                    invalid_files.append(file_path)

    if invalid_files:
        ask_open_files(invalid_files)

def ask_open_files(file_paths: List[Path]) -> None:
    print("\nDo you want to open the following files?\n")
    for path in file_paths:
        print(f" - {path}")
    response = input("\nType 'yes' to open them all: ").strip().lower()

    if response in ["yes", "y"]:
        for path in file_paths:
            try:
                os.startfile(path)  # Windows only
                print(f"Opened: {path}")
            except OSError as e:
                print(f"Failed to open {path}: {e}")
    else:
        print("No files were opened.")
