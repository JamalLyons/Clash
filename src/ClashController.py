#!/usr/bin/env python3
"""
Clash API Controller - Handles all HTTP requests to Clash of Clans API
Provides a clean API for fetching player and clan information
"""

import requests
import json
from typing import Dict, Optional, List
from datetime import datetime


class ClashController:
    """Handles all API interactions with Clash of Clans"""
    
    def __init__(self, api_token: str):
        """
        Initialize Clash API controller
        
        Args:
            api_token: Clash of Clans API token
        """
        self.api_token = api_token
        self.base_url = "https://api.clashofclans.com/v1"
        self.headers = {
            'Accept': 'application/json',
            'authorization': f'Bearer {api_token}'
        }
        self.timeout = 10
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        Make a request to the Clash of Clans API
        
        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            
        Returns:
            Response data as dictionary or None if failed
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(
                url, 
                headers=self.headers, 
                params=params,
                timeout=self.timeout
            )
            
            # Update rate limit info
            self.rate_limit_remaining = response.headers.get('X-Ratelimit-Remaining')
            self.rate_limit_reset = response.headers.get('X-Ratelimit-Reset')
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("⚠️  Rate limit exceeded. Waiting before retry...")
                return None
            else:
                print(f"❌ API request failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ API request timed out")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ API request error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected API error: {e}")
            return None
    
    def get_player_info(self, player_tag: str) -> Optional[Dict]:
        """
        Get detailed information about a player
        
        Args:
            player_tag: Player tag (with or without #)
            
        Returns:
            Player information dictionary or None if failed
        """
        # Ensure player tag starts with #
        if not player_tag.startswith('#'):
            player_tag = f"#{player_tag}"
        
        endpoint = f"/players/{player_tag}"
        return self._make_request(endpoint)
    
    def get_clan_info(self, clan_tag: str) -> Optional[Dict]:
        """
        Get detailed information about a clan
        
        Args:
            clan_tag: Clan tag (with or without #)
            
        Returns:
            Clan information dictionary or None if failed
        """
        # Ensure clan tag starts with #
        if not clan_tag.startswith('#'):
            clan_tag = f"#{clan_tag}"
        
        endpoint = f"/clans/{clan_tag}"
        return self._make_request(endpoint)
    
    def get_clan_members(self, clan_tag: str) -> Optional[List[Dict]]:
        """
        Get list of clan members
        
        Args:
            clan_tag: Clan tag (with or without #)
            
        Returns:
            List of clan members or None if failed
        """
        # Ensure clan tag starts with #
        if not clan_tag.startswith('#'):
            clan_tag = f"#{clan_tag}"
        
        endpoint = f"/clans/{clan_tag}/members"
        response = self._make_request(endpoint)
        
        if response and 'items' in response:
            return response['items']
        return None
    
    def search_clans(self, name: str = None, war_frequency: str = None, 
                    min_members: int = None, max_members: int = None,
                    min_clan_points: int = None, min_clan_level: int = None,
                    limit: int = 20) -> Optional[List[Dict]]:
        """
        Search for clans based on criteria
        
        Args:
            name: Clan name to search for
            war_frequency: War frequency filter
            min_members: Minimum number of members
            max_members: Maximum number of members
            min_clan_points: Minimum clan points
            min_clan_level: Minimum clan level
            limit: Number of results to return
            
        Returns:
            List of matching clans or None if failed
        """
        params = {'limit': limit}
        
        if name:
            params['name'] = name
        if war_frequency:
            params['warFrequency'] = war_frequency
        if min_members:
            params['minMembers'] = min_members
        if max_members:
            params['maxMembers'] = max_members
        if min_clan_points:
            params['minClanPoints'] = min_clan_points
        if min_clan_level:
            params['minClanLevel'] = min_clan_level
        
        endpoint = "/clans"
        response = self._make_request(endpoint, params)
        
        if response and 'items' in response:
            return response['items']
        return None
    
    def get_player_achievements(self, player_tag: str) -> Optional[List[Dict]]:
        """
        Get player achievements
        
        Args:
            player_tag: Player tag (with or without #)
            
        Returns:
            List of achievements or None if failed
        """
        # Ensure player tag starts with #
        if not player_tag.startswith('#'):
            player_tag = f"#{player_tag}"
        
        endpoint = f"/players/{player_tag}"
        response = self._make_request(endpoint)
        
        if response and 'achievements' in response:
            return response['achievements']
        return None
    
    def get_player_troops(self, player_tag: str) -> Optional[List[Dict]]:
        """
        Get player troops information
        
        Args:
            player_tag: Player tag (with or without #)
            
        Returns:
            List of troops or None if failed
        """
        # Ensure player tag starts with #
        if not player_tag.startswith('#'):
            player_tag = f"#{player_tag}"
        
        endpoint = f"/players/{player_tag}"
        response = self._make_request(endpoint)
        
        if response and 'troops' in response:
            return response['troops']
        return None
    
    def get_player_heroes(self, player_tag: str) -> Optional[List[Dict]]:
        """
        Get player heroes information
        
        Args:
            player_tag: Player tag (with or without #)
            
        Returns:
            List of heroes or None if failed
        """
        # Ensure player tag starts with #
        if not player_tag.startswith('#'):
            player_tag = f"#{player_tag}"
        
        endpoint = f"/players/{player_tag}"
        response = self._make_request(endpoint)
        
        if response and 'heroes' in response:
            return response['heroes']
        return None
    
    def get_player_spells(self, player_tag: str) -> Optional[List[Dict]]:
        """
        Get player spells information
        
        Args:
            player_tag: Player tag (with or without #)
            
        Returns:
            List of spells or None if failed
        """
        # Ensure player tag starts with #
        if not player_tag.startswith('#'):
            player_tag = f"#{player_tag}"
        
        endpoint = f"/players/{player_tag}"
        response = self._make_request(endpoint)
        
        if response and 'spells' in response:
            return response['spells']
        return None
    
    def validate_player(self, player_data: Dict) -> Dict[str, bool]:
        """
        Validate player data against common criteria
        
        Args:
            player_data: Player information dictionary
            
        Returns:
            Dictionary with validation results
        """
        validation = {
            'has_clan': False,
            'meets_level_requirements': False,
            'meets_townhall_requirements': False,
            'is_active': False
        }
        
        try:
            # Check if player has a clan
            validation['has_clan'] = 'clan' in player_data and player_data['clan'] is not None
            
            # Check level requirements
            level = player_data.get('expLevel', 0)
            validation['meets_level_requirements'] = level >= 50  # Minimum level
            
            # Check town hall requirements
            town_hall = player_data.get('townHallLevel', 0)
            validation['meets_townhall_requirements'] = town_hall >= 8  # Minimum TH8
            
            # Check if player is active (last seen within 30 days)
            last_seen = player_data.get('lastSeen')
            if last_seen:
                try:
                    last_seen_date = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
                    days_since_active = (datetime.now().astimezone() - last_seen_date).days
                    validation['is_active'] = days_since_active <= 30
                except:
                    validation['is_active'] = True  # Assume active if can't parse date
            
        except Exception as e:
            print(f"⚠️  Error validating player: {e}")
        
        return validation
    
    def get_rate_limit_info(self) -> Dict[str, Optional[str]]:
        """
        Get current rate limit information
        
        Returns:
            Dictionary with rate limit info
        """
        return {
            'remaining': self.rate_limit_remaining,
            'reset': self.rate_limit_reset
        }
    
    def test_connection(self) -> bool:
        """
        Test API connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try to get a simple endpoint
            response = self._make_request("/locations")
            return response is not None
        except Exception as e:
            print(f"❌ API connection test failed: {e}")
            return False
    
    def get_locations(self) -> Optional[List[Dict]]:
        """
        Get available locations (countries)
        
        Returns:
            List of locations or None if failed
        """
        endpoint = "/locations"
        response = self._make_request(endpoint)
        
        if response and 'items' in response:
            return response['items']
        return None
    
    def get_league_seasons(self) -> Optional[List[Dict]]:
        """
        Get available league seasons
        
        Returns:
            List of league seasons or None if failed
        """
        endpoint = "/leagues/29000022/seasons"
        response = self._make_request(endpoint)
        
        if response and 'items' in response:
            return response['items']
        return None
