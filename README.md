# Unreal Automated Checks

A Python script that runs automated checks on an Unreal Engine project, either all at once or individually. It checks project settings, build files, empty folders, source file encoding, C++ deprecation markers, Blueprint compilation, and copyright information. It also displays project code statistics.

![Automated check results in the VS Code terminal](https://github.com/xavier150/Unreal-Automated-Checks/wiki/images/terminal_result.png)

> **Note:** The configuration is currently hardcoded and set up for development of the [MMVS video game](https://github.com/xavier150/MMVS). A command-line interface for controlling the checks is planned for a future update.

## Usage

Run `run_automatisation_check.py` and select a numbered option:

- `[1] ALL` runs every check.
- `[2]` through `[11]` run one check.

An invalid choice displays an error and prompts again.

## Checks

### [2] Check Project Version

Checks that the project version follows the expected format:
`[RELEASE].[MAJOR].[MILESTONE].[PATCH]-[PHASE][ITERATION]`.

Example: `1.0.0.0-ap19`. See [MMVS versioning](https://github.com/xavier150/MMVS/wiki/Versioning) for details.

### [3] Check Build Icon

Checks that the Windows and Linux application icons are present. Missing icons
are reported with guidance on where to set them in Unreal Editor.

### [4] Check Additional Build Files

Checks script line endings in the Windows and Linux additional build files:
LF for `.sh` scripts and CRLF for `.bat` scripts.

### [5] Check Empty Folders

Finds empty folders in project and non-excluded plugin content and source,
as well as any configured additional locations. Excluded content folders are skipped.

Offers to delete the empty folders, but only after confirmation.

### [6] Check File Encoding

Checks that `.h`, `.cpp`, and `.Build.cs` source files in the project and
non-excluded plugins are valid UTF-8.

Reports the location of invalid bytes and offers to open affected files.

### [7] Check Deprecated C++

Finds `UE_DEPRECATED`, `DeprecatedFunction`, and `DeprecatedProperty` markers
in project and non-excluded plugin `.h` and `.cpp` files.

Reports each matching file, line number, and source line. This searches for
deprecation declarations, including markers in comments, not calls to deprecated APIs.

### [8] Check Deprecated Blueprint

Reports deprecation messages, warnings, and errors in three separate reports
for Blueprints in the project and non-excluded plugins. It can take
several minutes and does not save changes to assets.

(Right-click -> Open image in new tab to view full size)  
<img src="https://github.com/xavier150/Unreal-Automated-Checks/wiki/images/check_deprecated_bp_terminal_result.png" alt="Check Deprecated Blueprint" width="50%" />

Unused deprecated elements and level Blueprints may not be reported.

### [9] Check Copyright

Checks that the first line of each `.h`, `.cpp`, and `.Build.cs` source file
contains the copyright notice configured in the project settings.
Includes project and non-excluded plugin sources.

Reports mismatches and offers to open affected files.

### [10] Check Asset Naming

Not yet available. This option currently performs no checks.

### [11] Check Project Info

Displays code statistics for project and non-excluded plugin `.h`, `.cpp`,
and `.cs` files: file count, total and non-empty lines, and total size.
Also lists the ten largest code files.

(Right-click -> Open image in new tab to view full size)  
<img src="https://github.com/xavier150/Unreal-Automated-Checks/wiki/images/check_project_info_terminal_result.png" alt="Check Project Info" width="50%" />

## Additional Notes

You can join my Discord server for more information or if you need help.  

Discord [<img src="https://github.com/xavier150/Unreal-Automated-Checks/wiki/images/socials/discord_symbol_blurple.png" alt="Discord Icon" width="auto" height="12">](https://discord.gg/XuYeGCFtxa) ->
[BleuRaven side projects](https://discord.gg/XuYeGCFtxa)  