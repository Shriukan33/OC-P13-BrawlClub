import os
import requests


class BrawlAPi:

    def __init__(self) -> None:
        self.base_url = "https://api.brawlstars.com/v1/"
        self.api_key = os.environ.get("BRAWLSTARS_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }

    def get_player_stats(self, player_tag: str) -> dict:
        # We remove the # from the player tag
        player_tag = player_tag[1:]
        url = f"{self.base_url}players/%23{player_tag}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_player_battlelog(self, player_tag: str) -> dict:
        """Get data from the player's last 24 matches"""
        # We remove the # from the player tag
        player_tag = player_tag[1:]
        url = f"{self.base_url}players/%23{player_tag}/battlelog"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_player_club(self, player_tag: str) -> dict:
        data = self.get_player_stats(player_tag)
        return data["club"]

    def get_club_members(self, club_tag: str) -> list:
        # We remove the # from the club tag
        club_tag = club_tag[1:]
        url = f"{self.base_url}clubs/%23{club_tag}/members"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_club_information(self, club_tag: str) -> dict:
        # We remove the # from the club tag
        club_tag = club_tag[1:]
        url = f"{self.base_url}clubs/%23{club_tag}"
        response = requests.get(url, headers=self.headers)
        return response.json()
