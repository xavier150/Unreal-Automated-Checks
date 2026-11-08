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

    print("Start checks...")
    check_project_version.run_check_project_version()
    check_build_icon.run_check_build_icon()
    check_build_additional_files.run_check()
    check_empty_folders.run_check_empty_folders()
    check_encoding_files.run_check_encoding_files()
    check_deprecated_cpp.run_check_deprecated_cpp()
    check_copyright_info.run_check_copyright_files()
    check_asset_naming.run_check_asset_naming_files()
    check_project_info.run_check_project_info()
