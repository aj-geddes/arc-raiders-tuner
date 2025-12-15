#!/usr/bin/env python3
"""
Arc Raiders Config Tuner
A secure, user-friendly configuration manager for Arc Raiders.

Author: High Velocity Solutions LLC
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import configparser
import os
import shutil
import json
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION DEFINITIONS
# =============================================================================

@dataclass
class SettingDefinition:
    """Defines a configuration setting with metadata."""
    key: str
    display_name: str
    description: str
    setting_type: str  # 'choice', 'boolean', 'number', 'slider'
    section: str
    category: str
    options: list = field(default_factory=list)  # For choice type
    min_val: float = 0  # For number/slider
    max_val: float = 100  # For number/slider
    default: Any = None
    performance_impact: str = "Low"  # Low, Medium, High, Very High


# All settings definitions with explanations
SETTINGS_DEFINITIONS = {
    # === UPSCALING ===
    "ResolutionScalingMethod": SettingDefinition(
        key="ResolutionScalingMethod",
        display_name="Upscaling Technology",
        description="Choose which upscaling technology to use. DLSS (NVIDIA), XeSS (Intel), FSR (AMD), or None.",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Upscaling",
        options=["DLSS", "XeSS", "FSR3", "None"],
        default="DLSS",
        performance_impact="Very High"
    ),
    "DLSSMode": SettingDefinition(
        key="DLSSMode",
        display_name="DLSS Quality Mode",
        description="DLAA=Native AA only (sharpest, slowest). Quality=67% render (balanced). "
                   "Balanced=58% (good FPS). Performance=50% (high FPS). Ultra Performance=33% (maximum FPS, blurry).",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Upscaling",
        options=["DLAA", "Quality", "Balanced", "Performance", "UltraPerformance"],
        default="Quality",
        performance_impact="Very High"
    ),
    "DLSSModel": SettingDefinition(
        key="DLSSModel",
        display_name="DLSS Model",
        description="Transformer (DLSS 4) provides better motion clarity and less ghosting. "
                   "CNN is the older model with slightly better performance but more artifacts.",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Upscaling",
        options=["Transformer", "CNN"],
        default="Transformer",
        performance_impact="Low"
    ),
    "XeSSMode": SettingDefinition(
        key="XeSSMode",
        display_name="XeSS Quality Mode",
        description="Intel XeSS upscaling quality. Higher quality = lower performance.",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Upscaling",
        options=["NativeAA", "UltraQualityPlus", "UltraQuality", "Quality", "Balanced", "Performance", "UltraPerformance"],
        default="Quality",
        performance_impact="Very High"
    ),
    "FSR3Mode": SettingDefinition(
        key="FSR3Mode",
        display_name="FSR 3 Quality Mode",
        description="AMD FSR upscaling quality. Works on all GPUs.",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Upscaling",
        options=["NativeAA", "Quality", "Balanced", "Performance", "UltraPerformance"],
        default="Balanced",
        performance_impact="Very High"
    ),
    
    # === FRAME GENERATION ===
    "DLSSFrameGenerationMode": SettingDefinition(
        key="DLSSFrameGenerationMode",
        display_name="DLSS Frame Generation",
        description="AI generates extra frames for smoother visuals. WARNING: Adds 15-30ms input latency! "
                   "On2X=Double FPS. Off recommended for competitive play.",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Frame Generation",
        options=["Off", "On", "On2X", "On3X", "On4X"],
        default="Off",
        performance_impact="Very High"
    ),
    "FSR3FrameGenerationMode": SettingDefinition(
        key="FSR3FrameGenerationMode",
        display_name="FSR 3 Frame Generation",
        description="AMD frame generation. Works on all GPUs but adds latency.",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Frame Generation",
        options=["Off", "On"],
        default="Off",
        performance_impact="Very High"
    ),
    
    # === LATENCY ===
    "NvReflexMode": SettingDefinition(
        key="NvReflexMode",
        display_name="NVIDIA Reflex",
        description="Reduces input latency by 20-50%. Enabled=Standard mode. "
                   "Enabled+Boost=Keeps GPU clocks high (better for CPU-bound scenarios).",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Latency",
        options=["Disabled", "Enabled", "Enabled+Boost"],
        default="Enabled",
        performance_impact="Low"
    ),
    "ReflexLatewarpMode": SettingDefinition(
        key="ReflexLatewarpMode",
        display_name="Reflex Frame Warp",
        description="Reflex 2 feature that warps frames at display time. Can reduce latency by additional 50%. "
                   "May cause visual artifacts in some scenarios.",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Latency",
        options=["Off", "On"],
        default="Off",
        performance_impact="Low"
    ),
    "bAntiLag2Enabled": SettingDefinition(
        key="bAntiLag2Enabled",
        display_name="AMD Anti-Lag 2",
        description="AMD's latency reduction. Only works on AMD RDNA GPUs.",
        setting_type="boolean",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Latency",
        default=True,
        performance_impact="Low"
    ),
    
    # === RAY TRACING ===
    "RTXGIQuality": SettingDefinition(
        key="RTXGIQuality",
        display_name="RTX Global Illumination",
        description="Ray-traced indirect lighting. Static=Off (best performance). "
                   "DynamicEpic=Highest quality but 25-45% performance cost!",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Ray Tracing",
        options=["Static", "DynamicLow", "DynamicMedium", "DynamicHigh", "DynamicEpic"],
        default="DynamicHigh",
        performance_impact="Very High"
    ),
    "RTXGIResolutionQuality": SettingDefinition(
        key="RTXGIResolutionQuality",
        display_name="RTX GI Resolution",
        description="Resolution of global illumination calculations. 0=Low, 3=Epic.",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Ray Tracing",
        options=[("0", "Low"), ("1", "Medium"), ("2", "High"), ("3", "Epic")],
        default="3",
        performance_impact="High"
    ),
    
    # === DISPLAY ===
    "FullscreenMode": SettingDefinition(
        key="FullscreenMode",
        display_name="Fullscreen Mode",
        description="Exclusive=Lowest latency but slow Alt+Tab. Borderless=Seamless windows integration. "
                   "Windowed=Window mode.",
        setting_type="choice",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Display",
        options=[("0", "Exclusive Fullscreen"), ("1", "Borderless Windowed"), ("2", "Windowed")],
        default="1",
        performance_impact="Low"
    ),
    "bUseVSync": SettingDefinition(
        key="bUseVSync",
        display_name="VSync",
        description="Synchronizes frames to monitor refresh. OFF recommended with Reflex for lowest latency.",
        setting_type="boolean",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Display",
        default=False,
        performance_impact="Medium"
    ),
    "FrameRateLimit": SettingDefinition(
        key="FrameRateLimit",
        display_name="Frame Rate Limit",
        description="0=Unlimited. Set slightly below monitor refresh for G-Sync/FreeSync.",
        setting_type="number",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Display",
        min_val=0,
        max_val=500,
        default=0,
        performance_impact="Medium"
    ),
    "bUseHDRDisplayOutput": SettingDefinition(
        key="bUseHDRDisplayOutput",
        display_name="HDR Output",
        description="Enable HDR if your monitor supports it. Provides wider color range and brightness.",
        setting_type="boolean",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Display",
        default=False,
        performance_impact="Low"
    ),
    
    # === VISUAL EFFECTS ===
    "MotionBlurEnabled": SettingDefinition(
        key="MotionBlurEnabled",
        display_name="Motion Blur",
        description="Blurs fast-moving objects. OFF recommended for competitive play.",
        setting_type="boolean",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Visual Effects",
        default=False,
        performance_impact="Low"
    ),
    "LensDistortionEnabled": SettingDefinition(
        key="LensDistortionEnabled",
        display_name="Lens Distortion",
        description="Simulates camera lens curvature. OFF for clearer image edges.",
        setting_type="boolean",
        section="/Script/EmbarkUserSettings.EmbarkGameUserSettings",
        category="Visual Effects",
        default=False,
        performance_impact="Low"
    ),
    
    # === SCALABILITY GROUPS ===
    "sg.ViewDistanceQuality": SettingDefinition(
        key="sg.ViewDistanceQuality",
        display_name="View Distance",
        description="How far objects render before LOD/culling. Higher=see farther, more GPU load.",
        setting_type="choice",
        section="ScalabilityGroups",
        category="Quality Settings",
        options=[("0", "Low"), ("1", "Medium"), ("2", "High"), ("3", "Epic"), ("4", "Cinematic")],
        default="3",
        performance_impact="Medium"
    ),
    "sg.ShadowQuality": SettingDefinition(
        key="sg.ShadowQuality",
        display_name="Shadow Quality",
        description="Shadow resolution and filtering. 0=512px, 3=4096px shadows.",
        setting_type="choice",
        section="ScalabilityGroups",
        category="Quality Settings",
        options=[("0", "Low"), ("1", "Medium"), ("2", "High"), ("3", "Epic")],
        default="3",
        performance_impact="High"
    ),
    "sg.TextureQuality": SettingDefinition(
        key="sg.TextureQuality",
        display_name="Texture Quality",
        description="Texture resolution. Affects VRAM usage more than FPS.",
        setting_type="choice",
        section="ScalabilityGroups",
        category="Quality Settings",
        options=[("0", "Low"), ("1", "Medium"), ("2", "High"), ("3", "Epic")],
        default="3",
        performance_impact="Low"
    ),
    "sg.EffectsQuality": SettingDefinition(
        key="sg.EffectsQuality",
        display_name="Effects Quality",
        description="Particle counts, explosions, physics debris complexity.",
        setting_type="choice",
        section="ScalabilityGroups",
        category="Quality Settings",
        options=[("0", "Low"), ("1", "Medium"), ("2", "High"), ("3", "Epic")],
        default="3",
        performance_impact="Medium"
    ),
    "sg.FoliageQuality": SettingDefinition(
        key="sg.FoliageQuality",
        display_name="Foliage Quality",
        description="Grass/tree density. Low=Sparse vegetation (competitive advantage). Epic=Lush environments.",
        setting_type="choice",
        section="ScalabilityGroups",
        category="Quality Settings",
        options=[("0", "Low"), ("1", "Medium"), ("2", "High"), ("3", "Epic")],
        default="3",
        performance_impact="High"
    ),
    "sg.PostProcessQuality": SettingDefinition(
        key="sg.PostProcessQuality",
        display_name="Post Processing",
        description="Bloom, lens flares, color grading, depth of field.",
        setting_type="choice",
        section="ScalabilityGroups",
        category="Quality Settings",
        options=[("0", "Low"), ("1", "Medium"), ("2", "High"), ("3", "Epic")],
        default="3",
        performance_impact="Low"
    ),
    "sg.ReflectionQuality": SettingDefinition(
        key="sg.ReflectionQuality",
        display_name="Reflection Quality",
        description="Screen-space reflections and reflection probe quality.",
        setting_type="choice",
        section="ScalabilityGroups",
        category="Quality Settings",
        options=[("0", "Low"), ("1", "Medium"), ("2", "High"), ("3", "Epic")],
        default="3",
        performance_impact="Medium"
    ),
    "sg.ShadingQuality": SettingDefinition(
        key="sg.ShadingQuality",
        display_name="Shading Quality",
        description="Material complexity, subsurface scattering for skin/hair.",
        setting_type="choice",
        section="ScalabilityGroups",
        category="Quality Settings",
        options=[("0", "Low"), ("1", "Medium"), ("2", "High"), ("3", "Epic")],
        default="3",
        performance_impact="Medium"
    ),
    "sg.GlobalIlluminationQuality": SettingDefinition(
        key="sg.GlobalIlluminationQuality",
        display_name="Global Illumination",
        description="Indirect lighting quality (non-RTX fallback).",
        setting_type="choice",
        section="ScalabilityGroups",
        category="Quality Settings",
        options=[("0", "Low"), ("1", "Medium"), ("2", "High"), ("3", "Epic")],
        default="3",
        performance_impact="Medium"
    ),
    "sg.AntiAliasingQuality": SettingDefinition(
        key="sg.AntiAliasingQuality",
        display_name="Anti-Aliasing Quality",
        description="TAA sample count. Often overridden by DLSS/XeSS/FSR.",
        setting_type="choice",
        section="ScalabilityGroups",
        category="Quality Settings",
        options=[("0", "Low"), ("1", "Medium"), ("2", "High"), ("3", "Epic")],
        default="3",
        performance_impact="Low"
    ),
    "sg.ResolutionQuality": SettingDefinition(
        key="sg.ResolutionQuality",
        display_name="Resolution Scale %",
        description="Internal render resolution percentage. Usually controlled by upscaler.",
        setting_type="slider",
        section="ScalabilityGroups",
        category="Quality Settings",
        min_val=25,
        max_val=100,
        default=100,
        performance_impact="Very High"
    ),
}

# Preset configurations
PRESETS = {
    "Competitive": {
        "description": "Maximum FPS and lowest latency for competitive play",
        "settings": {
            "DLSSMode": "Performance",
            "DLSSFrameGenerationMode": "Off",
            "NvReflexMode": "Enabled+Boost",
            "RTXGIQuality": "Static",
            "RTXGIResolutionQuality": "0",
            "FullscreenMode": "0",
            "bUseVSync": "False",
            "MotionBlurEnabled": "False",
            "LensDistortionEnabled": "False",
            "sg.FoliageQuality": "0",
            "sg.ShadowQuality": "1",
            "sg.EffectsQuality": "1",
            "sg.PostProcessQuality": "1",
            "sg.ViewDistanceQuality": "3",
        }
    },
    "Balanced": {
        "description": "Good visuals with solid performance",
        "settings": {
            "DLSSMode": "Quality",
            "DLSSFrameGenerationMode": "Off",
            "NvReflexMode": "Enabled",
            "RTXGIQuality": "DynamicHigh",
            "RTXGIResolutionQuality": "2",
            "FullscreenMode": "1",
            "bUseVSync": "False",
            "MotionBlurEnabled": "False",
            "LensDistortionEnabled": "False",
            "sg.FoliageQuality": "2",
            "sg.ShadowQuality": "2",
            "sg.EffectsQuality": "2",
            "sg.PostProcessQuality": "2",
            "sg.ViewDistanceQuality": "3",
        }
    },
    "Quality": {
        "description": "Maximum visual quality",
        "settings": {
            "DLSSMode": "DLAA",
            "DLSSFrameGenerationMode": "Off",
            "NvReflexMode": "Enabled",
            "RTXGIQuality": "DynamicEpic",
            "RTXGIResolutionQuality": "3",
            "FullscreenMode": "1",
            "bUseVSync": "False",
            "MotionBlurEnabled": "False",
            "LensDistortionEnabled": "True",
            "sg.FoliageQuality": "3",
            "sg.ShadowQuality": "3",
            "sg.EffectsQuality": "3",
            "sg.PostProcessQuality": "3",
            "sg.ViewDistanceQuality": "4",
        }
    },
    "Cinematic": {
        "description": "Best visuals with frame generation for smooth playback",
        "settings": {
            "DLSSMode": "DLAA",
            "DLSSFrameGenerationMode": "On2X",
            "NvReflexMode": "Enabled+Boost",
            "RTXGIQuality": "DynamicEpic",
            "RTXGIResolutionQuality": "3",
            "FullscreenMode": "1",
            "bUseVSync": "False",
            "MotionBlurEnabled": "True",
            "LensDistortionEnabled": "True",
            "sg.FoliageQuality": "3",
            "sg.ShadowQuality": "3",
            "sg.EffectsQuality": "3",
            "sg.PostProcessQuality": "3",
            "sg.ViewDistanceQuality": "4",
        }
    },
}


# =============================================================================
# CONFIG MANAGER
# =============================================================================

class ConfigManager:
    """Handles reading, writing, and backing up Arc Raiders configuration files."""
    
    # Default config path - Arc Raiders uses standard UE5 location
    DEFAULT_CONFIG_PATH = Path(os.environ.get('LOCALAPPDATA', '')) / "ArcRaiders" / "Saved" / "Config" / "Windows" / "GameUserSettings.ini"
    
    def __init__(self):
        self.config_path: Optional[Path] = None
        self.backup_dir: Optional[Path] = None
        self.profiles_dir: Optional[Path] = None
        self.current_config: Dict[str, Dict[str, str]] = {}
        
    def initialize(self, config_path: Optional[Path] = None) -> bool:
        """Initialize the config manager with paths."""
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = self.DEFAULT_CONFIG_PATH
            
        if not self.config_path.exists():
            logger.warning(f"Config file not found at {self.config_path}")
            return False
            
        # Set up backup and profiles directories next to the config
        self.backup_dir = self.config_path.parent / "ArcTuner_Backups"
        self.profiles_dir = self.config_path.parent / "ArcTuner_Profiles"
        
        # Create directories
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
        return True
    
    def validate_path(self, path: Path) -> bool:
        """Security: Validate that a path is safe to use."""
        try:
            # Resolve to absolute path
            resolved = path.resolve()
            
            # Check it's not trying to escape to system directories
            forbidden_paths = [
                Path("C:/Windows"),
                Path("C:/Program Files"),
                Path("C:/Program Files (x86)"),
                Path("/etc"),
                Path("/usr"),
                Path("/bin"),
            ]
            
            for forbidden in forbidden_paths:
                if forbidden.exists():
                    try:
                        resolved.relative_to(forbidden.resolve())
                        logger.error(f"Attempted access to forbidden path: {path}")
                        return False
                    except ValueError:
                        pass  # Not a subpath, which is good
                        
            # Must have .ini extension for config files
            if path.suffix.lower() not in ['.ini', '.json', '']:
                logger.error(f"Invalid file extension: {path}")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Path validation error: {e}")
            return False
    
    def read_config(self) -> Dict[str, Dict[str, str]]:
        """Read the configuration file."""
        if not self.config_path or not self.config_path.exists():
            raise FileNotFoundError("Config file not found")
            
        config = {}
        current_section = None
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                    
                # Section header
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    if current_section not in config:
                        config[current_section] = {}
                    continue
                    
                # Key=Value pair
                if '=' in line and current_section:
                    key, _, value = line.partition('=')
                    config[current_section][key.strip()] = value.strip()
                    
        self.current_config = config
        return config
    
    def write_config(self, config: Dict[str, Dict[str, str]]) -> bool:
        """Write configuration to file."""
        if not self.config_path:
            raise ValueError("Config path not set")
            
        if not self.validate_path(self.config_path):
            raise ValueError("Invalid config path")
            
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                for section, values in config.items():
                    f.write(f"[{section}]\n")
                    for key, value in values.items():
                        f.write(f"{key}={value}\n")
                    f.write("\n")
                    
            self.current_config = config
            return True
        except Exception as e:
            logger.error(f"Failed to write config: {e}")
            return False
    
    def create_backup(self, tag: str = "") -> Optional[Path]:
        """Create a timestamped backup of the current config."""
        if not self.config_path or not self.config_path.exists():
            return None
            
        if not self.backup_dir:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tag_suffix = f"_{tag}" if tag else ""
        backup_name = f"GameUserSettings_{timestamp}{tag_suffix}.ini"
        backup_path = self.backup_dir / backup_name
        
        try:
            shutil.copy2(self.config_path, backup_path)
            logger.info(f"Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return None
    
    def list_backups(self) -> list:
        """List available backup files."""
        if not self.backup_dir or not self.backup_dir.exists():
            return []
            
        backups = []
        for f in self.backup_dir.glob("GameUserSettings_*.ini"):
            stat = f.stat()
            backups.append({
                'path': f,
                'name': f.name,
                'date': datetime.fromtimestamp(stat.st_mtime),
                'size': stat.st_size
            })
            
        return sorted(backups, key=lambda x: x['date'], reverse=True)
    
    def restore_backup(self, backup_path: Path) -> bool:
        """Restore a backup file."""
        if not backup_path.exists():
            return False
            
        if not self.validate_path(backup_path):
            return False
            
        # Create a backup of current before restoring
        self.create_backup("pre_restore")
        
        try:
            shutil.copy2(backup_path, self.config_path)
            logger.info(f"Restored backup: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False
    
    def save_profile(self, name: str, config: Dict[str, Dict[str, str]]) -> bool:
        """Save current settings as a named profile."""
        if not self.profiles_dir:
            return False
            
        # Sanitize profile name
        safe_name = re.sub(r'[^\w\-]', '_', name)
        profile_path = self.profiles_dir / f"{safe_name}.json"
        
        if not self.validate_path(profile_path):
            return False
            
        try:
            profile_data = {
                'name': name,
                'created': datetime.now().isoformat(),
                'config': config
            }
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2)
            logger.info(f"Profile saved: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to save profile: {e}")
            return False
    
    def load_profile(self, name: str) -> Optional[Dict[str, Dict[str, str]]]:
        """Load a named profile."""
        if not self.profiles_dir:
            return None
            
        safe_name = re.sub(r'[^\w\-]', '_', name)
        profile_path = self.profiles_dir / f"{safe_name}.json"
        
        if not profile_path.exists():
            return None
            
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('config')
        except Exception as e:
            logger.error(f"Failed to load profile: {e}")
            return None
    
    def list_profiles(self) -> list:
        """List available profiles."""
        if not self.profiles_dir or not self.profiles_dir.exists():
            return []
            
        profiles = []
        for f in self.profiles_dir.glob("*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    profiles.append({
                        'path': f,
                        'name': data.get('name', f.stem),
                        'created': data.get('created', 'Unknown')
                    })
            except Exception:
                pass
                
        return profiles
    
    def delete_profile(self, name: str) -> bool:
        """Delete a profile."""
        if not self.profiles_dir:
            return False
            
        safe_name = re.sub(r'[^\w\-]', '_', name)
        profile_path = self.profiles_dir / f"{safe_name}.json"
        
        if profile_path.exists():
            try:
                profile_path.unlink()
                return True
            except Exception as e:
                logger.error(f"Failed to delete profile: {e}")
                
        return False
    
    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting value from current config."""
        definition = SETTINGS_DEFINITIONS.get(key)
        if not definition:
            return None
            
        section_config = self.current_config.get(definition.section, {})
        
        # Handle sg. prefix for scalability groups
        if key.startswith("sg."):
            return section_config.get(key, str(definition.default))
        else:
            return section_config.get(key, str(definition.default))
    
    def set_setting(self, key: str, value: str) -> bool:
        """Set a setting value in current config."""
        definition = SETTINGS_DEFINITIONS.get(key)
        if not definition:
            return False
            
        if definition.section not in self.current_config:
            self.current_config[definition.section] = {}
            
        self.current_config[definition.section][key] = value
        return True


# =============================================================================
# GUI APPLICATION
# =============================================================================

class ArcTunerApp:
    """Main application window."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Arc Raiders Config Tuner")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set icon if available
        try:
            # Would set icon here if we had one
            pass
        except Exception:
            pass
            
        self.config_manager = ConfigManager()
        self.setting_widgets: Dict[str, Any] = {}
        self.unsaved_changes = False
        
        self._create_styles()
        self._create_menu()
        self._create_ui()
        self._bind_events()
        
        # Try to auto-detect config
        self._auto_detect_config()
        
    def _create_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        
        # Use a modern theme if available
        available_themes = style.theme_names()
        if 'vista' in available_themes:
            style.theme_use('vista')
        elif 'clam' in available_themes:
            style.theme_use('clam')
            
        # Custom styles
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
        style.configure('Description.TLabel', font=('Segoe UI', 9), foreground='#666666')
        style.configure('Impact.High.TLabel', foreground='#cc0000')
        style.configure('Impact.Medium.TLabel', foreground='#cc6600')
        style.configure('Impact.Low.TLabel', foreground='#006600')
        style.configure('Impact.VeryHigh.TLabel', foreground='#990000', font=('Segoe UI', 9, 'bold'))
        
    def _create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Config...", command=self._browse_config, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self._save_config, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)
        
        # Profiles menu
        profile_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Profiles", menu=profile_menu)
        profile_menu.add_command(label="Save Profile...", command=self._save_profile_dialog)
        profile_menu.add_command(label="Load Profile...", command=self._load_profile_dialog)
        profile_menu.add_command(label="Manage Profiles...", command=self._manage_profiles_dialog)
        
        # Backups menu
        backup_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Backups", menu=backup_menu)
        backup_menu.add_command(label="Create Backup", command=self._create_backup)
        backup_menu.add_command(label="Restore Backup...", command=self._restore_backup_dialog)
        backup_menu.add_command(label="Open Backup Folder", command=self._open_backup_folder)
        
        # Presets menu
        preset_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Presets", menu=preset_menu)
        for preset_name, preset_data in PRESETS.items():
            preset_menu.add_command(
                label=f"{preset_name} - {preset_data['description']}", 
                command=lambda n=preset_name: self._apply_preset(n)
            )
            
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        
    def _create_ui(self):
        """Create the main UI."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar at top
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.status_label = ttk.Label(self.status_frame, text="No config loaded")
        self.status_label.pack(side=tk.LEFT)
        
        self.changes_label = ttk.Label(self.status_frame, text="")
        self.changes_label.pack(side=tk.RIGHT)
        
        # Notebook for categories
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs by category
        categories = {}
        for key, definition in SETTINGS_DEFINITIONS.items():
            if definition.category not in categories:
                categories[definition.category] = []
            categories[definition.category].append(definition)
            
        for category, settings in categories.items():
            self._create_category_tab(category, settings)
            
        # Bottom button bar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save Changes", command=self._save_config).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Reload", command=self._reload_config).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self._reset_to_defaults).pack(side=tk.RIGHT, padx=5)
        
    def _create_category_tab(self, category: str, settings: list):
        """Create a tab for a settings category."""
        # Create scrollable frame
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=category)
        
        # Canvas for scrolling
        canvas = tk.Canvas(tab_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Add settings
        for i, definition in enumerate(settings):
            self._create_setting_widget(scrollable_frame, definition, i)
            
    def _create_setting_widget(self, parent: ttk.Frame, definition: SettingDefinition, row: int):
        """Create a widget for a single setting."""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.X, pady=2)
        
        # Left side: label and description
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Setting name with performance impact indicator
        name_frame = ttk.Frame(left_frame)
        name_frame.pack(fill=tk.X)
        
        ttk.Label(name_frame, text=definition.display_name, style='Header.TLabel').pack(side=tk.LEFT)
        
        impact_style = f'Impact.{"VeryHigh" if definition.performance_impact == "Very High" else definition.performance_impact}.TLabel'
        impact_text = f" [{definition.performance_impact} Impact]"
        ttk.Label(name_frame, text=impact_text, style=impact_style).pack(side=tk.LEFT, padx=(10, 0))
        
        # Description
        desc_label = ttk.Label(left_frame, text=definition.description, style='Description.TLabel', wraplength=500)
        desc_label.pack(fill=tk.X)
        
        # Right side: control widget
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        widget = None
        var = None
        
        if definition.setting_type == "choice":
            var = tk.StringVar()
            
            # Handle options that are tuples (value, display_name)
            if definition.options and isinstance(definition.options[0], tuple):
                values = [opt[1] for opt in definition.options]
                value_map = {opt[1]: opt[0] for opt in definition.options}
                reverse_map = {opt[0]: opt[1] for opt in definition.options}
            else:
                values = definition.options
                value_map = {v: v for v in values}
                reverse_map = value_map
                
            widget = ttk.Combobox(right_frame, textvariable=var, values=values, state="readonly", width=20)
            widget.pack()
            
            # Store maps for value conversion
            widget._value_map = value_map
            widget._reverse_map = reverse_map
            var.trace_add('write', lambda *args, k=definition.key: self._on_setting_changed(k))
            
        elif definition.setting_type == "boolean":
            var = tk.BooleanVar()
            widget = ttk.Checkbutton(right_frame, variable=var, text="Enabled")
            widget.pack()
            var.trace_add('write', lambda *args, k=definition.key: self._on_setting_changed(k))
            
        elif definition.setting_type == "number":
            var = tk.StringVar()
            widget = ttk.Entry(right_frame, textvariable=var, width=10)
            widget.pack()
            var.trace_add('write', lambda *args, k=definition.key: self._on_setting_changed(k))
            
        elif definition.setting_type == "slider":
            var = tk.IntVar()
            slider_frame = ttk.Frame(right_frame)
            slider_frame.pack()
            
            widget = ttk.Scale(
                slider_frame, 
                from_=definition.min_val, 
                to=definition.max_val, 
                variable=var,
                orient=tk.HORIZONTAL,
                length=150
            )
            widget.pack(side=tk.LEFT)
            
            value_label = ttk.Label(slider_frame, textvariable=var, width=5)
            value_label.pack(side=tk.LEFT, padx=(5, 0))
            
            var.trace_add('write', lambda *args, k=definition.key: self._on_setting_changed(k))
            
        if widget and var:
            self.setting_widgets[definition.key] = {
                'widget': widget,
                'var': var,
                'definition': definition
            }
            
    def _bind_events(self):
        """Bind keyboard and window events."""
        self.root.bind('<Control-o>', lambda e: self._browse_config())
        self.root.bind('<Control-s>', lambda e: self._save_config())
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
    def _auto_detect_config(self):
        """Try to auto-detect the config file location."""
        if self.config_manager.initialize():
            self._load_config()
        else:
            messagebox.showinfo(
                "Config Not Found",
                "Arc Raiders config not found at the default location.\n"
                "Please use File > Open Config to locate your GameUserSettings.ini"
            )
            
    def _browse_config(self):
        """Open file browser to select config."""
        initial_dir = Path(os.environ.get('LOCALAPPDATA', ''))
        
        filepath = filedialog.askopenfilename(
            title="Select GameUserSettings.ini",
            initialdir=initial_dir,
            filetypes=[("INI files", "*.ini"), ("All files", "*.*")]
        )
        
        if filepath:
            if self.config_manager.initialize(Path(filepath)):
                self._load_config()
            else:
                messagebox.showerror("Error", "Failed to load config file")
                
    def _load_config(self):
        """Load and display config values."""
        try:
            config = self.config_manager.read_config()
            
            for key, widget_data in self.setting_widgets.items():
                value = self.config_manager.get_setting(key)
                if value is None:
                    continue
                    
                var = widget_data['var']
                widget = widget_data['widget']
                definition = widget_data['definition']
                
                if definition.setting_type == "choice":
                    # Convert stored value to display value
                    if hasattr(widget, '_reverse_map'):
                        display_value = widget._reverse_map.get(value, value)
                        var.set(display_value)
                    else:
                        var.set(value)
                        
                elif definition.setting_type == "boolean":
                    var.set(value.lower() == 'true')
                    
                elif definition.setting_type in ("number", "slider"):
                    try:
                        if definition.setting_type == "slider":
                            var.set(int(float(value)))
                        else:
                            var.set(value)
                    except ValueError:
                        var.set(str(definition.default))
                        
            self.status_label.config(text=f"Loaded: {self.config_manager.config_path}")
            self.unsaved_changes = False
            self._update_changes_label()
            
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            messagebox.showerror("Error", f"Failed to load config: {e}")
            
    def _save_config(self):
        """Save current settings to config file."""
        if not self.config_manager.config_path:
            messagebox.showerror("Error", "No config file loaded")
            return
            
        # Create backup before saving
        backup = self.config_manager.create_backup("pre_save")
        if backup:
            logger.info(f"Backup created before save: {backup}")
            
        # Update config with current widget values
        for key, widget_data in self.setting_widgets.items():
            var = widget_data['var']
            widget = widget_data['widget']
            definition = widget_data['definition']
            
            if definition.setting_type == "choice":
                display_value = var.get()
                if hasattr(widget, '_value_map'):
                    value = widget._value_map.get(display_value, display_value)
                else:
                    value = display_value
            elif definition.setting_type == "boolean":
                value = "True" if var.get() else "False"
            else:
                value = str(var.get())
                
            self.config_manager.set_setting(key, value)
            
        # Write to file
        if self.config_manager.write_config(self.config_manager.current_config):
            self.unsaved_changes = False
            self._update_changes_label()
            messagebox.showinfo("Saved", "Configuration saved successfully!\n\nA backup was created automatically.")
        else:
            messagebox.showerror("Error", "Failed to save configuration")
            
    def _reload_config(self):
        """Reload config from file."""
        if self.unsaved_changes:
            if not messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Reload anyway?"):
                return
        self._load_config()
        
    def _reset_to_defaults(self):
        """Reset all settings to defaults."""
        if not messagebox.askyesno("Reset", "Reset all settings to defaults?"):
            return
            
        for key, widget_data in self.setting_widgets.items():
            var = widget_data['var']
            widget = widget_data['widget']
            definition = widget_data['definition']
            
            if definition.setting_type == "choice":
                if hasattr(widget, '_reverse_map'):
                    display_value = widget._reverse_map.get(str(definition.default), str(definition.default))
                    var.set(display_value)
                else:
                    var.set(str(definition.default))
            elif definition.setting_type == "boolean":
                var.set(definition.default)
            else:
                var.set(str(definition.default))
                
    def _on_setting_changed(self, key: str):
        """Called when a setting value changes."""
        self.unsaved_changes = True
        self._update_changes_label()
        
    def _update_changes_label(self):
        """Update the unsaved changes indicator."""
        if self.unsaved_changes:
            self.changes_label.config(text="● Unsaved Changes", foreground='#cc0000')
        else:
            self.changes_label.config(text="✓ Saved", foreground='#006600')
            
    def _apply_preset(self, preset_name: str):
        """Apply a preset configuration."""
        preset = PRESETS.get(preset_name)
        if not preset:
            return
            
        if not messagebox.askyesno("Apply Preset", f"Apply '{preset_name}' preset?\n\n{preset['description']}"):
            return
            
        for key, value in preset['settings'].items():
            if key in self.setting_widgets:
                widget_data = self.setting_widgets[key]
                var = widget_data['var']
                widget = widget_data['widget']
                definition = widget_data['definition']
                
                if definition.setting_type == "choice":
                    if hasattr(widget, '_reverse_map'):
                        display_value = widget._reverse_map.get(value, value)
                        var.set(display_value)
                    else:
                        var.set(value)
                elif definition.setting_type == "boolean":
                    var.set(value.lower() == 'true')
                else:
                    var.set(value)
                    
        self.unsaved_changes = True
        self._update_changes_label()
        
    def _create_backup(self):
        """Create a manual backup."""
        backup = self.config_manager.create_backup("manual")
        if backup:
            messagebox.showinfo("Backup Created", f"Backup saved to:\n{backup}")
        else:
            messagebox.showerror("Error", "Failed to create backup")
            
    def _restore_backup_dialog(self):
        """Show dialog to restore a backup."""
        backups = self.config_manager.list_backups()
        if not backups:
            messagebox.showinfo("No Backups", "No backup files found")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Restore Backup")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select a backup to restore:", padding=10).pack()
        
        # Listbox with backups
        listbox_frame = ttk.Frame(dialog)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        backup_paths = []
        for backup in backups:
            listbox.insert(tk.END, f"{backup['name']} ({backup['date'].strftime('%Y-%m-%d %H:%M')})")
            backup_paths.append(backup['path'])
            
        def restore_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a backup")
                return
                
            idx = selection[0]
            if messagebox.askyesno("Confirm", f"Restore '{backup_paths[idx].name}'?"):
                if self.config_manager.restore_backup(backup_paths[idx]):
                    self._load_config()
                    dialog.destroy()
                    messagebox.showinfo("Restored", "Backup restored successfully")
                else:
                    messagebox.showerror("Error", "Failed to restore backup")
                    
        ttk.Button(dialog, text="Restore Selected", command=restore_selected).pack(pady=10)
        
    def _open_backup_folder(self):
        """Open the backup folder in file explorer."""
        if self.config_manager.backup_dir and self.config_manager.backup_dir.exists():
            os.startfile(self.config_manager.backup_dir)
        else:
            messagebox.showwarning("Not Found", "Backup folder not found")
            
    def _save_profile_dialog(self):
        """Show dialog to save current settings as a profile."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Save Profile")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Profile Name:", padding=10).pack()
        
        name_var = tk.StringVar()
        entry = ttk.Entry(dialog, textvariable=name_var, width=40)
        entry.pack(padx=20)
        entry.focus()
        
        def save():
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning("Invalid Name", "Please enter a profile name")
                return
                
            # Update config with current values first
            for key, widget_data in self.setting_widgets.items():
                var = widget_data['var']
                widget = widget_data['widget']
                definition = widget_data['definition']
                
                if definition.setting_type == "choice":
                    display_value = var.get()
                    if hasattr(widget, '_value_map'):
                        value = widget._value_map.get(display_value, display_value)
                    else:
                        value = display_value
                elif definition.setting_type == "boolean":
                    value = "True" if var.get() else "False"
                else:
                    value = str(var.get())
                    
                self.config_manager.set_setting(key, value)
                
            if self.config_manager.save_profile(name, self.config_manager.current_config):
                dialog.destroy()
                messagebox.showinfo("Saved", f"Profile '{name}' saved successfully")
            else:
                messagebox.showerror("Error", "Failed to save profile")
                
        ttk.Button(dialog, text="Save", command=save).pack(pady=20)
        
    def _load_profile_dialog(self):
        """Show dialog to load a profile."""
        profiles = self.config_manager.list_profiles()
        if not profiles:
            messagebox.showinfo("No Profiles", "No saved profiles found")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Load Profile")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select a profile to load:", padding=10).pack()
        
        listbox_frame = ttk.Frame(dialog)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        profile_names = []
        for profile in profiles:
            listbox.insert(tk.END, profile['name'])
            profile_names.append(profile['name'])
            
        def load_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a profile")
                return
                
            name = profile_names[selection[0]]
            config = self.config_manager.load_profile(name)
            
            if config:
                self.config_manager.current_config = config
                
                # Update widgets
                for key, widget_data in self.setting_widgets.items():
                    value = self.config_manager.get_setting(key)
                    if value is None:
                        continue
                        
                    var = widget_data['var']
                    widget = widget_data['widget']
                    definition = widget_data['definition']
                    
                    if definition.setting_type == "choice":
                        if hasattr(widget, '_reverse_map'):
                            display_value = widget._reverse_map.get(value, value)
                            var.set(display_value)
                        else:
                            var.set(value)
                    elif definition.setting_type == "boolean":
                        var.set(value.lower() == 'true')
                    elif definition.setting_type in ("number", "slider"):
                        try:
                            if definition.setting_type == "slider":
                                var.set(int(float(value)))
                            else:
                                var.set(value)
                        except ValueError:
                            pass
                            
                self.unsaved_changes = True
                self._update_changes_label()
                dialog.destroy()
                messagebox.showinfo("Loaded", f"Profile '{name}' loaded.\n\nRemember to Save to apply to game.")
            else:
                messagebox.showerror("Error", "Failed to load profile")
                
        ttk.Button(dialog, text="Load Selected", command=load_selected).pack(pady=10)
        
    def _manage_profiles_dialog(self):
        """Show dialog to manage profiles."""
        profiles = self.config_manager.list_profiles()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Profiles")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Saved Profiles:", padding=10).pack()
        
        listbox_frame = ttk.Frame(dialog)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        profile_names = []
        for profile in profiles:
            listbox.insert(tk.END, f"{profile['name']} ({profile['created'][:10] if len(profile['created']) > 10 else profile['created']})")
            profile_names.append(profile['name'])
            
        def delete_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a profile")
                return
                
            name = profile_names[selection[0]]
            if messagebox.askyesno("Delete Profile", f"Delete profile '{name}'?"):
                if self.config_manager.delete_profile(name):
                    listbox.delete(selection[0])
                    profile_names.pop(selection[0])
                else:
                    messagebox.showerror("Error", "Failed to delete profile")
                    
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Delete Selected", command=delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def _show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About Arc Raiders Config Tuner",
            "Arc Raiders Config Tuner v1.0\n\n"
            "A secure configuration manager for Arc Raiders.\n\n"
            "Features:\n"
            "• Easy-to-use settings editor\n"
            "• Automatic backups\n"
            "• Multiple profile support\n"
            "• Built-in presets\n\n"
            "© 2025 High Velocity Solutions LLC"
        )
        
    def _on_close(self):
        """Handle window close."""
        if self.unsaved_changes:
            if messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Exit anyway?"):
                self.root.destroy()
        else:
            self.root.destroy()
            
    def run(self):
        """Start the application."""
        self.root.mainloop()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Application entry point."""
    app = ArcTunerApp()
    app.run()


if __name__ == "__main__":
    main()
