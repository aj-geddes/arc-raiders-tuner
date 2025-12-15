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

The application has a single main file (`arc_tuner.py`, ~1900 lines) with three major components:

1. **Configuration Definitions** (lines 49-618): `SETTINGS_DEFINITIONS` dict maps setting keys to `SettingDefinition` dataclasses containing metadata (display name, description, type, valid options, performance impact). `PRESETS` dict defines preset configurations (Competitive, Balanced, Quality, Cinematic).

2. **ConfigManager class** (lines 716-1000): Handles all file I/O operations:
   - Reads/writes UE5 INI format (not standard configparser due to section naming)
   - Manages backups in `ArcTuner_Backups/` subdirectory
   - Manages profiles as JSON in `ArcTuner_Profiles/` subdirectory
   - Includes path validation for security

3. **ArcTunerApp class** (lines 1007+): tkinter GUI with:
   - Tabbed interface organized by `category` field from settings definitions
   - Dynamic widget generation based on `setting_type` (choice, boolean, number, slider)
   - Menu bar for file/profile/backup/preset operations

### Key Design Patterns

- Settings are defined declaratively in `SETTINGS_DEFINITIONS`; UI is generated from these definitions
- The `section` field in settings maps to INI sections like `/Script/EmbarkUserSettings.EmbarkGameUserSettings` or `ScalabilityGroups`
- Choice options can be simple strings or tuples of `(stored_value, display_name)` for value mapping
- Tests mock tkinter entirely for headless execution

### Competitive Settings Category

The application includes a "Competitive Settings" category containing hidden/advanced UE5 settings for competitive players. These settings span multiple INI sections:

- **Mouse & Input settings** (`/Script/Engine.InputSettings`): Controls like `bEnableMouseSmoothing` and `bViewAccelerationEnabled` that affect input responsiveness
- **Visual clutter reduction** (`SystemSettings`): Console variables like `r.DepthOfFieldQuality`, `r.BloomQuality`, `r.LensFlareQuality`, `r.SceneColorFringeQuality`, `r.Tonemapper.Sharpen`, `r.TonemapperGrainQuantization`, and `r.MotionBlur.Max` for cleaner visuals
- **Performance tweaks** (`SystemSettings` and `/Script/Engine.Engine`): Settings like `r.OneFrameThreadLag`, `bSmoothFrameRate`, and `r.ShaderPipelineCache.Enabled` that affect frame pacing and latency
- **Texture/VRAM settings** (`SystemSettings`): Options like `r.Streaming.PoolSize`, `r.MaxAnisotropy`, and `r.Streaming.LimitPoolSizeToVRAM` for texture quality vs performance
- **Audio settings** (`/Script/EmbarkUserSettings.EmbarkGameUserSettings`): `AudioQualityLevel` and `bEnableAudioSpatialisation` for positional audio in competitive play

### File Locations (Windows)

- Game config: `%LOCALAPPDATA%\PioneerGame\Saved\Config\Windows\GameUserSettings.ini`
- Backups: `%LOCALAPPDATA%\PioneerGame\Saved\Config\Windows\ArcTuner_Backups\`
- Profiles: `%LOCALAPPDATA%\PioneerGame\Saved\Config\Windows\ArcTuner_Profiles\`
