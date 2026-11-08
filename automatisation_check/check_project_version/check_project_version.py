from .. import base_check
from .. import bpl
from .. import project_version_utils


class ProjectVersionCheck(base_check.BaseCheck):
    name = "Project version"

    def run_check(self) -> bool:
        print("- Checking project version...")

        if not project_version_utils.is_valid_app_version():
            print(bpl.color_set.red(f"Project version '{project_version_utils.get_project_version()}' is not valid!"))
            print("Expected format: [RELEASE].[MAJOR].[MILESTONE].[PATCH]-[PHASE][ITERATION]")
            print("Example: 1.0.0.0-ap19 more details: https://github.com/xavier150/MMVS/wiki/Versioning")
            return False

        return True


def run_check_project_version() -> bool:
    return ProjectVersionCheck().run_check()