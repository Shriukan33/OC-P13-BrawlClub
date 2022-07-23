from __future__ import annotations
from typing import TYPE_CHECKING
import os
import requests

if TYPE_CHECKING:
    import httpx


class BrawlAPi:

    def __init__(self) -> None:
        self.base_url = "https://api.brawlstars.com/v1/"
        self._api_key = os.environ.get("BRAWLSTARS_API_KEY")
        # To use multiple API keys, separate them with a #
        # The need of multiple keys is to avoid being throttled.
        # Up to 10 keys are allowed per account.
        self._api_key = iter(self._api_key.split("#"))

    @property
    def api_key(self) -> str:
        try:
            return next(self._api_key)
        except StopIteration:
            self.__init__()
            return next(self._api_key)

    @property
    def headers(self) -> dict:
        header = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        return header

    def get_player_stats(self, player_tag: str) -> dict:
        if player_tag.startswith("#"):
            # We remove the # from the player tag
            player_tag = player_tag[1:]
        url = f"{self.base_url}players/%23{player_tag}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_player_stats_url(self, player_tag: str) -> str:
        if player_tag.startswith("#"):
            # We remove the # from the player tag
            player_tag = player_tag[1:]
        url = f"{self.base_url}players/%23{player_tag}"
        return url

    def get_player_battlelog(self, player_tag: str, client: httpx.AsyncClient) -> dict:
        """Get data from the player's last 24 matches"""
        if player_tag.startswith("#"):
            # We remove the # from the player tag
            player_tag = player_tag[1:]
        url = f"{self.base_url}players/%23{player_tag}/battlelog"
        response = client.get(url, headers=self.headers)
        return response.json()

    def get_player_battlelog_url(self, player_tag: str) -> str:
        if player_tag.startswith("#"):
            # We remove the # from the player tag
            player_tag = player_tag[1:]
        url = f"{self.base_url}players/%23{player_tag}/battlelog"
        return url

    def get_player_club(self, player_tag: str) -> dict:
        data = self.get_player_stats(player_tag)
        return data["club"]

    def get_club_members(self, club_tag: str) -> dict:
        if club_tag.startswith("#"):
            # We remove the # from the club tag
            club_tag = club_tag[1:]
        url = f"{self.base_url}clubs/%23{club_tag}/members"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_club_members_tag_list(self, club_tag: str) -> list:
        """Returns a list of the club members' tags."""
        club_members = self.get_club_members(club_tag)
        club_members_tag_list = []
        for member in club_members["items"]:
            club_members_tag_list.append(member["tag"])
        return club_members_tag_list

    def get_club_information(self, club_tag: str) -> dict:
        if club_tag.startswith("#"):
            # We remove the # from the club tag
            club_tag = club_tag[1:]
        url = f"{self.base_url}clubs/%23{club_tag}"
        response = requests.get(url, headers=self.headers)
        return response.json()
