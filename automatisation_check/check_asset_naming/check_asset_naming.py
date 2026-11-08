from pathlib import Path
import subprocess

from .. import base_check
from .. import check_utils
from .. import config


class AssetNamingCheck(base_check.BaseCheck):
    name = "Asset naming"

    def run_check(self) -> None:
        """Check asset naming using pathlib for file system operations."""
        # @TODO Need found a way to check the assets from outside the editor...
        return

        print("- Checking editor asset naming...")

        script_path = Path(r"M:\MMVS_ProjectFiles\Other\MMVS_AutomatisationCheck\automatisation_check\test_script.py")

        subprocess.run([
            config.unreal_path,
            config.project_path,
            f'-ExecutePythonScript={script_path}'
        ])

        return
        locations_to_check = []
        locations_to_check += check_utils.get_project_and_plugin_content_paths()
        invalid_files = []

        for location in locations_to_check:
            location_path = Path(location)

            # Use pathlib's rglob to recursively find asset files
            for file_path in location_path.rglob("*.uasset"):
                # Asset processing logic would go here
                pass


def run_check_asset_naming_files() -> None:
    AssetNamingCheck().run_check()
