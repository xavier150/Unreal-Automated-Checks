import importlib

from . import check_project_info

if "check_project_info" in locals():
    importlib.reload(check_project_info)
