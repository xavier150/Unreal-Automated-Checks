import os
from pathlib import Path
from typing import List

from .. import base_check
from .. import bpl
from .. import check_utils


class EncodingFilesCheck(base_check.BaseCheck):
    name = "File encoding"

    def run_check(self) -> None:
        """Check encoding of source files using pathlib for file system operations."""
        print("- Checking source file encoding...")
        locations_to_check: List[Path] = []
        locations_to_check += check_utils.get_project_and_plugin_source_paths()
        invalid_encoding_files: List[Path] = []

        for location in locations_to_check:
            location_path = Path(location)

            # Use pathlib's rglob to recursively find source files
            for file_path in location_path.rglob('*'):
                if file_path.is_file() and file_path.suffix in ('.h', '.cpp') or file_path.name.endswith('.Build.cs'):
                    raw_bytes = file_path.read_bytes()
                    try:
                        raw_bytes.decode('utf-8')
                    except UnicodeDecodeError as e:
                        byte_position = e.start
                        line_number = raw_bytes.count(b'\n', 0, byte_position) + 1
                        # rfind returns -1 when there is no newline, which yields byte_position
                        last_newline = raw_bytes.rfind(b'\n', 0, byte_position)
                        char_index_in_line = byte_position - last_newline - 1

                        warning_message = (
                            f"utf-8 Encoding error in file:\n"
                            f" - Path     : {file_path}\n"
                            f" - Byte pos : {byte_position}\n"
                            f" - Line     : {line_number}, Char in line: {char_index_in_line}\n"
                            f" - Offending byte: 0x{raw_bytes[byte_position]:02x}"
                        )
                        print(bpl.color_set.yellow(warning_message))
                        invalid_encoding_files.append(file_path)

        if invalid_encoding_files:
            ask_open_files(invalid_encoding_files)


def run_check_encoding_files() -> None:
    EncodingFilesCheck().run_check()

def ask_open_files(file_paths: List[Path]) -> None:
    """Ask user if they want to open the files with encoding issues."""
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
