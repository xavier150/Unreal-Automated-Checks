from pathlib import Path
from typing import List

from . import bpl
from . import config
from . import project_utils

def run_check_build_icon() -> None:
    print("- Checking build icon...")

    icon_not_found: List[Path] = []

    def check_icon(icon_filepath: Path) -> bool:
        # Check if the icon file exists
        if icon_filepath.is_file():
            return True
        else:
            icon_not_found.append(icon_filepath)
            return False

    project_path = project_utils.get_project_path(config.project_path)
    windows_icon_relative_path: Path = project_path / "Build" / "Windows" / "Application.ico"
    linux_icon_relative_path: Path = project_path / "Build" / "Linux" / "Application.png"

    # Check icons
    check_icon(windows_icon_relative_path)
    check_icon(linux_icon_relative_path)

    if len(icon_not_found) > 0:
        for icon in icon_not_found:
            print(bpl.color_set.red(f"The icon {icon} was not found!"))

        text: str = f'You can find the icons at the path: {config.splash_and_icons_path}\n'
        text += 'In Unreal Editor, go to Edit > Project Settings > Platforms > Windows/Linux and set the icon paths accordingly.'
        print(text)