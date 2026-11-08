from pathlib import Path
from typing import List


def check_files(icon_filepath: Path) -> List[str]:
    """Check script line endings in the build files folder."""
    issues: List[str] = []

    for filepath in icon_filepath.parent.rglob("*"):
        if not filepath.is_file():
            continue

        if filepath.name.endswith(".sh"):
            try:
                content = filepath.read_bytes()
                if b"\r\n" in content:
                    issues.append(f"{filepath} contains CRLF (should be LF for .sh)")
            except OSError as error:
                issues.append(f"Could not check {filepath}: {error}")
        elif filepath.name.endswith(".bat"):
            try:
                content = filepath.read_bytes()
                if b"\n" in content and b"\r\n" not in content:
                    issues.append(
                        f"{filepath} contains LF only (should be CRLF for .bat)"
                    )
            except OSError as error:
                issues.append(f"Could not check {filepath}: {error}")

    return issues
