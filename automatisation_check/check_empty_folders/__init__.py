import importlib

from . import check_empty_folders

if "check_empty_folders" in locals():
    importlib.reload(check_empty_folders)
