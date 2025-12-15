# Arc Raiders Config Tuner - Graphics Settings Optimizer & Performance Tool

**Boost your FPS and optimize Arc Raiders graphics settings** with this powerful configuration manager. Fine-tune DLSS, FSR, Ray Tracing, NVIDIA Reflex, and competitive settings for maximum performance on Windows, Steam Deck, and Linux.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20SteamOS%20%7C%20Steam%20Deck%20%7C%20Linux-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Downloads](https://img.shields.io/github/downloads/aj-geddes/arc-raiders-tuner/total?label=downloads)
![GitHub stars](https://img.shields.io/github/stars/aj-geddes/arc-raiders-tuner?style=social)

**Topics**: `arc-raiders` `game-optimizer` `fps-boost` `dlss` `fsr` `nvidia-reflex` `steam-deck` `graphics-settings` `performance-tuning` `config-manager` `ray-tracing` `competitive-gaming` `unreal-engine` `gaming-tools`

## Quick Download

**[Download Latest Release](https://github.com/aj-geddes/arc-raiders-tuner/releases/latest)** | **[View Documentation](https://aj-geddes.github.io/arc-raiders-tuner/)**

Get the standalone Windows executable or run from source on any platform.

## Platform Support

- **Windows 10/11** - Native support with standalone .exe (no installation required)
- **Steam Deck / SteamOS** - Full compatibility via Proton (Arc Raiders is Steam Deck Verified)
- **Linux** - Works with Steam/Proton on all distributions

## Key Features

- **Graphics Settings Optimization** - Fine-tune DLSS, FSR 3, XeSS upscaling for maximum FPS
- **Latency Reduction** - Configure NVIDIA Reflex and frame generation settings
- **Ray Tracing Controls** - Adjust RTX Global Illumination for quality vs performance
- **Competitive Settings** - Hidden console variables for reduced input lag and visual clarity
- **Automatic Backups** - Never lose your settings, backups created before every save
- **Profile Management** - Save and load different configurations (competitive, quality, etc.)
- **Built-in Presets** - One-click optimization for common use cases
- **Secure & Private** - No network access, validates all file paths, no code execution
- **Zero Dependencies** - Single .exe on Windows, Python stdlib only on Linux

## Screenshot

![Arc Raiders Config Tuner - Graphics Settings Interface showing DLSS, FSR, and Ray Tracing controls](docs/assets/images/screenshot.png)

*Dark theme with Arc Raiders branding • Tabbed interface for graphics settings • Performance impact indicators • One-click optimization presets*

## Installation

### Windows - Quick Start

#### Option 1: Download Pre-built Executable (Recommended)
1. **[Download ArcRaidersTuner.exe](https://github.com/aj-geddes/arc-raiders-tuner/releases/latest)** from the Releases page
2. Run it - no installation required, instant access to all graphics settings!

#### Windows SmartScreen Warning

When you first run the app, Windows will show a SmartScreen warning. **This is normal** for open-source software that isn't signed with an expensive code signing certificate.

| Step 1: Click "More info" | Step 2: Click "Run anyway" |
|:-------------------------:|:--------------------------:|
| ![SmartScreen Step 1](docs/assets/images/smartscreen-1.png) | ![SmartScreen Step 2](docs/assets/images/smartscreen-2.png) |

The app is completely safe — the full source code is available in this repository for review.

#### Option 2: Run from Source (Windows)
```bash
# Clone or download this repository
git clone https://github.com/aj-geddes/arc-raiders-tuner.git
cd arc-raiders-tuner

# Run directly (requires Python 3.8+)
python arc_tuner.py
```

#### Option 3: Build Your Own Executable (Windows)
```bash
# Install PyInstaller
pip install pyinstaller

# Build (Windows)
build.bat

# Or manually:
pyinstaller --onefile --windowed --name "ArcRaidersTuner" arc_tuner.py
```

### Steam Deck / SteamOS - Optimize Performance

Perfect for optimizing Arc Raiders graphics settings on your Steam Deck!

1. **Switch to Desktop Mode** - Press the Steam button, select "Power", then "Switch to Desktop"
2. **Install Python tkinter** (if not already installed):
   ```bash
   # SteamOS 3.x (Arch-based)
   sudo pacman -S tk

   # Or use the Discover app store to install "Python tkinter"
   ```
3. **Download the repository**:
   ```bash
   git clone https://github.com/aj-geddes/arc-raiders-tuner.git
   cd arc-raiders-tuner
   ```
4. **Run the application**:
   ```bash
   python3 arc_tuner.py
   ```

The app will automatically detect your Steam Deck and find the Arc Raiders config file. Perfect for tweaking FSR settings and competitive optimizations for handheld gaming!

**Note**: Arc Raiders must be run at least once to create the config file. Arc Raiders App ID is `1808500`.

### Linux (General)

Requirements:
- Python 3.8+
- tkinter (`python3-tk` on Debian/Ubuntu, `tk` on Arch)
- Steam with Proton
- Arc Raiders installed and run at least once

The app supports both standard Steam and Flatpak Steam installations and will automatically detect the correct config file location.

```bash
# Install tkinter if needed
# Debian/Ubuntu:
sudo apt install python3-tk

# Arch/SteamOS:
sudo pacman -S tk

# Fedora:
sudo dnf install python3-tkinter

# Run the app
git clone https://github.com/aj-geddes/arc-raiders-tuner.git
cd arc-raiders-tuner
python3 arc_tuner.py
```

## How to Use - Game Optimizer Guide

### First Launch - Automatic Config Detection

#### Windows
1. Run `ArcRaidersTuner.exe`
2. The app automatically finds your Arc Raiders configuration file
3. If not found, use **File → Open Config** to locate it manually

#### Steam Deck / SteamOS / Linux
1. Run `python3 arc_tuner.py`
2. The app automatically detects your platform and finds the Arc Raiders config
3. Supports both standard Steam and Flatpak Steam installations
4. If not found, use **File → Open Config** to locate it manually

### Optimizing Graphics Settings for FPS
1. Navigate tabs: **Upscaling** (DLSS/FSR), **Latency** (Reflex), **Ray Tracing**, **Competitive Settings**
2. Adjust settings using dropdowns, checkboxes, and sliders
3. Each setting shows its **performance impact** (Low/Medium/High/Very High)
4. Click **Save Changes** when done
5. A backup is automatically created before saving

### Using Performance Presets - Quick Optimization
Quick-apply optimized configurations for instant FPS boost:
- **Competitive** - Maximum FPS, lowest input latency, reduced visual clutter
- **Balanced** - Great visuals with solid performance
- **Quality** - Maximum visual fidelity with ray tracing
- **Cinematic** - Best visuals with DLSS frame generation

### Managing Profiles
Save your custom configurations:
1. **Profiles → Save Profile** - Save current settings with a name
2. **Profiles → Load Profile** - Load a saved configuration
3. **Profiles → Manage Profiles** - Delete unwanted profiles

### Backups
Never lose your settings:
- Automatic backup created before every save
- **Backups → Create Backup** - Manual backup anytime
- **Backups → Restore Backup** - Restore any previous config
- **Backups → Open Backup Folder** - Access backup files directly

## Graphics Settings Reference - Performance Tuning Guide

### Upscaling Technologies - DLSS vs FSR vs XeSS

| Technology | Vendor | Best For | FPS Boost |
|------------|--------|----------|-----------|
| **DLSS 3** | NVIDIA | RTX 20/30/40 series - Best quality with AI upscaling | 40-120% |
| **XeSS** | Intel | All GPUs - Best quality on Intel Arc | 30-80% |
| **FSR 3** | AMD | All GPUs - No special hardware needed | 30-90% |

### DLSS Performance Modes - FPS vs Quality

| Mode | Render Scale | FPS Gain | Visual Quality | Best For |
|------|-------------|----------|----------------|----------|
| DLAA | 100% | 0% | Sharpest (AA only) | High-end GPUs |
| Quality | 67% | 30-50% | Excellent | Balanced gaming |
| Balanced | 58% | 45-65% | Good | Mid-range GPUs |
| Performance | 50% | 60-100% | Acceptable | Low-end GPUs |
| Ultra Performance | 33% | 100%+ | Blurry | 4K gaming |

### Latency Reduction - NVIDIA Reflex Settings

| Setting | Input Lag Reduction | FPS Impact | Best For |
|---------|-------------------|------------|----------|
| **Reflex On** | 20-50% lower latency | Minimal | Competitive gaming |
| **Reflex On+Boost** | 30-60% lower latency | 5-10% | CPU-bound scenarios |
| **Frame Generation** | ⚠️ Adds 15-30ms latency! | +50-100% FPS | Single-player only |

### Ray Tracing - RTX Global Illumination Settings

| Setting | Performance Cost | GPU Usage | Use Case |
|---------|-----------------|-----------|----------|
| Static | 0% | Minimal | Competitive - Maximum FPS |
| DynamicHigh | 25-35% | High | Balanced - Good visuals |
| DynamicEpic | 35-45% | Very High | Quality - Best ray tracing |

### Competitive Settings - Reduce Input Lag & Visual Clutter

> ⚠️ **WARNING**: Some settings in this section are experimental and may cause instability or visual artifacts. Settings marked with ⚠️ should be tested carefully before use in ranked matches.

#### Mouse & Input - Reduce Input Lag
| Setting | Recommended | Description | Performance Impact |
|---------|-------------|-------------|-------------------|
| Mouse Smoothing | OFF | Eliminates input lag and inconsistent aim | Improves responsiveness |
| Mouse Acceleration | OFF | Ensures consistent muscle memory | Better aim control |

#### Visual Clutter Reduction - Competitive Visibility
| Setting | Competitive Value | Effect | FPS Impact |
|---------|------------------|--------|------------|
| Depth of Field | 0 (Off) | Removes distance blur | +2-5% FPS |
| Bloom | 0 (Off) | Reduces visual noise | +1-3% FPS |
| Lens Flare | 0 (Off) | Prevents light obstruction | +1-2% FPS |
| Chromatic Aberration | 0 (Off) | Cleaner screen edges | Minimal |
| Vignette | 0 (Off) | Full peripheral visibility | Minimal |
| Film Grain | 0 (Off) | Cleaner image | Minimal |

#### Performance Tweaks - Advanced Optimization (⚠️ Experimental)
| Setting | Value | Effect | Stability |
|---------|-------|--------|-----------|
| One Frame Thread Lag | 0 | -1 frame input latency | ⚠️ May cause stuttering |
| Smooth Frame Rate | Off | Lower input latency | ⚠️ May cause stuttering |
| Precompile Shaders | On | Reduces in-game stutter | Stable |

#### VRAM & Texture Settings
| Setting | Recommendation | Notes | Performance |
|---------|---------------|-------|-------------|
| Texture Pool Size | VRAM-based | 6GB=4096MB, 8GB=6144MB, 12GB+=8192MB | Affects texture quality |
| Anisotropic Filtering | 16x | Sharper textures at angles | Minimal FPS impact |

#### Audio Settings - Competitive Advantage
| Setting | Competitive Value | Effect | Advantage |
|---------|------------------|--------|-----------|
| Audio Quality | Epic (3) | Best positional audio quality | Hear enemy footsteps clearly |
| Audio Spatialization | On | 3D audio positioning | Better enemy location tracking |

## Security

This application is designed with security in mind:

- ✅ **No network access** - Works completely offline
- ✅ **No code execution** - Only reads/writes INI files
- ✅ **Path validation** - Prevents directory traversal attacks
- ✅ **No elevation required** - Runs as standard user
- ✅ **Open source** - Full source code available for review

## File Locations

### Windows

| Item | Location |
|------|----------|
| Game Config | `%LOCALAPPDATA%\PioneerGame\Saved\Config\WindowsClient\GameUserSettings.ini` |
| Backups | `%LOCALAPPDATA%\PioneerGame\Saved\Config\WindowsClient\ArcTuner_Backups\` |
| Profiles | `%LOCALAPPDATA%\PioneerGame\Saved\Config\WindowsClient\ArcTuner_Profiles\` |

### SteamOS / Linux

| Item | Location |
|------|----------|
| Game Config | `~/.local/share/Steam/steamapps/compatdata/1808500/pfx/drive_c/users/steamuser/AppData/Local/PioneerGame/Saved/Config/WindowsClient/GameUserSettings.ini` |
| Backups | `~/.local/share/Steam/steamapps/compatdata/1808500/pfx/drive_c/users/steamuser/AppData/Local/PioneerGame/Saved/Config/WindowsClient/ArcTuner_Backups/` |
| Profiles | `~/.local/share/Steam/steamapps/compatdata/1808500/pfx/drive_c/users/steamuser/AppData/Local/PioneerGame/Saved/Config/WindowsClient/ArcTuner_Profiles/` |

**Note**: Arc Raiders App ID is `1808500`. Flatpak Steam uses a different base path but is automatically detected.

## Troubleshooting - Common Issues

### "Config File Not Found"
- **Solution**: Make sure Arc Raiders has been run at least once to generate the config file
- Use **File → Open Config** to manually locate `GameUserSettings.ini`
- On Steam Deck/Linux, ensure the game has been launched through Proton

### Graphics Settings Not Applying in Game
1. **Close Arc Raiders completely** before saving changes with the tuner
2. **Disable Steam Cloud saves** for Arc Raiders to prevent settings from being overwritten
3. Check if the config file is read-only (right-click → Properties)
4. Verify the game isn't running in the background

### Backup/Profile Errors
- Ensure you have write permissions to the Arc Raiders config folder
- On Linux/Steam Deck, check file permissions with `ls -l`
- Run as Administrator if needed on Windows (not recommended normally)

### Performance Issues After Changing Settings
- Use **Backups → Restore Backup** to revert to previous working configuration
- Try the **Balanced** preset as a starting point
- Ensure your GPU drivers are up to date for DLSS/FSR support

## Building from Source

### Windows Executable Build

Requirements:
- Python 3.8 or higher
- Windows 10/11

```bash
# Install PyInstaller for building standalone executable
pip install pyinstaller

# Build portable Windows executable (no installation required)
pyinstaller --onefile --windowed --name "ArcRaidersTuner" arc_tuner.py

# The standalone .exe will be in the dist/ folder
```

### Running from Source (All Platforms)

Requirements:
- Python 3.8 or higher
- tkinter (`python3-tk` on Debian/Ubuntu, `tk` on Arch/SteamOS)

```bash
# No build needed - run the Python script directly
python3 arc_tuner.py
```

## Contributing to Arc Raiders Tuner

Contributions welcome! Help improve this game optimizer:
1. Fork the repository on GitHub
2. Create a feature branch (`git checkout -b feature/amazing-optimization`)
3. Commit your changes (`git commit -m 'Add FPS optimization feature'`)
4. Push to the branch (`git push origin feature/amazing-optimization`)
5. Open a Pull Request

Ideas for contributions:
- Additional competitive settings
- New preset configurations
- Steam Deck-specific optimizations
- Performance benchmarking features

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Support & Community

- **Issues & Bug Reports**: [GitHub Issues](https://github.com/aj-geddes/arc-raiders-tuner/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/aj-geddes/arc-raiders-tuner/discussions)
- **Documentation**: [GitHub Pages Site](https://aj-geddes.github.io/arc-raiders-tuner/)

## Keywords & Search Terms

This Arc Raiders configuration tool helps with: graphics settings optimization, FPS boost, performance tuning, DLSS configuration, FSR settings, XeSS setup, NVIDIA Reflex latency reduction, ray tracing optimization, Steam Deck gaming, SteamOS compatibility, competitive settings, input lag reduction, game config editor, INI file manager, Unreal Engine 5 settings, visual clutter reduction, frame generation, upscaling technology comparison.

## Credits

- **High Velocity Solutions LLC** - Development
- **Arc Raiders** is a trademark of Embark Studios AB
- Graphics technologies: DLSS (NVIDIA), FSR (AMD), XeSS (Intel), Reflex (NVIDIA)

## Disclaimer

This is an unofficial tool and is not affiliated with, endorsed by, or connected to Embark Studios AB or Arc Raiders. Use at your own risk. Always keep backups of your configuration files. This tool modifies game configuration files - ensure you understand the changes being made.
