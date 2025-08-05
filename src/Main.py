#!/usr/bin/env python3
"""
Clash of Clans Clan Member Inviter - Main Entry Point
Handles environment loading, configuration, and program orchestration
"""

import os
import sys
import time
from typing import Dict, Any

from GuiController import GuiController
from ClashController import ClashController
from ScreenController import ScreenController


class ClashInviter:
    """Main orchestrator class that coordinates GUI automation and API calls"""
    
    def __init__(self):
        """Initialize the application with environment validation and configuration"""
        self.config = self._load_config()
        self.gui = GuiController(self.config['screen_positions'], self.config['player_positions'])
        self.clash_api = ClashController(self.config['api_token'])
        self.stats = {
            'invited': 0,
            'target': 0,
            'invited_players': []
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """Load and validate configuration from environment"""
        # Load API token
        api_token = os.getenv('CLASH_API_TOKEN')
        if not api_token:
            print("❌ ERROR: CLASH_API_TOKEN environment variable not set!")
            print("Please set your API token as an environment variable:")
            print("export CLASH_API_TOKEN='your_token_here'")
            print("Or create a .env file with: CLASH_API_TOKEN=your_token_here")
            sys.exit(1)
        
        # Load screen configuration
        screen_controller = ScreenController()
        screen_positions = screen_controller.get_screen_positions()
        player_positions = screen_controller.get_player_positions()
        
        return {
            'api_token': api_token,
            'screen_positions': screen_positions,
            'player_positions': player_positions,
            'failsafe': True,
            'confidence': 0.8,
            'timeout': 10
        }
    
    def get_user_input(self) -> int:
        """Get and validate user input for number of players to invite"""
        while True:
            try:
                count = input('Number of players to invite: ')
                if not count.isdigit() or int(count) <= 0:
                    print("❌ Please enter a valid positive number!")
                    continue
                return int(count)
            except KeyboardInterrupt:
                print("\n⚠️  Script interrupted by user")
                sys.exit(0)
    
    def run(self):
        """Main execution loop"""
        try:
            # Get user input
            self.stats['target'] = self.get_user_input()
            print(f"🎯 Target: {self.stats['target']} players")
            
            # Wait for user to focus BlueStacks
            print("⏳ Please focus on BlueStacks window in 8 seconds...")
            time.sleep(8)
            
            # Main execution loop
            for cycle in range(100):  # Safety limit
                for filter_type in ['war', 'league', 'trophy']:
                    if self.stats['invited'] >= self.stats['target']:
                        print("🎉 [FINISHED] All players invited!")
                        return
                    
                    print(f"🔄 Processing {filter_type} filter...")
                    self._process_filter(filter_type)
            
        except KeyboardInterrupt:
            print("\n⚠️  Script interrupted by user")
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            sys.exit(1)
    
    def _process_filter(self, filter_type: str):
        """Process a specific filter type (war, league, trophy)"""
        try:
            # Navigate to member search
            self.gui.navigate_to_member_search()
            
            # Select filter
            self.gui.select_filter(filter_type)
            
            # Search for players
            self.gui.search_players()
            
            # Process player invitations
            self._invite_players()
            
        except Exception as e:
            print(f"❌ Error processing {filter_type} filter: {e}")
    
    def _invite_players(self):
        """Process player invitations for current filter"""
        for page in range(12):  # Process 12 pages
            for player_num in range(1, 6):  # 5 players per page
                if self.stats['invited'] >= self.stats['target']:
                    return
                
                try:
                    # Click on player profile
                    self.gui.click_player_profile(player_num)
                    time.sleep(2)
                    
                    # Check if player meets criteria
                    if self._evaluate_player():
                        self._invite_current_player()
                    
                    # Go back to player list
                    self.gui.go_back()
                    
                except Exception as e:
                    print(f"❌ Error processing player {player_num}: {e}")
                    continue
            
            # Scroll to next page
            self.gui.scroll_to_next_page()
    
    def _evaluate_player(self) -> bool:
        """Evaluate if current player meets invitation criteria"""
        try:
            # Get player ID from clipboard
            player_id = self.gui.get_player_id()
            if not player_id:
                return False
            
            # Get player data from API
            player_data = self.clash_api.get_player_info(player_id)
            if not player_data:
                return False
            
            # Apply filters
            if not self._check_clan_filter(player_data):
                return False
            
            if not self._check_level_filter(player_data):
                return False
            
            # Player passed all filters
            self.stats['invited_players'].append(player_data.get('name', 'Unknown'))
            return True
            
        except Exception as e:
            print(f"❌ Error evaluating player: {e}")
            return False
    
    def _check_clan_filter(self, player_data: Dict) -> bool:
        """Check if player passes clan filter (no clan or very short name)"""
        try:
            clan = player_data.get('clan')
            if clan:
                name = clan.get('name', '')
                if len(name) > 1:
                    return False
        except Exception as e:
            print(f"⚠️  Error in clan filter: {e}")
        return True
    
    def _check_level_filter(self, player_data: Dict) -> bool:
        """Check if player meets level requirements"""
        try:
            th = player_data.get('townHallLevel', 0)
            level = player_data.get('expLevel', 0)
            
            # Level requirements by town hall
            requirements = {
                8: 65,
                9: 75,
                10: 85,
                11: 100
            }
            
            if th in requirements:
                return level >= requirements[th]
            elif th > 11:
                return level >= 120
            
            return False
            
        except Exception as e:
            print(f"❌ Error in level filter: {e}")
            return False
    
    def _invite_current_player(self):
        """Invite the currently selected player"""
        try:
            self.gui.click_invite_button()
            self.stats['invited'] += 1
            print(f"✅ [invited] {self.stats['invited']}/{self.stats['target']}")
            
        except Exception as e:
            print(f"⚠️  Could not invite player: {e}")


def main():
    """Main entry point"""
    try:
        app = ClashInviter()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
