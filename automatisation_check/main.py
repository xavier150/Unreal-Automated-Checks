from . import bpl
from . import check_asset_naming
from . import check_build_additional_files
from . import check_build_icon
from . import check_copyright_info
from . import check_deprecated_cpp
from . import check_empty_folders
from . import check_encoding_files
from . import check_project_info
from . import check_project_version

def main() -> None:
    bpl.advprint.print_simple_title("Automatisation checks")
    bpl.console_utils.clear_console()

    checks = (
        (
            "Project version",
            check_project_version.check_project_version.run_check_project_version,
        ),
        ("Build icon", check_build_icon.check_build_icon.run_check_build_icon),
        (
            "Additional build files",
            check_build_additional_files.check_build_additional_files.run_check,
        ),
        (
            "Empty folders",
            check_empty_folders.check_empty_folders.run_check_empty_folders,
        ),
        (
            "File encoding",
            check_encoding_files.check_encoding_files.run_check_encoding_files,
        ),
        (
            "Deprecated C++",
            check_deprecated_cpp.check_deprecated_cpp.run_check_deprecated_cpp,
        ),
        (
            "Copyright",
            check_copyright_info.check_copyright_info.run_check_copyright_files,
        ),
        (
            "Asset naming",
            check_asset_naming.check_asset_naming.run_check_asset_naming_files,
        ),
        (
            "Project info",
            check_project_info.check_project_info.run_check_project_info,
        ),
    )

    print("Choose a check:")
    print("[1] ALL")
    for choice, (name, _) in enumerate(checks, start=2):
        print(f"[{choice}] Check {name}")

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
    for _, run_check in selected_checks:
        run_check()
