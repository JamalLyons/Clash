#!/usr/bin/env python3
"""
Screen Configuration Module
Handles screen size detection and position mapping for different resolutions
"""

import pyautogui
from typing import Dict, Tuple, Optional


class ScreenController:
    """Manages screen configuration and position mapping for different resolutions"""
    
    # Screen resolutions and their position mappings
    SCREEN_PRESETS = {
        # 1920x1080 (windows)
        (1920, 1080): {
            'game_area': (1373, 35),
            'my_clan': (809, 66),
            'find_new_members': (516, 733),
            'filter_wars': (396, 298),
            'filter_league': (802, 296),
            'filter_trophy': (1249, 301),
            'search_suggested': (1548, 426),
            'player_area': (253, 501),
            'player_code': (757, 286),
            'copy': (946, 300),
            'player_positions': {
                '1': (252, 525),
                '2': (251, 637),
                '3': (253, 768),
                '4': (249, 897),
                '5': (250, 1002),
            }
        },
        
        # 1512x982 (macbook)
        (1512, 982): {
            'game_area': (1080, 32),
            'my_clan': (636, 60),
            'find_new_members': (405, 666),
            'filter_wars': (311, 271),
            'filter_league': (630, 269),
            'filter_trophy': (981, 273),
            'search_suggested': (1215, 387),
            'player_area': (199, 456),
            'player_code': (594, 260),
            'copy': (743, 273),
            'player_positions': {
                '1': (198, 477),
                '2': (197, 578),
                '3': (199, 696),
                '4': (196, 814),
                '5': (197, 911),
            }
        }
    }
    
    def __init__(self):
        """Initialize screen configuration"""
        self.current_resolution = self._get_current_resolution()
        self.positions = self._load_positions()
    
    def _get_current_resolution(self) -> Tuple[int, int]:
        """Get current screen resolution"""
        try:
            width, height = pyautogui.size()
            print(f"🖥️  Detected screen resolution: {width}x{height}")
            return (width, height)
        except Exception as e:
            print(f"❌ Error detecting screen resolution: {e}")
            return (1920, 1080)  # Default fallback
    
    def _load_positions(self) -> Dict:
        """Load screen positions for current resolution"""
        # Check if we have a preset for current resolution
        if self.current_resolution in self.SCREEN_PRESETS:
            print(f"✅ Using preset configuration for {self.current_resolution[0]}x{self.current_resolution[1]}")
            return self.SCREEN_PRESETS[self.current_resolution]
        
        # If no preset, try to scale from 1920x1080
        print(f"⚠️  No preset found for {self.current_resolution[0]}x{self.current_resolution[1]}, scaling from 1920x1080")
        return self._scale_positions()
    
    def _scale_positions(self) -> Dict:
        """Scale positions from 1920x1080 to current resolution"""
        base_resolution = (1920, 1080)
        base_positions = self.SCREEN_PRESETS[base_resolution]
        
        scale_x = self.current_resolution[0] / base_resolution[0]
        scale_y = self.current_resolution[1] / base_resolution[1]
        
        scaled_positions = {}
        
        for key, value in base_positions.items():
            if key == 'player_positions':
                scaled_positions[key] = {}
                for player_key, player_pos in value.items():
                    scaled_positions[key][player_key] = (
                        int(player_pos[0] * scale_x),
                        int(player_pos[1] * scale_y)
                    )
            else:
                scaled_positions[key] = (
                    int(value[0] * scale_x),
                    int(value[1] * scale_y)
                )
        
        return scaled_positions
    
    def get_positions(self) -> Dict:
        """Get current screen positions"""
        return self.positions
    
    def get_player_positions(self) -> Dict:
        """Get player position mappings"""
        return self.positions.get('player_positions', {})
    
    def get_screen_positions(self) -> Dict:
        """Get screen element positions (excluding player positions)"""
        screen_positions = {}
        for key, value in self.positions.items():
            if key != 'player_positions':
                screen_positions[key] = value
        return screen_positions
    
    def list_available_presets(self) -> list:
        """List all available screen presets"""
        return list(self.SCREEN_PRESETS.keys())
    
    def set_resolution_preset(self, resolution: Tuple[int, int]) -> bool:
        """
        Manually set a resolution preset
        
        Args:
            resolution: Tuple of (width, height)
            
        Returns:
            True if preset exists and was set, False otherwise
        """
        if resolution in self.SCREEN_PRESETS:
            self.current_resolution = resolution
            self.positions = self.SCREEN_PRESETS[resolution]
            print(f"✅ Set resolution preset to {resolution[0]}x{resolution[1]}")
            return True
        else:
            print(f"❌ No preset found for {resolution[0]}x{resolution[1]}")
            return False
    
    def test_positions(self) -> bool:
        """Test if current positions are valid"""
        try:
            # Test a few key positions
            test_positions = ['game_area', 'my_clan', 'find_new_members']
            
            for pos_name in test_positions:
                if pos_name not in self.positions:
                    print(f"❌ Missing position: {pos_name}")
                    return False
                
                x, y = self.positions[pos_name]
                if x < 0 or y < 0 or x > self.current_resolution[0] or y > self.current_resolution[1]:
                    print(f"❌ Position {pos_name} ({x}, {y}) is outside screen bounds")
                    return False
            
            print("✅ All positions are valid")
            return True
            
        except Exception as e:
            print(f"❌ Error testing positions: {e}")
            return False
    
    def print_current_config(self):
        """Print current screen configuration"""
        print(f"\n📱 Current Screen Configuration:")
        print(f"   Resolution: {self.current_resolution[0]}x{self.current_resolution[1]}")
        print(f"   Screen positions: {len(self.get_screen_positions())} elements")
        print(f"   Player positions: {len(self.get_player_positions())} slots")
        
        print(f"\n📍 Key Positions:")
        for key, value in self.get_screen_positions().items():
            print(f"   {key}: {value}")
        
        print(f"\n👥 Player Positions:")
        for key, value in self.get_player_positions().items():
            print(f"   Player {key}: {value}")


def create_screen_controller() -> ScreenController:
    """Factory function to create screen controller"""
    return ScreenController()


if __name__ == "__main__":
    # Test the screen controller
    controller = ScreenController()
    controller.print_current_config()
    
    print(f"\n📋 Available Presets:")
    for resolution in controller.list_available_presets():
        print(f"   {resolution[0]}x{resolution[1]}")
    
    print(f"\n🧪 Testing positions...")
    controller.test_positions() 