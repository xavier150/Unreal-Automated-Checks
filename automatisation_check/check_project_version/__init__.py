import importlib

from . import check_project_version

if "check_project_version" in locals():
    importlib.reload(check_project_version)
