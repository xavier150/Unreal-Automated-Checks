"""Report Blueprint deprecation diagnostics using Unreal's native commandlet.

This checks compiler messages, not all deprecated declarations. Suppressed
diagnostics, unused deprecated members and level Blueprints may not be reported.
No C++ source files are scanned and the commandlet does not save compiled assets.
"""

from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from .. import base_check
from .. import bpl
from .. import config
from . import check_deprecated_bp_utils as utils


class DeprecatedBpCheck(base_check.BaseCheck):
    name = "Deprecated Blueprint"

    def run_check(self) -> None:
        print("- Checking Blueprint deprecation diagnostics...")
        editor = config.unreal_path.with_name("UnrealEditor-Cmd.exe")
        project = config.project_path.resolve()
        if not editor.is_file() or not project.is_file():
            print(
                f"Blueprint deprecation check incomplete: editor or project missing: "
                f"{editor}, {project}"
            )
            return

        log_path = project.parent / "Saved" / "AutomatisationChecks" / "check_deprecated_bp.log"
        try:
            assets = utils.get_asset_allow_list()
            if not assets:
                print("No project/plugin .uasset candidates found; Blueprint compilation skipped.")
                return
            log_path.parent.mkdir(parents=True, exist_ok=True)
            # Unreal resolves AllowListFile relative to the project directory.
            with TemporaryDirectory(prefix="bp_check_", dir=project.parent) as directory:
                allow_list = Path(directory) / "assets.txt"
                # LoadANSITextFileToStrings widens each byte; UTF-8 is not supported.
                allow_list.write_text("\n".join(assets) + "\n", encoding="latin-1")
                command = [
                    str(editor),
                    str(project),
                    "-run=CompileAllBlueprints",
                    f"-AllowListFile={allow_list.relative_to(project.parent)}",
                    "-ShowResultsOnly",
                    "-unattended",
                    "-nop4",
                    "-nosplash",
                    "-NullRHI",
                    "-culture=en",
                    "-stdout",
                    "-FullStdOutLogOutput",
                    "-UTF8Output",
                ]
                print("Running: " + subprocess.list2cmdline(command))
                print(f"Compilation can take several minutes. Log: {log_path}")
                with log_path.open("w", encoding="utf-8") as log:
                    result = subprocess.run(
                        command,
                        cwd=project.parent,
                        stdin=subprocess.DEVNULL,
                        stdout=log,
                        stderr=subprocess.STDOUT,
                        check=False,
                    )
            report = utils.parse_compilation_log(log_path)
        except (OSError, UnicodeError) as error:
            print(f"Blueprint deprecation check incomplete: {error}. Log: {log_path}")
            return

        for asset, line_number, message in report.findings:
            print(
                bpl.color_set.yellow(
                    f"Warning! Blueprint deprecation at {asset}: {message} "
                    f"(log {log_path}:{line_number})"
                )
            )
        print(
            f"Found {len(report.findings)} Blueprint deprecation diagnostic(s); "
            f"{report.compiled_assets} Blueprint asset(s) selected by Unreal."
        )
        if report.summary is None:
            print(
                f"Blueprint deprecation check incomplete: no compilation summary "
                f"(exit code {result.returncode}). See {log_path}"
            )
        else:
            errors, warnings, failed_loads = report.summary
            print(
                f"Blueprint compiler: {errors} error(s), {warnings} warning(s), "
                f"{failed_loads} failed load(s)."
            )
            if result.returncode or errors or failed_loads:
                print(
                    f"Blueprint deprecation check incomplete: compilation/load failure "
                    f"(exit code {result.returncode}). See {log_path}"
                )
            elif not report.findings:
                print("No Blueprint deprecation diagnostics emitted by the compiler.")
        print(
            "Coverage: project and non-excluded plugin Blueprint assets only; "
            "level Blueprints, unused declarations and suppressed diagnostics "
            "are not guaranteed to be detected."
        )


def run_check_deprecated_bp() -> None:
    DeprecatedBpCheck().run_check()
