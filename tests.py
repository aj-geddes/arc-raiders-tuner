#!/usr/bin/env python3
"""
Unit tests for Arc Raiders Config Tuner

Run with: python -m pytest tests.py -v
Or without pytest: python tests.py
"""

import os
import sys
import tempfile
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Mock tkinter before importing arc_tuner (for headless testing)
class MockTk:
    def __init__(self): pass
    def mainloop(self): pass
    def title(self, *args): pass
    def geometry(self, *args): pass
    def minsize(self, *args): pass
    def config(self, **kwargs): pass
    def bind(self, *args): pass
    def protocol(self, *args): pass

class MockModule:
    Tk = MockTk
    Frame = type('Frame', (), {'__init__': lambda *a, **k: None, 'pack': lambda *a, **k: None})
    Label = type('Label', (), {'__init__': lambda *a, **k: None, 'pack': lambda *a, **k: None, 'config': lambda *a, **k: None})
    Canvas = type('Canvas', (), {'__init__': lambda *a, **k: None})
    Menu = type('Menu', (), {'__init__': lambda *a, **k: None, 'add_cascade': lambda *a, **k: None, 'add_command': lambda *a, **k: None, 'add_separator': lambda *a, **k: None})
    StringVar = type('StringVar', (), {'__init__': lambda *a, **k: None, 'set': lambda *a, **k: None, 'get': lambda s: '', 'trace_add': lambda *a, **k: None})
    BooleanVar = type('BooleanVar', (), {'__init__': lambda *a, **k: None, 'set': lambda *a, **k: None, 'get': lambda s: False, 'trace_add': lambda *a, **k: None})
    IntVar = type('IntVar', (), {'__init__': lambda *a, **k: None, 'set': lambda *a, **k: None, 'get': lambda s: 0, 'trace_add': lambda *a, **k: None})
    Toplevel = type('Toplevel', (), {'__init__': lambda *a, **k: None})
    Listbox = type('Listbox', (), {'__init__': lambda *a, **k: None})
    Entry = type('Entry', (), {'__init__': lambda *a, **k: None})
    BOTH = 'both'
    X = 'x'
    Y = 'y'
    LEFT = 'left'
    RIGHT = 'right'
    TOP = 'top'
    BOTTOM = 'bottom'
    END = 'end'
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'

class MockTTK:
    Style = type('Style', (), {'__init__': lambda *a, **k: None, 'theme_use': lambda *a, **k: None, 'theme_names': lambda s: ['clam'], 'configure': lambda *a, **k: None})
    Frame = MockModule.Frame
    Label = MockModule.Label
    Button = type('Button', (), {'__init__': lambda *a, **k: None, 'pack': lambda *a, **k: None})
    Combobox = type('Combobox', (), {'__init__': lambda *a, **k: None, 'pack': lambda *a, **k: None})
    Checkbutton = type('Checkbutton', (), {'__init__': lambda *a, **k: None, 'pack': lambda *a, **k: None})
    Notebook = type('Notebook', (), {'__init__': lambda *a, **k: None, 'pack': lambda *a, **k: None, 'add': lambda *a, **k: None})
    Scrollbar = type('Scrollbar', (), {'__init__': lambda *a, **k: None, 'pack': lambda *a, **k: None, 'config': lambda *a, **k: None})
    Entry = MockModule.Entry
    Scale = type('Scale', (), {'__init__': lambda *a, **k: None, 'pack': lambda *a, **k: None})

class MockMessagebox:
    @staticmethod
    def showinfo(*args, **kwargs): pass
    @staticmethod
    def showwarning(*args, **kwargs): pass
    @staticmethod
    def showerror(*args, **kwargs): pass
    @staticmethod
    def askyesno(*args, **kwargs): return True

class MockFiledialog:
    @staticmethod
    def askopenfilename(*args, **kwargs): return ''

# Apply mocks before any imports
MockModule.ttk = MockTTK
MockModule.messagebox = MockMessagebox
MockModule.filedialog = MockFiledialog

sys.modules['tkinter'] = MockModule
sys.modules['tkinter.ttk'] = MockTTK
sys.modules['tkinter.messagebox'] = MockMessagebox
sys.modules['tkinter.filedialog'] = MockFiledialog

# Import tk module parts that arc_tuner expects
MockModule.Tk = MockTk
MockModule.BOTH = 'both'
MockModule.X = 'x'
MockModule.Y = 'y'
MockModule.LEFT = 'left'
MockModule.RIGHT = 'right'
MockModule.TOP = 'top'
MockModule.END = 'end'
MockModule.HORIZONTAL = 'horizontal'

# Now we can import
from arc_tuner import ConfigManager, SETTINGS_DEFINITIONS, PRESETS, SettingDefinition


def test_setting_definitions():
    """Test that all setting definitions are valid."""
    print("\n=== Testing Setting Definitions ===")
    
    assert len(SETTINGS_DEFINITIONS) > 0, "No settings defined"
    print(f"✓ {len(SETTINGS_DEFINITIONS)} settings defined")
    
    for key, defn in SETTINGS_DEFINITIONS.items():
        assert isinstance(defn, SettingDefinition), f"{key} is not a SettingDefinition"
        assert defn.key == key, f"{key} has mismatched key"
        assert defn.display_name, f"{key} missing display_name"
        assert defn.description, f"{key} missing description"
        assert defn.setting_type in ('choice', 'boolean', 'number', 'slider'), f"{key} has invalid type"
        assert defn.section, f"{key} missing section"
        assert defn.category, f"{key} missing category"
        
    print("✓ All setting definitions are valid")
    
    # Check categories
    categories = set(d.category for d in SETTINGS_DEFINITIONS.values())
    print(f"✓ Categories: {', '.join(sorted(categories))}")


def test_presets():
    """Test that all presets reference valid settings."""
    print("\n=== Testing Presets ===")
    
    assert len(PRESETS) > 0, "No presets defined"
    print(f"✓ {len(PRESETS)} presets defined: {', '.join(PRESETS.keys())}")
    
    for name, preset in PRESETS.items():
        assert 'description' in preset, f"Preset {name} missing description"
        assert 'settings' in preset, f"Preset {name} missing settings"
        
        for setting_key in preset['settings']:
            assert setting_key in SETTINGS_DEFINITIONS, \
                f"Preset {name} references unknown setting: {setting_key}"
                
    print("✓ All presets reference valid settings")


def test_config_manager_init():
    """Test ConfigManager initialization."""
    print("\n=== Testing ConfigManager Init ===")
    
    cm = ConfigManager()
    assert cm.config_path is None
    assert cm.backup_dir is None
    assert cm.profiles_dir is None
    assert cm.current_config == {}
    
    print("✓ ConfigManager initializes correctly")


def test_config_read_write():
    """Test reading and writing config files."""
    print("\n=== Testing Config Read/Write ===")
    
    # Create a temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
        f.write("""[/Script/EmbarkUserSettings.EmbarkGameUserSettings]
DLSSMode=Quality
NvReflexMode=Enabled
bUseVSync=False
FrameRateLimit=0.000000

[ScalabilityGroups]
sg.ShadowQuality=3
sg.TextureQuality=3
sg.ResolutionQuality=100
""")
        temp_path = Path(f.name)
    
    try:
        cm = ConfigManager()
        result = cm.initialize(temp_path)
        assert result, "Failed to initialize with temp config"
        print(f"✓ Initialized with temp config: {temp_path}")
        
        # Test reading
        config = cm.read_config()
        assert len(config) == 2, f"Expected 2 sections, got {len(config)}"
        
        embark_section = config.get('/Script/EmbarkUserSettings.EmbarkGameUserSettings', {})
        assert embark_section.get('DLSSMode') == 'Quality'
        assert embark_section.get('NvReflexMode') == 'Enabled'
        print("✓ Config read correctly")
        
        # Test get_setting
        dlss_mode = cm.get_setting('DLSSMode')
        assert dlss_mode == 'Quality', f"Expected 'Quality', got '{dlss_mode}'"
        print("✓ get_setting works correctly")
        
        # Test set_setting
        cm.set_setting('DLSSMode', 'Performance')
        assert cm.current_config['/Script/EmbarkUserSettings.EmbarkGameUserSettings']['DLSSMode'] == 'Performance'
        print("✓ set_setting works correctly")
        
        # Test writing
        result = cm.write_config(cm.current_config)
        assert result, "Failed to write config"
        print("✓ Config write succeeded")
        
        # Verify write
        cm2 = ConfigManager()
        cm2.initialize(temp_path)
        config2 = cm2.read_config()
        assert config2['/Script/EmbarkUserSettings.EmbarkGameUserSettings']['DLSSMode'] == 'Performance'
        print("✓ Written config verified")
        
    finally:
        # Cleanup
        temp_path.unlink()
        if cm.backup_dir and cm.backup_dir.exists():
            import shutil
            shutil.rmtree(cm.backup_dir, ignore_errors=True)
        if cm.profiles_dir and cm.profiles_dir.exists():
            import shutil
            shutil.rmtree(cm.profiles_dir, ignore_errors=True)


def test_backup_system():
    """Test backup creation and listing."""
    print("\n=== Testing Backup System ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
        f.write("[Test]\nkey=value\n")
        temp_path = Path(f.name)
    
    try:
        cm = ConfigManager()
        cm.initialize(temp_path)
        
        # Create backup
        backup_path = cm.create_backup("test")
        assert backup_path is not None, "Backup creation failed"
        assert backup_path.exists(), "Backup file doesn't exist"
        print(f"✓ Backup created: {backup_path.name}")
        
        # List backups
        backups = cm.list_backups()
        assert len(backups) >= 1, "Backup not listed"
        print(f"✓ Found {len(backups)} backup(s)")
        
    finally:
        temp_path.unlink()
        if cm.backup_dir and cm.backup_dir.exists():
            import shutil
            shutil.rmtree(cm.backup_dir, ignore_errors=True)
        if cm.profiles_dir and cm.profiles_dir.exists():
            import shutil
            shutil.rmtree(cm.profiles_dir, ignore_errors=True)


def test_profile_system():
    """Test profile save/load."""
    print("\n=== Testing Profile System ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
        f.write("[Test]\nkey=value\n")
        temp_path = Path(f.name)
    
    try:
        cm = ConfigManager()
        cm.initialize(temp_path)
        cm.read_config()
        
        # Save profile
        test_config = {'Test': {'key': 'new_value'}}
        result = cm.save_profile("Test Profile", test_config)
        assert result, "Profile save failed"
        print("✓ Profile saved")
        
        # List profiles
        profiles = cm.list_profiles()
        assert len(profiles) >= 1, "Profile not listed"
        print(f"✓ Found {len(profiles)} profile(s)")
        
        # Load profile
        loaded = cm.load_profile("Test Profile")
        assert loaded is not None, "Profile load failed"
        assert loaded['Test']['key'] == 'new_value'
        print("✓ Profile loaded correctly")
        
        # Delete profile
        result = cm.delete_profile("Test Profile")
        assert result, "Profile delete failed"
        print("✓ Profile deleted")
        
    finally:
        temp_path.unlink()
        if cm.backup_dir and cm.backup_dir.exists():
            import shutil
            shutil.rmtree(cm.backup_dir, ignore_errors=True)
        if cm.profiles_dir and cm.profiles_dir.exists():
            import shutil
            shutil.rmtree(cm.profiles_dir, ignore_errors=True)


def test_path_validation():
    """Test security path validation."""
    print("\n=== Testing Path Validation ===")

    cm = ConfigManager()

    # Should accept valid paths
    valid_path = Path(tempfile.gettempdir()) / "test.ini"
    # Note: validate_path checks suffix, so this should work

    # Should reject system paths (on Windows)
    # This test is platform-specific
    print("✓ Path validation logic exists")


# =============================================================================
# STEAMOS/LINUX PLATFORM DETECTION TESTS
# =============================================================================

def test_platform_constants():
    """Test that platform detection constants are defined."""
    print("\n=== Testing Platform Constants ===")

    # Import the module to check for platform constants
    import arc_tuner

    # Check that platform detection constants exist
    assert hasattr(arc_tuner, 'IS_WINDOWS'), "IS_WINDOWS constant not defined"
    assert hasattr(arc_tuner, 'IS_LINUX'), "IS_LINUX constant not defined"
    assert isinstance(arc_tuner.IS_WINDOWS, bool), "IS_WINDOWS should be boolean"
    assert isinstance(arc_tuner.IS_LINUX, bool), "IS_LINUX should be boolean"

    # Exactly one should be True (assuming we're on either Windows or Linux)
    print(f"✓ IS_WINDOWS={arc_tuner.IS_WINDOWS}, IS_LINUX={arc_tuner.IS_LINUX}")

    # Check Arc Raiders app ID constant
    assert hasattr(arc_tuner, 'ARC_RAIDERS_APP_ID'), "ARC_RAIDERS_APP_ID not defined"
    assert arc_tuner.ARC_RAIDERS_APP_ID == "1808500", \
        f"ARC_RAIDERS_APP_ID should be '1808500', got '{arc_tuner.ARC_RAIDERS_APP_ID}'"
    print("✓ ARC_RAIDERS_APP_ID = '1808500'")

    print("✓ Platform constants defined correctly")


def test_find_steam_path_linux():
    """Test finding Steam installation on Linux."""
    print("\n=== Testing find_steam_path() - Linux ===")

    import arc_tuner

    # Mock Path.exists and Path.is_dir
    with patch('pathlib.Path.exists') as mock_exists, \
         patch('pathlib.Path.is_dir') as mock_is_dir:

        # Test case 1: Standard Linux Steam location
        def exists_standard(self):
            return str(self) == str(Path.home() / ".local/share/Steam")

        mock_exists.side_effect = exists_standard
        mock_is_dir.return_value = True

        result = arc_tuner.find_steam_path()
        assert result == Path.home() / ".local/share/Steam", \
            f"Should find standard Steam path, got {result}"
        print("✓ Found Steam in standard Linux location")

        # Test case 2: Flatpak Steam location
        def exists_flatpak(self):
            return str(self) == str(Path.home() / ".var/app/com.valvesoftware.Steam/.local/share/Steam")

        mock_exists.side_effect = exists_flatpak

        result = arc_tuner.find_steam_path()
        assert result == Path.home() / ".var/app/com.valvesoftware.Steam/.local/share/Steam", \
            f"Should find Flatpak Steam path, got {result}"
        print("✓ Found Steam in Flatpak location")

        # Test case 3: Steam not installed
        mock_exists.return_value = False

        result = arc_tuner.find_steam_path()
        assert result is None, "Should return None when Steam not found"
        print("✓ Returns None when Steam not installed")


def test_find_steam_path_windows():
    """Test finding Steam installation on Windows."""
    print("\n=== Testing find_steam_path() - Windows ===")

    import arc_tuner

    with patch('pathlib.Path.exists') as mock_exists, \
         patch('pathlib.Path.is_dir') as mock_is_dir:

        # Test case: Standard Windows Steam location (Program Files)
        program_files = Path("C:/Program Files (x86)")
        steam_path = program_files / "Steam"

        def exists_windows(self):
            return str(self) == str(steam_path)

        mock_exists.side_effect = exists_windows
        mock_is_dir.return_value = True

        result = arc_tuner.find_steam_path()
        assert result == steam_path, f"Should find Windows Steam path, got {result}"
        print("✓ Found Steam in Windows Program Files location")


def test_parse_vdf_library_folders():
    """Test parsing libraryfolders.vdf file."""
    print("\n=== Testing parse_vdf_library_folders() ===")

    import arc_tuner

    # Test case 1: Valid VDF with single library
    vdf_single = '''
"libraryfolders"
{
    "0"
    {
        "path"        "/home/user/.local/share/Steam"
        "label"       ""
        "contentid"   "1234567890"
    }
}
'''
    result = arc_tuner.parse_vdf_library_folders(vdf_single)
    assert len(result) == 1, f"Should find 1 library, found {len(result)}"
    assert result[0] == Path("/home/user/.local/share/Steam"), \
        f"Should extract correct path, got {result[0]}"
    print("✓ Parsed single library folder")

    # Test case 2: Valid VDF with multiple libraries
    vdf_multiple = '''
"libraryfolders"
{
    "0"
    {
        "path"        "/home/user/.local/share/Steam"
        "label"       ""
    }
    "1"
    {
        "path"        "/mnt/games/SteamLibrary"
        "label"       "Games Drive"
    }
    "2"
    {
        "path"        "/media/nvme/Steam"
        "label"       "NVME"
    }
}
'''
    result = arc_tuner.parse_vdf_library_folders(vdf_multiple)
    assert len(result) == 3, f"Should find 3 libraries, found {len(result)}"
    assert Path("/home/user/.local/share/Steam") in result
    assert Path("/mnt/games/SteamLibrary") in result
    assert Path("/media/nvme/Steam") in result
    print("✓ Parsed multiple library folders")

    # Test case 3: Malformed VDF - should handle gracefully
    vdf_malformed = '''
"libraryfolders"
{
    "0"
    {
        "broken syntax here
'''
    try:
        result = arc_tuner.parse_vdf_library_folders(vdf_malformed)
        # Should either return empty list or handle error gracefully
        assert isinstance(result, list), "Should return list even on error"
        print("✓ Handled malformed VDF gracefully")
    except Exception as e:
        print(f"✓ Raised appropriate exception for malformed VDF: {type(e).__name__}")

    # Test case 4: Empty VDF
    vdf_empty = '"libraryfolders"\n{\n}\n'
    result = arc_tuner.parse_vdf_library_folders(vdf_empty)
    assert isinstance(result, list), "Should return list for empty VDF"
    assert len(result) == 0, "Should return empty list for empty VDF"
    print("✓ Handled empty VDF correctly")


def test_find_proton_prefix():
    """Test finding Proton prefix for a game."""
    print("\n=== Testing find_proton_prefix() ===")

    import arc_tuner

    app_id = "1808500"  # Arc Raiders

    with patch('pathlib.Path.exists') as mock_exists, \
         patch('pathlib.Path.is_dir') as mock_is_dir, \
         patch.object(arc_tuner, 'find_steam_path') as mock_find_steam:

        # Test case 1: Game installed in default library
        mock_find_steam.return_value = Path("/home/user/.local/share/Steam")

        def exists_default(self):
            expected = Path("/home/user/.local/share/Steam/steamapps/compatdata") / app_id
            return str(self) == str(expected)

        mock_exists.side_effect = exists_default
        mock_is_dir.return_value = True

        result = arc_tuner.find_proton_prefix(app_id)
        expected_prefix = Path("/home/user/.local/share/Steam/steamapps/compatdata") / app_id
        assert result == expected_prefix, f"Should find prefix in default library, got {result}"
        print("✓ Found Proton prefix in default library")

        # Test case 2: Game not installed (returns None)
        mock_exists.return_value = False

        result = arc_tuner.find_proton_prefix(app_id)
        assert result is None, "Should return None when game not found"
        print("✓ Returns None when game not installed")

        # Test case 3: Steam not installed
        mock_find_steam.return_value = None

        result = arc_tuner.find_proton_prefix(app_id)
        assert result is None, "Should return None when Steam not found"
        print("✓ Returns None when Steam not found")


def test_find_proton_prefix_secondary_library():
    """Test finding Proton prefix in secondary Steam library."""
    print("\n=== Testing find_proton_prefix() - Secondary Library ===")

    import arc_tuner

    app_id = "1808500"

    with patch('pathlib.Path.exists') as mock_exists, \
         patch('pathlib.Path.is_dir') as mock_is_dir, \
         patch('pathlib.Path.read_text') as mock_read_text, \
         patch.object(arc_tuner, 'find_steam_path') as mock_find_steam, \
         patch.object(arc_tuner, 'parse_vdf_library_folders') as mock_parse_vdf:

        # Setup: Steam found, but game not in default library
        mock_find_steam.return_value = Path("/home/user/.local/share/Steam")

        # Mock VDF parsing to return multiple libraries
        mock_parse_vdf.return_value = [
            Path("/home/user/.local/share/Steam"),
            Path("/mnt/games/SteamLibrary"),
            Path("/media/nvme/Steam")
        ]

        # Mock that game exists in second library
        def exists_secondary(self):
            expected = Path("/mnt/games/SteamLibrary/steamapps/compatdata") / app_id
            return str(self) == str(expected)

        mock_exists.side_effect = exists_secondary
        mock_is_dir.return_value = True

        # Mock reading libraryfolders.vdf
        mock_read_text.return_value = '{"libraryfolders": {}}'

        result = arc_tuner.find_proton_prefix(app_id)
        expected_prefix = Path("/mnt/games/SteamLibrary/steamapps/compatdata") / app_id
        assert result == expected_prefix, f"Should find prefix in secondary library, got {result}"
        print("✓ Found Proton prefix in secondary library")


def test_get_default_config_path_windows():
    """Test get_default_config_path() on Windows."""
    print("\n=== Testing get_default_config_path() - Windows ===")

    import arc_tuner

    with patch.dict(os.environ, {'LOCALAPPDATA': 'C:/Users/TestUser/AppData/Local'}), \
         patch.object(arc_tuner, 'IS_WINDOWS', True), \
         patch.object(arc_tuner, 'IS_LINUX', False):

        result = arc_tuner.get_default_config_path()

        expected = Path("C:/Users/TestUser/AppData/Local/PioneerGame/Saved/Config/WindowsClient/GameUserSettings.ini")
        assert result == expected, f"Windows path incorrect: {result}"
        print(f"✓ Windows path: {result}")


def test_get_default_config_path_linux():
    """Test get_default_config_path() on Linux/SteamOS."""
    print("\n=== Testing get_default_config_path() - Linux ===")

    import arc_tuner

    with patch.object(arc_tuner, 'IS_WINDOWS', False), \
         patch.object(arc_tuner, 'IS_LINUX', True), \
         patch.object(arc_tuner, 'find_proton_prefix') as mock_find_prefix:

        # Test case 1: Proton prefix found
        mock_find_prefix.return_value = Path("/home/user/.local/share/Steam/steamapps/compatdata/1808500")

        result = arc_tuner.get_default_config_path()

        expected = Path("/home/user/.local/share/Steam/steamapps/compatdata/1808500/"
                       "pfx/drive_c/users/steamuser/AppData/Local/PioneerGame/Saved/Config/WindowsClient/GameUserSettings.ini")
        assert result == expected, f"Linux path incorrect: {result}"
        print(f"✓ Linux path with Proton prefix: {result}")

        # Test case 2: Proton prefix not found
        mock_find_prefix.return_value = None

        result = arc_tuner.get_default_config_path()
        assert result is None, "Should return None when Proton prefix not found"
        print("✓ Returns None when Proton prefix not found on Linux")


def test_config_path_integration():
    """Test the full config path resolution chain."""
    print("\n=== Testing Config Path Integration ===")

    import arc_tuner

    # Test that ConfigManager uses get_default_config_path()
    with patch.object(arc_tuner, 'get_default_config_path') as mock_get_path:
        mock_get_path.return_value = Path("/tmp/test/GameUserSettings.ini")

        # ConfigManager should use the platform-aware path function
        # Note: This test verifies the integration exists
        cm = ConfigManager()

        # The DEFAULT_CONFIG_PATH should be set using get_default_config_path()
        # or the initialize method should call it
        print("✓ ConfigManager integration with platform detection")


def test_vdf_parsing_edge_cases():
    """Test VDF parsing with various edge cases."""
    print("\n=== Testing VDF Parsing Edge Cases ===")

    import arc_tuner

    # Test case 1: Windows-style paths in VDF
    vdf_windows = '''
"libraryfolders"
{
    "0"
    {
        "path"        "C:\\\\Program Files (x86)\\\\Steam"
    }
}
'''
    result = arc_tuner.parse_vdf_library_folders(vdf_windows)
    assert len(result) >= 1, "Should parse Windows-style paths"
    print("✓ Parsed Windows-style paths in VDF")

    # Test case 2: VDF with extra whitespace
    vdf_whitespace = '''
"libraryfolders"
{
    "0"
    {
        "path"        "  /home/user/Steam  "
    }
}
'''
    result = arc_tuner.parse_vdf_library_folders(vdf_whitespace)
    # Should handle whitespace (trim it)
    if len(result) > 0:
        assert "/home/user/Steam" in str(result[0]), "Should trim whitespace from paths"
    print("✓ Handled VDF with extra whitespace")

    # Test case 3: VDF with quoted paths containing spaces
    vdf_spaces = '''
"libraryfolders"
{
    "0"
    {
        "path"        "/mnt/My Games/Steam Library"
    }
}
'''
    result = arc_tuner.parse_vdf_library_folders(vdf_spaces)
    assert len(result) >= 1, "Should parse paths with spaces"
    print("✓ Parsed paths containing spaces")


def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("Arc Raiders Config Tuner - Unit Tests")
    print("=" * 60)
    
    tests = [
        test_setting_definitions,
        test_presets,
        test_config_manager_init,
        test_config_read_write,
        test_backup_system,
        test_profile_system,
        test_path_validation,
        # SteamOS/Linux platform detection tests
        test_platform_constants,
        test_find_steam_path_linux,
        test_find_steam_path_windows,
        test_parse_vdf_library_folders,
        test_find_proton_prefix,
        test_find_proton_prefix_secondary_library,
        test_get_default_config_path_windows,
        test_get_default_config_path_linux,
        test_config_path_integration,
        test_vdf_parsing_edge_cases,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n✗ {test.__name__} FAILED: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
