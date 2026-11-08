import importlib

from . import check_build_icon

if "check_build_icon" in locals():
    importlib.reload(check_build_icon)
