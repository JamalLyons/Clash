#!/usr/bin/env python3
"""
Test script for screen configuration
Tests the screen configuration with the user's Mac resolution
"""

import sys
from ScreenController import ScreenController


def test_screen_controller():
    """Test the screen controller"""
    print("🧪 Testing Screen Controller")
    print("=" * 40)
    
    try:
        # Create screen controller
        controller = ScreenController()
        
        # Print current configuration
        controller.print_current_config()
        
        # Test positions
        print(f"\n🧪 Testing positions...")
        if controller.test_positions():
            print("✅ All positions are valid!")
        else:
            print("❌ Some positions are invalid!")
        
        # List available presets
        print(f"\n📋 Available Presets:")
        for resolution in controller.list_available_presets():
            print(f"   {resolution[0]}x{resolution[1]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing screen controller: {e}")
        return False


def test_gui_controller_integration():
    """Test GUI controller with screen controller"""
    print(f"\n🧪 Testing GUI Controller Integration")
    print("=" * 40)
    
    try:
        from GuiController import GuiController
        
        controller = ScreenController()
        screen_positions = controller.get_screen_positions()
        player_positions = controller.get_player_positions()
        
        gui = GuiController(screen_positions, player_positions)
        
        print("✅ GUI Controller initialized with screen controller")
        print(f"   - Screen positions: {len(screen_positions)}")
        print(f"   - Player positions: {len(player_positions)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing GUI controller integration: {e}")
        return False


def main():
    """Run all tests"""
    tests = [
        test_screen_controller,
        test_gui_controller_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Screen configuration is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 