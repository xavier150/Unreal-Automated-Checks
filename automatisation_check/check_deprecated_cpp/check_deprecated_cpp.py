"""Report Unreal deprecation markers in project and non-excluded plugin sources.

This is a text search in .h and .cpp files, including comments and strings.
It finds UE_DEPRECATED, DeprecatedFunction and DeprecatedProperty markers,
not unmarked calls to deprecated APIs. Plugin exclusions come from config.
"""

import re

from .. import base_check
from .. import bpl
from .. import check_utils
from .. import config
from .. import plugin_utils


class DeprecatedCppCheck(base_check.BaseCheck):
    name = "Deprecated C++"

    def run_check(self) -> None:
        """Print matching source lines with their paths and one-based line numbers."""
        print("- Checking C++ deprecation markers...")
        marker_pattern = re.compile(
            r"\b(?:UE_DEPRECATED|DeprecatedFunction|DeprecatedProperty)\b"
        )
        excluded_roots = [
            path.resolve()
            for path in plugin_utils.get_excluded_plugin_root_path_list(config.project_path)
        ]
        match_count = 0
        error_count = 0

        for location in check_utils.get_project_and_plugin_source_paths():
            for file_path in sorted(location.rglob("*")):
                if not file_path.is_file() or file_path.suffix.lower() not in (".h", ".cpp"):
                    continue
                resolved_path = file_path.resolve()
                if any(
                    resolved_path == root or root in resolved_path.parents
                    for root in excluded_roots
                ):
                    continue

                try:
                    # Encoding issues are reported by the separate encoding check.
                    with file_path.open("r", encoding="utf-8-sig", errors="replace") as file:
                        for line_number, line in enumerate(file, start=1):
                            if marker_pattern.search(line):
                                match_count += 1
                                print(
                                    bpl.color_set.yellow(
                                        f"Warning! C++ deprecation marker at "
                                        f"{file_path}:{line_number}: {line.strip()}"
                                    )
                                )
                except OSError as error:
                    error_count += 1
                    print(f"Error while reading file {file_path}: {error}")

        if match_count:
            print(f"Found C++ deprecation markers on {match_count} source line(s).")
        elif not error_count:
            print("No C++ deprecation markers found.")
        if error_count:
            print(f"C++ deprecation check incomplete: {error_count} file(s) could not be read.")


def run_check_deprecated_cpp() -> None:
    DeprecatedCppCheck().run_check()
