#!/usr/bin/env python3
"""
GUI Controller - Handles all pyautogui operations and screen interactions
Provides a clean API for automating Clash of Clans interface
"""

import time
import pyautogui
import pyperclip as pc
from pynput.keyboard import Key, Controller
from typing import Dict, Tuple, Optional


class GuiController:
    """Handles all GUI automation operations for Clash of Clans"""
    
    def __init__(self, screen_positions: Dict[str, Tuple[int, int]], player_positions: Dict[str, Tuple[int, int]] = None):
        """
        Initialize GUI controller with screen positions
        
        Args:
            screen_positions: Dictionary mapping element names to (x, y) coordinates
            player_positions: Dictionary mapping player numbers to (x, y) coordinates
        """
        self.positions = screen_positions
        self.player_positions = player_positions or {}
        self.keyboard = Controller()
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1  # Small pause between actions
        
        # Image recognition settings
        self.confidence = 0.8
        self.timeout = 10
    
    def click(self, position_name: str, delay: float = 1.0) -> bool:
        """
        Click at a specific position
        
        Args:
            position_name: Name of the position to click
            delay: Delay after clicking
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if position_name not in self.positions:
                print(f"❌ Unknown position: {position_name}")
                return False
            
            x, y = self.positions[position_name]
            pyautogui.click(x, y)
            time.sleep(delay)
            return True
            
        except Exception as e:
            print(f"❌ Error clicking {position_name}: {e}")
            return False
    
    def press_key(self, key: str, delay: float = 1.0) -> bool:
        """
        Press a keyboard key
        
        Args:
            key: Key to press
            delay: Delay after pressing
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.keyboard.press(key)
            self.keyboard.release(key)
            time.sleep(delay)
            return True
            
        except Exception as e:
            print(f"❌ Error pressing key {key}: {e}")
            return False
    
    def press_escape(self, delay: float = 1.0) -> bool:
        """Press escape key"""
        try:
            self.keyboard.press(Key.esc)
            self.keyboard.release(Key.esc)
            time.sleep(delay)
            return True
            
        except Exception as e:
            print(f"❌ Error pressing escape: {e}")
            return False
    
    def find_and_click_image(self, image_path: str, confidence: float = None) -> bool:
        """
        Find and click an image on screen
        
        Args:
            image_path: Path to the image file
            confidence: Confidence level for image recognition
            
        Returns:
            True if found and clicked, False otherwise
        """
        try:
            confidence = confidence or self.confidence
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            
            if location:
                x, y = location
                pyautogui.click(x, y)
                return True
            else:
                print(f"⚠️  Could not find image: {image_path}")
                return False
                
        except Exception as e:
            print(f"❌ Error finding image {image_path}: {e}")
            return False
    
    def navigate_to_member_search(self) -> bool:
        """Navigate to the member search area"""
        try:
            # Click game area
            self.click('game_area')
            
            # Press 'g' key
            self.press_key('g')
            
            # Click my clan
            self.click('my_clan')
            
            # Click find new members
            self.click('find_new_members')
            
            return True
            
        except Exception as e:
            print(f"❌ Error navigating to member search: {e}")
            return False
    
    def select_filter(self, filter_type: str) -> bool:
        """
        Select a specific filter type
        
        Args:
            filter_type: Type of filter ('war', 'league', 'trophy')
        """
        try:
            filter_map = {
                'war': 'filter_wars',
                'league': 'filter_league',
                'trophy': 'filter_trophy'
            }
            
            if filter_type not in filter_map:
                print(f"❌ Unknown filter type: {filter_type}")
                return False
            
            position_name = filter_map[filter_type]
            return self.click(position_name)
            
        except Exception as e:
            print(f"❌ Error selecting filter {filter_type}: {e}")
            return False
    
    def search_players(self) -> bool:
        """Click the search suggested button"""
        return self.click('search_suggested')
    
    def click_player_profile(self, player_num: int) -> bool:
        """
        Click on a specific player profile
        
        Args:
            player_num: Player number (1-5)
        """
        try:
            position_name = str(player_num)
            if position_name not in self.player_positions:
                print(f"❌ Unknown player position: {player_num}")
                return False
            
            x, y = self.player_positions[position_name]
            pyautogui.click(x, y)
            time.sleep(1.5)
            return True
            
        except Exception as e:
            print(f"❌ Error clicking player {player_num}: {e}")
            return False
    
    def get_player_id(self) -> Optional[str]:
        """
        Get player ID from clipboard
        
        Returns:
            Player ID string or None if failed
        """
        try:
            # Click player code area
            self.click('player_code', delay=0.7)
            
            # Click copy button
            self.click('copy')
            
            # Get from clipboard
            player_id = str(pc.paste())
            
            if not player_id or len(player_id) < 2:
                print("⚠️  Invalid player ID from clipboard")
                return None
            
            return player_id
            
        except Exception as e:
            print(f"❌ Error getting player ID: {e}")
            return None
    
    def click_invite_button(self) -> bool:
        """Click the invite button"""
        return self.find_and_click_image('invite.png')
    
    def go_back(self) -> bool:
        """Go back to previous screen"""
        return self.find_and_click_image('back.png')
    
    def exit_screen(self) -> bool:
        """Exit current screen"""
        return self.find_and_click_image('exit.png')
    
    def scroll_to_next_page(self) -> bool:
        """Scroll to the next page of players"""
        try:
            # Move to last player position
            if '5' not in self.player_positions:
                print("❌ Player position '5' not found for scrolling")
                return False
                
            x, y = self.player_positions['5']
            pyautogui.moveTo(x, y)
            time.sleep(1.5)
            
            # Drag to scroll (scaled target position)
            target_x = int(247 * (self.player_positions['5'][0] / 250))  # Scale based on current position
            target_y = int(480 * (self.player_positions['5'][1] / 1002))  # Scale based on current position
            pyautogui.dragTo(target_x, target_y, 2, button='left')
            time.sleep(1.5)
            
            return True
            
        except Exception as e:
            print(f"❌ Error scrolling: {e}")
            return False
    
    def wait_for_image(self, image_path: str, timeout: float = None) -> bool:
        """
        Wait for an image to appear on screen
        
        Args:
            image_path: Path to the image file
            timeout: Timeout in seconds
            
        Returns:
            True if image found, False if timeout
        """
        timeout = timeout or self.timeout
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if pyautogui.locateOnScreen(image_path, confidence=self.confidence):
                    return True
                time.sleep(0.5)
            except Exception:
                time.sleep(0.5)
        
        return False
    
    def is_image_visible(self, image_path: str) -> bool:
        """
        Check if an image is currently visible on screen
        
        Args:
            image_path: Path to the image file
            
        Returns:
            True if image is visible, False otherwise
        """
        try:
            return pyautogui.locateOnScreen(image_path, confidence=self.confidence) is not None
        except Exception:
            return False
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get current screen size"""
        return pyautogui.size()
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position"""
        return pyautogui.position()
    
    def move_mouse(self, x: int, y: int) -> bool:
        """
        Move mouse to specific coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successful, False otherwise
        """
        try:
            pyautogui.moveTo(x, y)
            return True
        except Exception as e:
            print(f"❌ Error moving mouse: {e}")
            return False
