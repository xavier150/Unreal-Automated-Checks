import importlib

from . import check_copyright_info

if "check_copyright_info" in locals():
    importlib.reload(check_copyright_info)
