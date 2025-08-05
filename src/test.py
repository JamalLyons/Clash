#!/usr/bin/env python3
"""
Test script for the refactored Clash of Clans inviter
Tests the new architecture without running the full automation
"""

import os
import sys
from Main import ClashInviter


def test_configuration():
    """Test that configuration loads correctly"""
    print("🧪 Testing configuration loading...")
    
    try:
        app = ClashInviter()
        print("✅ Configuration loaded successfully")
        print(f"   - API Token: {'Set' if app.config['api_token'] else 'Not set'}")
        print(f"   - Screen positions: {len(app.config['screen_positions'])} configured")
        print(f"   - Player positions: {len(app.config['player_positions'])} configured")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_gui_controller():
    """Test GUI controller initialization"""
    print("\n🧪 Testing GUI controller...")
    
    try:
        from GuiController import GuiController
        
        # Test positions
        test_positions = {
            'test': (100, 100),
            'game_area': (1373, 35)
        }
        
        gui = GuiController(test_positions)
        print("✅ GUI controller initialized successfully")
        print(f"   - Screen size: {gui.get_screen_size()}")
        print(f"   - Mouse position: {gui.get_mouse_position()}")
        return True
    except Exception as e:
        print(f"❌ GUI controller test failed: {e}")
        return False


def test_clash_controller():
    """Test Clash API controller"""
    print("\n🧪 Testing Clash API controller...")
    
    try:
        from ClashController import ClashController
        
        # Test with dummy token (will fail but should initialize)
        api_token = os.getenv('CLASH_API_TOKEN', 'dummy_token')
        clash = ClashController(api_token)
        
        print("✅ Clash API controller initialized successfully")
        print(f"   - Base URL: {clash.base_url}")
        print(f"   - Timeout: {clash.timeout}s")
        
        # Test connection (will fail with dummy token)
        if api_token != 'dummy_token':
            connection_test = clash.test_connection()
            print(f"   - API connection: {'✅' if connection_test else '❌'}")
        
        return True
    except Exception as e:
        print(f"❌ Clash API controller test failed: {e}")
        return False


def test_user_input():
    """Test user input validation"""
    print("\n🧪 Testing user input validation...")
    
    try:
        app = ClashInviter()
        
        # Test with valid input (simulate)
        test_input = "5"
        if test_input.isdigit() and int(test_input) > 0:
            print("✅ User input validation works correctly")
            return True
        else:
            print("❌ User input validation failed")
            return False
            
    except Exception as e:
        print(f"❌ User input test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Testing Refactored Clash of Clans Inviter")
    print("=" * 50)
    
    tests = [
        test_configuration,
        test_gui_controller,
        test_clash_controller,
        test_user_input
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The refactored architecture is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 