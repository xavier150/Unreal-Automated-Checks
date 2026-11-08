import importlib

from . import base_check
from . import config
from . import bpl
from . import project_utils
from . import plugin_utils
from . import project_version_utils
from . import check_utils
from . import utils
from . import check_asset_naming
from . import check_build_additional_files
from . import check_build_icon
from . import check_copyright_info
from . import check_deprecated_cpp
from . import check_deprecated_bp
from . import check_empty_folders
from . import check_encoding_files
from . import check_project_info
from . import check_project_version
from . import main

if "base_check" in locals():
    importlib.reload(base_check)
if "config" in locals():
    importlib.reload(config)
if "bpl" in locals():
    importlib.reload(bpl)
if "project_utils" in locals():
    importlib.reload(project_utils)
if "plugin_utils" in locals():
    importlib.reload(plugin_utils)
if "project_version_utils" in locals():
    importlib.reload(project_version_utils)
if "check_utils" in locals():
    importlib.reload(check_utils)
if "utils" in locals():
    importlib.reload(utils)
if "check_asset_naming" in locals():
    importlib.reload(check_asset_naming)
if "check_build_additional_files" in locals():
    importlib.reload(check_build_additional_files)
if "check_build_icon" in locals():
    importlib.reload(check_build_icon)
if "check_copyright_info" in locals():
    importlib.reload(check_copyright_info)
if "check_deprecated_cpp" in locals():
    importlib.reload(check_deprecated_cpp)
if "check_deprecated_bp" in locals():
    importlib.reload(check_deprecated_bp)
if "check_empty_folders" in locals():
    importlib.reload(check_empty_folders)
if "check_encoding_files" in locals():
    importlib.reload(check_encoding_files)
if "check_project_info" in locals():
    importlib.reload(check_project_info)
if "check_project_version" in locals():
    importlib.reload(check_project_version)
if "main" in locals():
    importlib.reload(main)
