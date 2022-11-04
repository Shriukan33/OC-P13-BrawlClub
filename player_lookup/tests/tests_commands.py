import json
from pathlib import Path
from unittest import mock

import httpx
from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time
from player_lookup.models import Club, MatchIssue, Player, PlayerHistory, Match


class UpdateAllPlayersTests(TestCase):

    def setUp(self):
        self.player_9090YYGQ = Player.objects.create(
            player_tag='#9090YYGQ',
            player_name='Player 9090YYGQ',
            trophy_count=1000,
        )
        self.player_2RQRYV0L = Player.objects.create(
            player_tag='#2RQRYV0L',
            player_name='Player 2RQRYV0L',
            trophy_count=1000,
        )

        THIS_DIR = Path(__file__).parent
        self.TEST_DATA_DIR = THIS_DIR / "test_data"

        # Data setup
        with open(self.TEST_DATA_DIR / "test_player_2RQRYV0L.json", "rb") as f:
            self.player_data_2RQRYV0L = json.load(f)
        with open(
            self.TEST_DATA_DIR / "test_player_2RQRYV0L_battlelog.json", "rb"
        ) as f:
            self.player_battlelog_2RQRYV0L = json.load(f)
        with open(self.TEST_DATA_DIR / "test_club_P0GVGVRP.json", "rb") as f:
            self.club_data_P0GVGVRP = json.load(f)
        with open(self.TEST_DATA_DIR / "test_club_P0GVGVRP_members.json", "rb") as f:
            self.club_members_P0GVGVRP = json.load(f)
        with open(self.TEST_DATA_DIR / "test_player_9090YYGQ.json", "rb") as f:
            self.player_data_9090YYGQ = json.load(f)
        with open(
            self.TEST_DATA_DIR / "test_player_9090YYGQ_battlelog.json", "rb"
        ) as f:
            self.player_battlelog_9090YYGQ = json.load(f)

    @mock.patch("httpx.AsyncClient.get")
    @mock.patch("player_lookup.utils.get_club_league_status")
    @freeze_time("2022-10-26", tick=True)
    def test_update_while_club_league_running(
        self,
        mocked_club_league_status,
        mocked_httpx_get,
    ):
        mocked_club_league_status.return_value = True
        mocked_httpx_get.side_effect = [
            httpx.Response(200, json=self.player_data_9090YYGQ),
            httpx.Response(200, json=self.player_data_2RQRYV0L),
            httpx.Response(200, json=self.player_battlelog_9090YYGQ),
            httpx.Response(200, json=self.player_battlelog_2RQRYV0L),
            httpx.Response(200, json=self.club_data_P0GVGVRP),
        ]
        call_command("update_all_players", "--force")
        self.player_9090YYGQ.refresh_from_db()
        self.player_2RQRYV0L.refresh_from_db()
        self.assertEqual(self.player_9090YYGQ.trophy_count, 30616)
        self.assertEqual(self.player_2RQRYV0L.trophy_count, 30425)
        self.assertEqual(MatchIssue.objects.count(), 2)
        self.assertEqual(Match.objects.count(), 2)

        mocked_club_league_status.return_value = False
        call_command("update_all_players")


class TestGetNewPlayers(TestCase):

    def setUp(self):
        self.club_P0GVGVRP = Club.objects.create(
            club_tag='#P0GVGVRP',
            club_name='Test Club',
        )

        THIS_DIR = Path(__file__).parent
        self.TEST_DATA_DIR = THIS_DIR / "test_data"

        # Data setup
        with open(self.TEST_DATA_DIR / "test_club_P0GVGVRP_members.json", "rb") as f:
            self.club_members_P0GVGVRP = json.load(f)

    @mock.patch("httpx.AsyncClient.get")
    def test_get_new_players(self, mocked_httpx_get):
        mocked_httpx_get.side_effect = [
            httpx.Response(200, json=self.club_members_P0GVGVRP),
        ]
        call_command("get_new_players")
        self.assertEqual(Player.objects.count(), 2)
        self.assertEqual(
            list(Player.objects.values_list(
                "player_tag", flat=True
            ).order_by("player_tag")),
            ["#2RQRYV0L", "#9090YYGQ"],
        )


class TestMakePlayersHistory(TestCase):

    def setUp(self):
        self.player_9090YYGQ = Player.objects.create(
            player_tag='#9090YYGQ',
            player_name='Player 9090YYGQ',
            trophy_count=1000,
        )
        self.player_2RQRYV0L = Player.objects.create(
            player_tag='#2RQRYV0L',
            player_name='Player 2RQRYV0L',
            trophy_count=1000,
        )

    def test_make_players_history(self):
        call_command("make_players_history")

        self.assertEqual(PlayerHistory.objects.count(), 2)
        self.assertEqual(
            list(PlayerHistory.objects.values_list(
                "player__player_tag", flat=True
            ).order_by("player__player_tag")),
            ["#2RQRYV0L", "#9090YYGQ"],
        )
