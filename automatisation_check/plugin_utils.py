import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import config

def get_plugin_data(plugin_path: Path) -> Optional[Dict[str, Any]]:
    """Load plugin data from .uplugin file."""
    try:
        with open(plugin_path, 'r', encoding='utf-8') as file:
            plugin_data: Dict[str, Any] = json.load(file)
            return plugin_data
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error while reading file {plugin_path}: {e}")
        return None


def get_valid_plugin_path_list(project_path: Path) -> List[Path]:
    """Get list of valid plugin paths using pathlib for file system operations."""
    plugin_path = project_path.parent / "Plugins"
    plugin_list: List[Path] = []
    exclude_plugin_check = config.exclude_plugin_check

    # Use pathlib's rglob to find all .uplugin files recursively
    for uplugin_file in plugin_path.rglob("*.uplugin"):
        if uplugin_file.name not in exclude_plugin_check:
            plugin_list.append(uplugin_file)

    return plugin_list

def get_excluded_plugin_path_list(project_path: Path) -> List[Path]:
    """Get list of excluded plugin paths using pathlib for file system operations."""
    plugin_path = project_path.parent / "Plugins"
    excluded_plugin_list: List[Path] = []
    exclude_plugin_check = config.exclude_plugin_check

    # Use pathlib's rglob to find all .uplugin files recursively
    for uplugin_file in plugin_path.rglob("*.uplugin"):
        if uplugin_file.name in exclude_plugin_check:
            excluded_plugin_list.append(uplugin_file)

    return excluded_plugin_list

def get_excluded_plugin_root_path_list(project_path: Path) -> List[Path]:
    """Get list of excluded plugin root paths using pathlib for file system operations."""
    plugin_path = project_path.parent / "Plugins"
    excluded_plugin_root_list: List[Path] = []
    exclude_plugin_check = config.exclude_plugin_check

    # Use pathlib's rglob to find all .uplugin files recursively
    for uplugin_file in plugin_path.rglob("*.uplugin"):
        if uplugin_file.name in exclude_plugin_check:
            excluded_plugin_root_list.append(uplugin_file.parent)

    return excluded_plugin_root_list

def get_valid_plugin_content_path_list(project_path: Path) -> List[Path]:
    """Get list of valid plugin content paths using pathlib for file system operations."""
    plugin_path = project_path.parent / "Plugins"
    plugin_directories: List[Path] = []

    # Use pathlib's rglob to find all .uplugin files recursively
    for uplugin_file in plugin_path.rglob("*.uplugin"):
        content_path = uplugin_file.parent / "Content"
        if content_path not in plugin_directories:  # Avoid duplicates
            plugin_directories.append(content_path)

    return plugin_directories

def get_plugin_content_path(project_path: Path) -> Path:
    content_path = project_path.parent / "Content"
    return content_path

def get_plugin_source_path(project_path: Path) -> Path:
    content_path = project_path.parent / "Source"
    return content_path