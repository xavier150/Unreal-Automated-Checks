# Unreal Automated Checks

A Python script that runs automated checks on an Unreal Engine project, either all at once or individually. It checks project settings, build files, folders, file encoding, C++ code, copyright information, and asset naming.

![Automated check results in the VS Code terminal](https://github.com/xavier150/Unreal-Automated-Checks/wiki/images/terminal_result.png)

> **Note:** The configuration is currently hardcoded and set up for development of the [MMVS video game](https://github.com/xavier150/MMVS). A command-line interface for controlling the checks is planned for a future update.

## Usage

Run `run_automatisation_check.py` and select a numbered option:

- `[1] ALL` runs every check.
- `[2]` through `[10]` run one check.

An invalid choice displays an error and prompts again.
