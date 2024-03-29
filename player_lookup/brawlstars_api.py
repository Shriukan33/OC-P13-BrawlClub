from __future__ import annotations
import asyncio
import os
from typing import Union
import requests
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
            "Accept": "application/json",
        }
        return header

    def get_player_stats_url(self, player_tag: str) -> str:
        if player_tag.startswith("#"):
            # We remove the # from the player tag
            player_tag = player_tag[1:]
        url = f"{self.base_url}players/%23{player_tag}"
        return url

    def get_player_battlelog(self, player_tag: str, client=httpx.AsyncClient()) -> dict:
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

    async def get_club_members(self, club_tag: str, client=httpx.AsyncClient()) -> dict:
        if club_tag.startswith("#"):
            # We remove the # from the club tag
            club_tag = club_tag[1:]
        url = f"{self.base_url}clubs/%23{club_tag}/members"
        response = await client.get(url, headers=self.headers)
        return response.json()

    async def get_club_members_tag_list(
        self, club_tag: str, client=httpx.AsyncClient()
    ) -> list:
        """Returns a list of the club members' tags."""
        api_calls = []
        response = self.get_club_members(club_tag, client)
        api_calls.append(response)
        responses = await asyncio.gather(*api_calls)
        club_members_tag_list = []
        for club_members in responses:
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

    async def get_club_batch_player_tags_list(self, club_tags: list):
        """Returns a list of the clubs members' tags."""
        club_members_tag_list = []
        api_calls = []
        # We fetch all clubs members' tags, for each club in club_tags
        async with httpx.AsyncClient(timeout=None) as client:
            for club_tag in club_tags:
                response = self.get_club_members(club_tag, client)
                api_calls.append(response)
            responses = await asyncio.gather(*api_calls)

        # 1 api call = 1 club
        # Each response is a dict with an "items" key, which is a list where each
        # element is a dict with a "tag" key, which is the player tag.
        for response in responses:
            for member in response["items"]:
                club_members_tag_list.append(member["tag"])

        return club_members_tag_list

    def is_player_or_club(self, tag: str) -> Union[str, None]:
        """Returns wheter or not a tag represents a player or club or none of these

        Note that a tag can belong to both a player and a club.
        We return the player in priority because most likely the user is looking for a
        player (themselves) and will get the club from here.

        Returns:
        'player' -- If the tag is associated with a player
        'club' -- If the tag is associated with a club
        None -- If the tag doesn't match any of the above
        """
        if tag.startswith("#"):
            # We remove the # from the club tag
            tag = tag[1:]

        # Battlelog will return 404 if the player hasn't played in a long time
        url = f"{self.base_url}players/%23{tag}/battlelog"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return "player"

        url = f"{self.base_url}clubs/%23{tag}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return "club"

        return None
