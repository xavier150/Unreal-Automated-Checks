import importlib

from . import check_asset_naming

if "check_asset_naming" in locals():
    importlib.reload(check_asset_naming)
