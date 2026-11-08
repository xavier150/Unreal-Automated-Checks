from pathlib import Path
from typing import List

from . import bpl
from . import config
from . import project_utils


def check_files(icon_filepath: Path) -> List[str]:
    """Check build files for proper line endings using pathlib for file system operations."""
    issues: List[str] = []

    base_dir = icon_filepath.parent

    # Use pathlib's rglob to recursively find script files
    for filepath in base_dir.rglob('*'):
        if not filepath.is_file():
            continue
            
        filename = filepath.name

        # Check linux .sh files
        if filename.endswith(".sh"):
            try:
                content = filepath.read_bytes()
                if b'\r\n' in content:
                    issues.append(f"{filepath} contains CRLF (should be LF for .sh)")
            except OSError as e:
                issues.append(f"Could not check {filepath}: {e}")

        # Check Windows .bat files
        elif filename.endswith(".bat"):
            try:
                content = filepath.read_bytes()
                if b'\n' in content and b'\r\n' not in content:
                    issues.append(f"{filepath} contains LF only (should be CRLF for .bat)")
            except OSError as e:
                issues.append(f"Could not check {filepath}: {e}")

    return issues


def run_check() -> None:
    print("- Checking additional build files...")

    issues: List[str] = []

    project_path = project_utils.get_project_path(config.project_path)
    windows_relative_path = project_path / "AdditionalBuildFiles" / "Windows" / "Application.ico"
    linux_relative_path = project_path / "AdditionalBuildFiles" / "Linux" / "Application.png"

    # Check icons
    issues += check_files(windows_relative_path)
    issues += check_files(linux_relative_path)

    if len(issues) > 0:
        for issue in issues:
            print(bpl.color_set.red(f"Error: {issue}"))