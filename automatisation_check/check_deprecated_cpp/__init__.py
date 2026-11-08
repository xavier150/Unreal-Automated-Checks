import importlib

from . import check_deprecated_cpp

if "check_deprecated_cpp" in locals():
    importlib.reload(check_deprecated_cpp)
