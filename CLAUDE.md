# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Repository**: https://github.com/aj-geddes/arc-raiders-tuner

## Project Overview

Arc Raiders Config Tuner is a cross-platform GUI application for managing Arc Raiders game configuration on Windows and Linux/SteamOS. It's a single-file Python/tkinter application with zero runtime dependencies (uses only Python stdlib). The tool reads/writes `GameUserSettings.ini` files for the Unreal Engine 5-based game.

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

## Changelog Maintenance

**IMPORTANT**: Always update `CHANGELOG.md` when making notable changes to the codebase. The changelog should be updated in the same commit as the feature or fix.

### Guidelines

1. **Format**: Follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format
2. **Location**: Add all changes under the `[Unreleased]` section at the top of the file
3. **Categories**: Use these standard categories in order:
   - `### Added` - New features
   - `### Changed` - Changes to existing functionality
   - `### Deprecated` - Soon-to-be removed features
   - `### Removed` - Removed features
   - `### Fixed` - Bug fixes
   - `### Security` - Security-related changes
4. **Style**:
   - Use present tense ("Add feature" not "Added feature")
   - Be concise but descriptive
   - Group related changes with sub-bullets when appropriate
   - Bold the main feature/component name for clarity

### Example Workflow

```bash
# 1. Make your code changes
vim arc_tuner.py

# 2. Update the changelog
vim CHANGELOG.md
# Add entry under [Unreleased] > ### Added (or appropriate category):
# - **New setting**: Add FOV slider for first-person view

# 3. Commit both together
git add arc_tuner.py CHANGELOG.md
git commit -m "Add FOV slider for first-person view"
```

### What to Document

**DO document**:
- New features or settings
- Changes to existing behavior
- Bug fixes
- Performance improvements
- Breaking changes
- Security fixes
- Documentation updates (major ones)

**DON'T document**:
- Code refactoring with no user-visible changes
- Minor typo fixes in comments
- Internal test improvements (unless adding major test coverage)

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

### Platform Detection & Multi-Platform Support

The application supports both Windows and Linux/SteamOS through platform-specific path resolution:

#### Platform Constants
- **`IS_WINDOWS`**: Boolean flag set at module load time (`platform.system() == 'Windows'`)
- **`IS_LINUX`**: Boolean flag set at module load time (`platform.system() == 'Linux'`)
- **`ARC_RAIDERS_APP_ID`**: Constant string `'1808500'` (Steam App ID for Arc Raiders)

#### Path Resolution Functions

**`find_steam_path() -> Optional[Path]`**
- Locates the Steam installation directory on Linux/SteamOS
- Checks standard location: `~/.local/share/Steam/`
- Checks Flatpak location: `~/.var/app/com.valvesoftware.Steam/.local/share/Steam/`
- Returns `None` if Steam is not found
- Only called on Linux systems

**`find_proton_prefix(app_id: str) -> Optional[Path]`**
- Locates the Proton compatibility prefix for a given Steam app
- Searches all Steam library folders by parsing `libraryfolders.vdf`
- Looks for `steamapps/compatdata/{app_id}/pfx/` in each library
- Returns the first valid prefix found, or `None` if not found
- Uses minimal VDF parser (see below)

**`get_default_config_path() -> Optional[Path]`**
- Returns the platform-appropriate default config path
- **Windows**: `%LOCALAPPDATA%\PioneerGame\Saved\Config\WindowsClient\GameUserSettings.ini`
- **Linux/SteamOS**: `{proton_prefix}/drive_c/users/steamuser/AppData/Local/PioneerGame/Saved/Config/WindowsClient/GameUserSettings.ini`
- Path resolution is lazy (only computed when needed)
- Returns `None` if the config cannot be located

#### VDF Parser

The application includes a minimal VDF (Valve Data File) parser that handles only the `libraryfolders.vdf` format:
- Parses simple nested key-value structure used by Steam
- Extracts library folder paths from the `"path"` keys
- Does not attempt to parse full VDF spec (only what's needed for library detection)
- Handles both quoted strings and numeric values

### Competitive Settings Category

The application includes a "Competitive Settings" category containing hidden/advanced UE5 settings for competitive players. These settings span multiple INI sections:

- **Mouse & Input settings** (`/Script/Engine.InputSettings`): Controls like `bEnableMouseSmoothing` and `bViewAccelerationEnabled` that affect input responsiveness
- **Visual clutter reduction** (`SystemSettings`): Console variables like `r.DepthOfFieldQuality`, `r.BloomQuality`, `r.LensFlareQuality`, `r.SceneColorFringeQuality`, `r.Tonemapper.Sharpen`, `r.TonemapperGrainQuantization`, and `r.MotionBlur.Max` for cleaner visuals
- **Performance tweaks** (`SystemSettings` and `/Script/Engine.Engine`): Settings like `r.OneFrameThreadLag`, `bSmoothFrameRate`, and `r.ShaderPipelineCache.Enabled` that affect frame pacing and latency
- **Texture/VRAM settings** (`SystemSettings`): Options like `r.Streaming.PoolSize`, `r.MaxAnisotropy`, and `r.Streaming.LimitPoolSizeToVRAM` for texture quality vs performance
- **Audio settings** (`/Script/EmbarkUserSettings.EmbarkGameUserSettings`): `AudioQualityLevel` and `bEnableAudioSpatialisation` for positional audio in competitive play

### File Locations

#### Windows
- Game config: `%LOCALAPPDATA%\PioneerGame\Saved\Config\WindowsClient\GameUserSettings.ini`
- Backups: `%LOCALAPPDATA%\PioneerGame\Saved\Config\WindowsClient\ArcTuner_Backups\`
- Profiles: `%LOCALAPPDATA%\PioneerGame\Saved\Config\WindowsClient\ArcTuner_Profiles\`

#### Linux/SteamOS
- Steam (standard): `~/.local/share/Steam/`
- Steam (Flatpak): `~/.var/app/com.valvesoftware.Steam/.local/share/Steam/`
- Library folders config: `{steam_path}/steamapps/libraryfolders.vdf`
- Game config: `{steam_path}/steamapps/compatdata/1808500/pfx/drive_c/users/steamuser/AppData/Local/PioneerGame/Saved/Config/WindowsClient/GameUserSettings.ini`
- Backups: `{config_dir}/ArcTuner_Backups/` (same directory as config file)
- Profiles: `{config_dir}/ArcTuner_Profiles/` (same directory as config file)

**Note**: On Linux, the config path may vary depending on which Steam library the game is installed in. The application searches all library folders to locate the correct Proton prefix.
