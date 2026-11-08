from typing import List

from .. import bpl
from .. import config
from .. import project_utils
from . import check_build_additional_files_utils


def run_check() -> None:
    print("- Checking additional build files...")

    issues: List[str] = []

    project_path = project_utils.get_project_path(config.project_path)
    windows_relative_path = project_path / "AdditionalBuildFiles" / "Windows" / "Application.ico"
    linux_relative_path = project_path / "AdditionalBuildFiles" / "Linux" / "Application.png"

    # Check icons
    issues += check_build_additional_files_utils.check_files(windows_relative_path)
    issues += check_build_additional_files_utils.check_files(linux_relative_path)

    if len(issues) > 0:
        for issue in issues:
            print(bpl.color_set.red(f"Error: {issue}"))