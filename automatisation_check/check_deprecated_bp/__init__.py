import importlib

from . import check_deprecated_bp_utils
from . import check_deprecated_bp

if "check_deprecated_bp_utils" in locals():
    importlib.reload(check_deprecated_bp_utils)
if "check_deprecated_bp" in locals():
    importlib.reload(check_deprecated_bp)
