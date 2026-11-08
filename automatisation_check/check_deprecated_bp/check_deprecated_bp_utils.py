"""Asset selection and parsing for the native CompileAllBlueprints commandlet."""

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import List, Optional, Tuple

from .. import check_utils
from .. import config
from .. import plugin_utils


def get_asset_allow_list() -> List[str]:
    """Select project/plugin assets; Unreal filters these to Blueprint subclasses."""
    mounts = {config.project_path.parent / "Content": "/Game"}
    for plugin in plugin_utils.get_valid_plugin_path_list(config.project_path):
        mounts[plugin_utils.get_plugin_content_path(plugin)] = f"/{plugin.stem}"
    excluded_roots = [
        path.resolve()
        for path in plugin_utils.get_excluded_plugin_root_path_list(config.project_path)
    ]
    assets = set()
    for content in check_utils.get_project_and_plugin_content_paths():
        for asset in sorted(content.rglob("*")):
            if not asset.is_file() or asset.suffix.lower() != ".uasset":
                continue
            resolved = asset.resolve()
            if any(root == resolved or root in resolved.parents for root in excluded_roots):
                continue
            package = asset.relative_to(content).with_suffix("").as_posix()
            assets.add(f"{mounts[content]}/{package}.{asset.stem}")
    return sorted(assets)


@dataclass
class CompilationReport:
    findings: List[Tuple[str, int, str]] = field(default_factory=list)
    compiled_assets: int = 0
    summary: Optional[Tuple[int, int, int]] = None


def parse_compilation_log(log_path: Path) -> CompilationReport:
    report = CompilationReport()
    asset_pattern = re.compile(r"Loading and Compiling: '([^']+)'")
    summary_pattern = re.compile(
        r"Compiling Completed with (\d+) errors and (\d+) warnings "
        r"and (\d+) blueprints that failed to load\."
    )
    deprecation_pattern = re.compile(r"\bdeprecat(?:ed|ion)\b", re.IGNORECASE)
    current_asset = ""
    with log_path.open("r", encoding="utf-8-sig", errors="replace") as log:
        for line_number, line in enumerate(log, start=1):
            asset_match = asset_pattern.search(line)
            if asset_match and "LogCompileAllBlueprintsCommandlet:" in line:
                current_asset = asset_match.group(1)
                report.compiled_assets += 1
            summary_match = summary_pattern.search(line)
            if summary_match:
                report.summary = (
                    int(summary_match.group(1)),
                    int(summary_match.group(2)),
                    int(summary_match.group(3)),
                )
            if (
                current_asset
                and "LogCompileAllBlueprintsCommandlet: Display:" in line
            ):
                message = line.split("LogCompileAllBlueprintsCommandlet: Display:", 1)[1].strip()
                if not asset_match and deprecation_pattern.search(message):
                    report.findings.append((current_asset, line_number, message))
    return report
