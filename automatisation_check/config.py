from pathlib import Path
from typing import Dict, List

unreal_path: Path = Path(r"M:\MMVS_EngineFiles_v2\Engine\Binaries\Win64\UnrealEditor.exe")
unreal_cmd_path: Path = Path(r"M:\MMVS_EngineFiles_v2\Engine\Binaries\Win64\UnrealEditor-Cmd.exe")
project_path: Path = Path(r"M:\MMVS_ProjectFiles_v2\UnrealProject\MacroMicroVrService.uproject")
splash_and_icons_path: Path = Path(r"M:\MMVS_ProjectFiles_v2\SourceAssets\SplashAndIcons")

additional_empty_paths_to_check: List[Path] = [
    Path(r"M:\MMVS_ProjectFiles_v2\SourceAssets")
]

warning_folder_name: Dict[str, str] = {
    "Nouveau dossier": "Dossier avec nom de base",
    "NewFolder": "Dossier avec nom de base",
}

warning_file_name: Dict[str, str] = {
    "exemple.txt": "Fichier avec nom de base",
}

exclude_content_check_directory: Dict[str, str] = {
    "Developers": "...",
}

exclude_source_check_directory: Dict[str, str] = {
}

exclude_plugin_check: List[str] = [
    "VisualStudioTools.uplugin",
    "VaRest.uplugin",
    "ClangTidy.uplugin",
    "AdvancedSessions.uplugin",
    "Kdtree.uplugin",
    "AssetsCleaner.uplugin",
    "BleuRavenLightmass.uplugin",
    "Wwise.uplugin",
    "WwiseNiagara.uplugin",
    "WwiseSoundEngine.uplugin",
    "SteamAudio.uplugin",
    "SteamAudioWwise.uplugin",
    "CesiumForUnreal.uplugin",
    "WwiseMotionOpenXRHelpers.uplugin"
]

directories_to_never_cook: Dict[str, str] = {
    "DebugMaps": "...",
    "SituationSetupMaps": "...",
}