import configparser
import json
from pathlib import Path
from typing import Any, Dict, Optional

class MultiRawConfigParser(configparser.RawConfigParser):
    """Configuration parser that supports multiple values for the same key."""
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._optcre = self.OPTCRE

    def _read(self, fp: Any, fpname: str) -> None:
        """Parse a sectioned configuration file with support for duplicate keys."""
        cursect: Optional[Dict[str, Any]] = None
        sectname: Optional[str] = None
        optname: Optional[str] = None
        lineno: int = 0
        e: Optional[configparser.ParsingError] = None
        
        for lineno, line in enumerate(fp, start=1):
            comment_start = line.find('#')
            if comment_start == 0:
                continue
            if comment_start > 0:
                line = line[:comment_start]
            line = line.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                sectname = line[1:-1]
                # Utilisation de getattr pour accéder aux attributs privés de manière sûre
                sections = getattr(self, '_sections', {})
                if sectname in sections:
                    cursect = sections[sectname]
                else:
                    dict_type = getattr(self, '_dict', dict)
                    cursect = dict_type()
                    if cursect is not None:
                        cursect['__name__'] = sectname
                    sections[sectname] = cursect
            elif cursect is None:
                raise configparser.MissingSectionHeaderError(fpname, lineno, line)
            else:
                mo = self._optcre.match(line)
                if mo:
                    optname, _, optval = mo.groups()
                    if optname and cursect:
                        if optname in cursect:
                            if not isinstance(cursect[optname], list):
                                cursect[optname] = [cursect[optname]]
                            cursect[optname].append(optval)
                        else:
                            cursect[optname] = optval
                else:
                    if not e:
                        e = configparser.ParsingError(fpname)
                    e.append(lineno, repr(line))
        if e:
            raise e


def get_project_data(project_path: Path) -> Optional[Dict[str, Any]]:
    """
    Lit et retourne les données JSON d'un projet.
    
    Args:
        project_path: Chemin vers le fichier de projet JSON
        
    Returns:
        Dictionnaire contenant les données du projet, ou None en cas d'erreur
    """
    try:
        with open(project_path, 'r', encoding='utf-8') as file:
            plugin_data: Dict[str, Any] = json.load(file)
            return plugin_data
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        print(f"Erreur lors de la lecture du fichier {project_path}: {e}")
        return None
    
def get_project_default_game_data(project_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Lit et parse le fichier DefaultGame.ini d'un projet Unreal Engine.
    
    Args:
        project_path: Chemin vers le fichier de projet
        
    Returns:
        Dictionnaire contenant les données de configuration par section
    """
    default_game_path = project_path.parent / "Config" / "DefaultGame.ini"

    # Initialiser ConfigParser avec options pour préserver la casse
    config = configparser.ConfigParser(allow_no_value=True, strict=False, interpolation=None)
    config.optionxform = str  # type: ignore[method-assign, assignment]  # Preserve option case
    
    config.read(default_game_path, encoding='utf-8')

    data: Dict[str, Dict[str, Any]] = {}
    for section in config.sections():
        items = config.items(section)
        section_data: Dict[str, Any] = {}
        for key, value in items:
            if key in section_data:
                # Si la clé existe déjà, transforme sa valeur en liste si ce n'est pas déjà fait
                if not isinstance(section_data[key], list):
                    section_data[key] = [section_data[key]]
                section_data[key].append(value)
            else:
                section_data[key] = value
        data[section] = section_data
    
    return data

def get_project_path(project_path: Path) -> Path:
    """
    Retourne le chemin racine du projet.
    
    Args:
        project_path: Chemin vers le fichier de projet
        
    Returns:
        Chemin vers le dossier racine du projet
    """
    return project_path.parent


def get_project_content_path(project_path: Path) -> Path:
    """
    Retourne le chemin vers le dossier Content du projet.
    
    Args:
        project_path: Chemin vers le fichier de projet
        
    Returns:
        Chemin vers le dossier Content
    """
    return project_path.parent / "Content"


def get_project_source_path(project_path: Path) -> Path:
    """
    Retourne le chemin vers le dossier Source du projet.
    
    Args:
        project_path: Chemin vers le fichier de projet
        
    Returns:
        Chemin vers le dossier Source
    """
    return project_path.parent / "Source"


def get_project_plugin_path(project_path: Path) -> Path:
    """
    Retourne le chemin vers le dossier Plugins du projet.
    
    Args:
        project_path: Chemin vers le fichier de projet
        
    Returns:
        Chemin vers le dossier Plugins
    """
    return project_path.parent / "Plugins"