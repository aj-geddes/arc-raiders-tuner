# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Repository**: https://github.com/aj-geddes/arc-raiders-tuner

## Project Overview

Arc Raiders Config Tuner is a Windows GUI application for managing Arc Raiders game configuration. It's a single-file Python/tkinter application with zero runtime dependencies (uses only Python stdlib). The tool reads/writes `GameUserSettings.ini` files for the Unreal Engine 5-based game.

## Commands

### Run from source
```bash
python arc_tuner.py
```

### Run tests
```bash
python tests.py
# Or with pytest:
python -m pytest tests.py -v
```

### Build standalone executable (Windows)
```bash
# Using build script:
build.bat

# Or manually:
pip install pyinstaller
pyinstaller --onefile --windowed --name "ArcRaidersTuner" arc_tuner.py
```

## Architecture

The application has a single main file (`arc_tuner.py`) with three major components:

1. **Configuration Definitions** (lines 32-466): `SETTINGS_DEFINITIONS` dict maps setting keys to `SettingDefinition` dataclasses containing metadata (display name, description, type, valid options, performance impact). `PRESETS` dict defines preset configurations (Competitive, Balanced, Quality, Cinematic).

2. **ConfigManager class** (lines 473-757): Handles all file I/O operations:
   - Reads/writes UE5 INI format (not standard configparser due to section naming)
   - Manages backups in `ArcTuner_Backups/` subdirectory
   - Manages profiles as JSON in `ArcTuner_Profiles/` subdirectory
   - Includes path validation for security

3. **ArcTunerApp class** (lines 764-1454): tkinter GUI with:
   - Tabbed interface organized by `category` field from settings definitions
   - Dynamic widget generation based on `setting_type` (choice, boolean, number, slider)
   - Menu bar for file/profile/backup/preset operations

### Key Design Patterns

- Settings are defined declaratively in `SETTINGS_DEFINITIONS`; UI is generated from these definitions
- The `section` field in settings maps to INI sections like `/Script/EmbarkUserSettings.EmbarkGameUserSettings` or `ScalabilityGroups`
- Choice options can be simple strings or tuples of `(stored_value, display_name)` for value mapping
- Tests mock tkinter entirely for headless execution

### File Locations (Windows)

- Game config: `%LOCALAPPDATA%\ArcRaiders\Saved\Config\Windows\GameUserSettings.ini`
- Backups: `%LOCALAPPDATA%\ArcRaiders\Saved\Config\Windows\ArcTuner_Backups\`
- Profiles: `%LOCALAPPDATA%\ArcRaiders\Saved\Config\Windows\ArcTuner_Profiles\`
