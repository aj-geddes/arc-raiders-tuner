# Arc Raiders Config Tuner

A secure, user-friendly configuration manager for Arc Raiders. Easily tune your graphics settings, manage multiple profiles, and never lose your configs with automatic backups.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)

## Features

- **Easy-to-Use Interface** - All settings explained with performance impact indicators
- **Automatic Backups** - Never lose your settings, backups created before every save
- **Multiple Profiles** - Save and load different configurations for competitive, quality, etc.
- **Built-in Presets** - One-click presets for common use cases
- **Secure** - No network access, validates all file paths, no code execution
- **Zero Dependencies** - Single .exe that works without installing anything

## Screenshots

```
┌─────────────────────────────────────────────────────────────────┐
│ Arc Raiders Config Tuner                                    [_][□][X]│
├─────────────────────────────────────────────────────────────────┤
│ File  Profiles  Backups  Presets  Help                          │
├─────────────────────────────────────────────────────────────────┤
│ Loaded: C:\...\GameUserSettings.ini           ● Unsaved Changes │
├─────────────────────────────────────────────────────────────────┤
│ [Upscaling] [Frame Gen] [Latency] [Ray Tracing] [Display] ...   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Upscaling Technology                    [Very High Impact]     │
│  Choose which upscaling technology to use.     [DLSS      ▼]    │
│                                                                 │
│  DLSS Quality Mode                       [Very High Impact]     │
│  DLAA=Native AA only. Quality=67%...          [Quality    ▼]    │
│                                                                 │
│  DLSS Model                              [Low Impact]           │
│  Transformer provides better motion clarity.   [Transformer▼]   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│              [Reset to Defaults] [Reload] [Save Changes]        │
└─────────────────────────────────────────────────────────────────┘
```

## Installation

### Option 1: Download Pre-built Executable (Recommended)
1. Download `ArcRaidersTuner.exe` from the Releases page
2. Run it - no installation required!

### Option 2: Run from Source
```bash
# Clone or download this repository
git clone https://github.com/yourusername/arc-raiders-tuner.git
cd arc-raiders-tuner

# Run directly (requires Python 3.8+)
python arc_tuner.py
```

### Option 3: Build Your Own Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build (Windows)
build.bat

# Or manually:
pyinstaller --onefile --windowed --name "ArcRaidersTuner" arc_tuner.py
```

## Usage

### First Launch
1. Run `ArcRaidersTuner.exe`
2. The app automatically finds your Arc Raiders config at:
   ```
   %LOCALAPPDATA%\ArcRaiders\Saved\Config\Windows\GameUserSettings.ini
   ```
3. If not found, use **File → Open Config** to locate it manually

### Changing Settings
1. Navigate tabs (Upscaling, Latency, Ray Tracing, etc.)
2. Adjust settings using dropdowns, checkboxes, and sliders
3. Each setting shows its **performance impact** (Low/Medium/High/Very High)
4. Click **Save Changes** when done
5. A backup is automatically created before saving

### Using Presets
Quick-apply optimized configurations:
- **Competitive** - Maximum FPS, lowest latency
- **Balanced** - Good visuals with solid performance  
- **Quality** - Maximum visual fidelity
- **Cinematic** - Best visuals with frame generation

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

## Settings Reference

### Upscaling Technologies

| Technology | Vendor | Best For |
|------------|--------|----------|
| **DLSS** | NVIDIA | RTX GPUs - Best quality with Tensor cores |
| **XeSS** | Intel | All GPUs - Best on Intel Arc |
| **FSR 3** | AMD | All GPUs - No special hardware needed |

### DLSS Modes

| Mode | Render Scale | FPS Gain | Quality |
|------|-------------|----------|---------|
| DLAA | 100% | 0% | Sharpest (AA only) |
| Quality | 67% | 30-50% | Excellent |
| Balanced | 58% | 45-65% | Good |
| Performance | 50% | 60-100% | Acceptable |
| Ultra Performance | 33% | 100%+ | Blurry |

### Latency Reduction

| Setting | Effect |
|---------|--------|
| **Reflex On** | 20-50% latency reduction |
| **Reflex On+Boost** | Better for CPU-bound scenarios |
| **Frame Generation** | ⚠️ Adds 15-30ms latency! |

### RTX Global Illumination

| Setting | Performance Cost | Use Case |
|---------|-----------------|----------|
| Static | 0% | Competitive - Best FPS |
| DynamicHigh | 25-35% | Balanced |
| DynamicEpic | 35-45% | Quality - Best visuals |

## Security

This application is designed with security in mind:

- ✅ **No network access** - Works completely offline
- ✅ **No code execution** - Only reads/writes INI files
- ✅ **Path validation** - Prevents directory traversal attacks
- ✅ **No elevation required** - Runs as standard user
- ✅ **Open source** - Full source code available for review

## File Locations

| Item | Location |
|------|----------|
| Game Config | `%LOCALAPPDATA%\ArcRaiders\Saved\Config\Windows\GameUserSettings.ini` |
| Backups | `%LOCALAPPDATA%\ArcRaiders\Saved\Config\Windows\ArcTuner_Backups\` |
| Profiles | `%LOCALAPPDATA%\ArcRaiders\Saved\Config\Windows\ArcTuner_Profiles\` |

## Troubleshooting

### "Config Not Found"
- Make sure Arc Raiders has been run at least once
- Use **File → Open Config** to manually locate the file

### Settings Not Applying
1. Close Arc Raiders completely before saving
2. Disable cloud saves for Arc Raiders in your game launcher
3. Check if the file is read-only

### Backup/Profile Errors
- Ensure you have write permissions to the config folder
- Run as Administrator if needed (not recommended normally)

## Building from Source

Requirements:
- Python 3.8 or higher
- Windows 10/11

```bash
# Install build dependencies
pip install pyinstaller

# Build standalone executable
pyinstaller --onefile --windowed --name "ArcRaidersTuner" arc_tuner.py

# The .exe will be in the dist/ folder
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Credits

- **High Velocity Solutions LLC** - Development
- **Arc Raiders** is a trademark of Embark Studios

## Disclaimer

This is an unofficial tool and is not affiliated with, endorsed by, or connected to Embark Studios or Arc Raiders. Use at your own risk. Always keep backups of your configuration files.
