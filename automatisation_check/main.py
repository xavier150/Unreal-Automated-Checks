from typing import Tuple

from . import base_check
from . import bpl
from . import check_asset_naming
from . import check_build_additional_files
from . import check_build_icon
from . import check_copyright_info
from . import check_deprecated_cpp
from . import check_deprecated_bp
from . import check_empty_folders
from . import check_encoding_files
from . import check_project_info
from . import check_project_version

def main() -> None:
    bpl.advprint.print_simple_title("Automatisation checks")
    bpl.console_utils.clear_console()

    checks: Tuple[base_check.BaseCheck, ...] = (
        check_project_version.check_project_version.ProjectVersionCheck(),
        check_build_icon.check_build_icon.BuildIconCheck(),
        check_build_additional_files.check_build_additional_files.BuildAdditionalFilesCheck(),
        check_empty_folders.check_empty_folders.EmptyFoldersCheck(),
        check_encoding_files.check_encoding_files.EncodingFilesCheck(),
        check_deprecated_cpp.check_deprecated_cpp.DeprecatedCppCheck(),
        check_deprecated_bp.check_deprecated_bp.DeprecatedBpCheck(),
        check_copyright_info.check_copyright_info.CopyrightInfoCheck(),
        check_asset_naming.check_asset_naming.AssetNamingCheck(),
        check_project_info.check_project_info.ProjectInfoCheck(),

    )

    print("Choose a check:")
    print("[1] ALL")
    for choice, check in enumerate(checks, start=2):
        print(f"[{choice}] Check {check.name}")

    while True:
        selection = input("Choice: ").strip()
        if selection == "1":
            selected_checks = checks
            break

        try:
            check_index = int(selection) - 2
        except ValueError:
            check_index = -1

        if 0 <= check_index < len(checks):
            selected_checks = (checks[check_index],)
            break

        print("Invalid choice. Please select one of the listed numbers.")

    print("Start checks...")
    for check in selected_checks:
        check.run_check()
