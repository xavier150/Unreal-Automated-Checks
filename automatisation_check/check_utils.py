from pathlib import Path
from typing import List

from . import config
from . import plugin_utils
from . import project_utils

def get_project_and_plugin_content_paths() -> List[Path]:
    """Get project and plugin content paths using pathlib for path operations."""
    location_to_check: List[Path] = []
    location_to_check.append(project_utils.get_project_content_path(config.project_path))
    plugin_list = plugin_utils.get_valid_plugin_path_list(config.project_path)
    exclude_plugin_check = config.exclude_plugin_check

    for plugin_path in plugin_list:
        # Use pathlib's .name property instead of os.path.basename
        file_name = plugin_path.name
        if file_name not in exclude_plugin_check:
            plugin_data = plugin_utils.get_plugin_data(plugin_path)
            if plugin_data:
                can_contain_content = plugin_data.get('CanContainContent', False)
                if can_contain_content:
                    plugin_content_path = plugin_utils.get_plugin_content_path(plugin_path)
                    location_to_check.append(plugin_content_path)
    return location_to_check

def get_project_and_plugin_source_paths() -> List[Path]:
    """Get project and plugin source paths using pathlib for path operations."""
    location_to_check: List[Path] = []
    location_to_check.append(project_utils.get_project_source_path(config.project_path))
    plugin_list = plugin_utils.get_valid_plugin_path_list(config.project_path)
    exclude_plugin_check = config.exclude_plugin_check

    for plugin_path in plugin_list:
        # Use pathlib's .name property instead of os.path.basename
        file_name = plugin_path.name
        if file_name not in exclude_plugin_check:
            plugin_data = plugin_utils.get_plugin_data(plugin_path)
            if plugin_data:
                plugin_content_path = plugin_utils.get_plugin_source_path(plugin_path)
                location_to_check.append(plugin_content_path)
    return location_to_check

def get_project_empty_path_check()-> List[Path]:
    """Get additional root paths to include in empty-folder checks."""
    return config.additional_empty_paths_to_check