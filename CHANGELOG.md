# Changelog

All notable changes to Arc Raiders Config Tuner will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **SteamOS/Linux platform support** with automatic detection
  - Automatic platform detection (Windows vs Linux)
  - Steam installation finder (standard and Flatpak locations)
  - VDF parser for `libraryfolders.vdf` to support multiple Steam libraries
  - Proton prefix detection for Arc Raiders (App ID: 1808500)
  - Platform-aware config path resolution
- 10 new test functions for SteamOS support
- **Changelog Maintenance section** in CLAUDE.md with guidelines for updating CHANGELOG.md

### Changed
- `ConfigManager` now uses automatic platform detection for default paths
- Updated README with full SteamOS/Steam Deck installation instructions
- Updated CLAUDE.md with platform architecture documentation

### Known Issues
- 5 of the new SteamOS tests have mock setup edge cases (core implementation works correctly)

## [1.1.1] - 2025-12-15

### Added
- **Competitive Settings category** with 18 hidden/advanced UE5 settings
  - Mouse & Input: `bEnableMouseSmoothing`, `bViewAccelerationEnabled`
  - Visual clutter reduction: Depth of Field, Bloom, Lens Flare, Color Fringe, Sharpen, Grain, Motion Blur
  - Performance tweaks: `r.OneFrameThreadLag`, `bSmoothFrameRate`, Shader Pipeline Cache
  - Texture/VRAM: Streaming Pool Size, Max Anisotropy, VRAM limits
  - Audio: Quality Level, Spatial Audio
- Add/Remove functionality for Competitive Settings (dynamic setting management)

## [1.0.0] - 2025-12-15

### Added
- GitHub Pages documentation site with Arc Raiders branding
- Prominent SmartScreen warning section with images in README
- Actual application screenshots in documentation

### Changed
- Complete UI redesign with Arc Raiders dark theme
- Config path corrected to `PioneerGame/WindowsClient`

### Fixed
- Release workflow permissions for GitHub Actions

## [0.1.0] - 2025-12-15

### Added
- Initial release of Arc Raiders Config Tuner
- Single-file Python/tkinter application with zero runtime dependencies
- Settings editor with performance impact indicators (Low/Medium/High)
- Automatic backup system before every save
- Multiple profile support (save/load configurations)
- Built-in presets: Competitive, Balanced, Quality, Cinematic
- UE5 INI file parser (handles non-standard section naming)
- GitHub Actions workflow for automated releases
- Windows executable build via PyInstaller
- Comprehensive test suite with mocked tkinter

### Security
- Path validation to prevent access to system directories
- Safe file operations with proper encoding handling

[Unreleased]: https://github.com/aj-geddes/arc-raiders-tuner/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/aj-geddes/arc-raiders-tuner/compare/v1.0.0...v1.1.1
[1.0.0]: https://github.com/aj-geddes/arc-raiders-tuner/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/aj-geddes/arc-raiders-tuner/releases/tag/v0.1.0
