import importlib

from . import check_encoding_files

if "check_encoding_files" in locals():
    importlib.reload(check_encoding_files)
