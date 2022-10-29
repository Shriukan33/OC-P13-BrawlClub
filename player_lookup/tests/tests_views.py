import datetime
import json
from pathlib import Path
from unittest import mock

import httpx
import requests
from django.db.models import Avg, Count
from django.test import TestCase
from django.urls import reverse
from player_lookup.models import Club, Player, PlayerHistory


class ClubFinderTests(TestCase):
    def setUp(self):
        self.low_level_club = Club.objects.create(
            club_tag="#123456789",
            club_name="Test Club",
            club_description="Test Club Description",
        )
        self.low_level_player = Player.objects.create(
            player_tag="#987654321",
            player_name="Test Player",
            trophy_count=1000,
            club=self.low_level_club,
        )
        self.high_level_club = Club.objects.create(
            club_tag="#112233445",
            club_name="Test Club 2",
            club_description="Test Club Description 2",
            required_trophies=30000,
        )
        self.high_level_player = Player.objects.create(
            player_tag="#554433221",
            player_name="Test Player 2",
            trophy_count=50000,
            club=self.high_level_club,
        )
        self.club_finder_url = reverse("player_lookup:club_finder_results")

    def test_club_finder(self):
        # These get args should return the low level club
        get_args = "&".join(
            [
                "max_trophies=0",
                "type=open",
                "min_members=1",
                "max_members=29",
            ]
        )
        response = self.client.get(self.club_finder_url + "?" + get_args)
        self.assertEqual(response.status_code, 200)
        # Only the low level club should be returned, as the max_trophies is 0
        # max_trophies is reference to a club's required_trophies
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["club_tag"], self.low_level_club.club_tag)

        high_level_get_args = get_args.replace("max_trophies=0", "max_trophies=100000")
        response = self.client.get(self.club_finder_url + "?" + high_level_get_args)
        self.assertEqual(response.status_code, 200)
        # Both clubs should be returned, as the max_trophies is 100000
        self.assertEqual(len(response.data), 2)
        # Clubs are ordered by average brawlclub rating and then total of trophies
        # of all members.
        # The high level one has more trophies than the low level one, and both have
        # the same average brawlclub rating (0), so the high level one should be first.
        self.assertEqual(response.data[0]["club_tag"], self.high_level_club.club_tag)
        self.assertEqual(response.data[1]["club_tag"], self.low_level_club.club_tag)

        # We're testing that the club finder returns the best average brawlclub rating
        # first.
        self.low_level_player.brawlclub_rating = 100
        self.low_level_player.save()

        response = self.client.get(self.club_finder_url + "?" + high_level_get_args)
        self.assertEqual(response.status_code, 200)
        # Both clubs should be returned, as the max_trophies is 100000
        self.assertEqual(len(response.data), 2)
        # Clubs are ordered by average brawlclub rating and then total of trophies
        # of all members.
        # The low level club has a higher average brawlclub rating than the high level
        # one, so the low level one should be first.
        self.assertEqual(response.data[0]["club_tag"], self.low_level_club.club_tag)
        self.assertEqual(response.data[1]["club_tag"], self.high_level_club.club_tag)

        # We're testing what happens when invalid get args are passed.
        valid_get_args = "&".join(
            [
                "max_trophies=100000",
                "type=open",
                "min_members=0",
                "max_members=30",
            ]
        )
        # First we're making the types invalid
        closed_club = Club.objects.create(
            club_tag="#CLOSED",
            club_name="Closed Club",
            club_description="Closed Club Description",
            club_type="closed",
        )
        Player.objects.create(
            player_tag="#CLOSEDPLAYER",
            player_name="Closed Player",
            trophy_count=1000,
            club=closed_club,
        )
        invalid_get_args = valid_get_args.replace("type=open", "type=0")
        response = self.client.get(self.club_finder_url + "?" + invalid_get_args)
        # Still returns 200 and no filter is applied on types
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3, f'{response.data}')

        # Now we're making the max_trophies invalid
        invalid_get_args = valid_get_args.replace(
            "max_trophies=100000", "max_trophies=invalid")
        response = self.client.get(self.club_finder_url + "?" + invalid_get_args)
        # Still returns 200 and no filter is applied on max_trophies
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2, f'{response.data}')

        # Now we're making the min_members invalid
        invalid_get_args = valid_get_args.replace(
            "min_members=0", "min_members=invalid")
        response = self.client.get(self.club_finder_url + "?" + invalid_get_args)
        # Still returns 200 and no filter is applied on min_members
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2, f'{response.data}')

        # Now we're making the max_members invalid
        invalid_get_args = valid_get_args.replace(
            "max_members=30", "max_members=invalid")
        response = self.client.get(self.club_finder_url + "?" + invalid_get_args)
        # Still returns 200 and no filter is applied on max_members
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2, f'{response.data}')


class ClubMembersTests(TestCase):
    def setUp(self):
        ClubFinderTests.setUp(self)
        self.low_level_club_members_url = reverse(
            "player_lookup:club_members", args=[self.low_level_club.club_tag]
        )
        self.second_low_level_player = Player.objects.create(
            player_tag="#111111111",
            player_name="Test Player 3",
            trophy_count=1000,
            club=self.low_level_club,
        )

    def test_club_members(self):
        url = reverse("player_lookup:club_members", args=["123456789"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data[0]["player_tag"], self.low_level_player.player_tag
        )
        self.assertEqual(
            response.data[1]["player_tag"], self.second_low_level_player.player_tag
        )


class LeaderBoardViewTests(TestCase):
    def setUp(self):
        ClubMembersTests.setUp(self)
        self.player_leaderboard_url = reverse(
            "player_lookup:leaderboard", args=["players"]
        )
        self.club_leaderboard_url = reverse("player_lookup:leaderboard", args=["clubs"])

        club = Club.objects.create(
            club_tag="#FULLCLUB",
            club_name="Test Full Club",
            club_description="Test Club Description",
        )
        for i in range(1, 30):
            Player.objects.create(
                player_tag="#ABCDEFG{}".format(i),
                player_name="Test Player {}".format(i),
                trophy_count=i * 1000,
                club=club,
                brawlclub_rating=i * 2,
            )

    def test_player_leaderboard(self):
        response = self.client.get(self.player_leaderboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 10)
        highest_brawlclub_rating_player = Player.objects.filter(
            brawlclub_rating__gt=0
        ).order_by("-brawlclub_rating")[0]
        self.assertEqual(
            response.data["results"][0]["player_tag"],
            highest_brawlclub_rating_player.player_tag,
        )

    def test_club_leaderboard(self):

        # Create 10 random clubs
        for i in range(10):
            club = Club.objects.create(
                club_tag="#TESTCLUB{}".format(i),
                club_name="Test Club {}".format(i),
                club_description="Test Club Description",
            )
            for j in range(1, 30):
                Player.objects.create(
                    player_tag="#TESTPLAYER{}".format(str(i) + str(j)),
                    player_name="Test Player {}".format(str(i) + str(j)),
                    trophy_count=j * 1000,
                    club=club,
                    brawlclub_rating=j * 2,
                )

        response = self.client.get(self.club_leaderboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 10)
        highest_brawlclub_rating_club = (
            Club.objects.annotate(avg_bcr=Avg("player__brawlclub_rating"))
            .annotate(nb_of_players=Count("player"))
            .order_by("-avg_bcr", "-trophies")
            .filter(nb_of_players__gte=25)
        )[0]
        self.assertEqual(
            response.data["results"][0]["club_tag"],
            highest_brawlclub_rating_club.club_tag,
        )

    def test_leaderboard_invalid_entity(self):
        url = reverse("player_lookup:leaderboard", args=["invalid_entity"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class PlayerAreaGraphViewTests(TestCase):
    def setUp(self):
        self.player = Player.objects.create(
            player_tag="#ABCDEFG",
            player_name="Test Player",
            trophy_count=1000,
        )
        self.player_area_graph_url = reverse(
            "player_lookup:player_areagraph", args=["ABCDEFG"]
        )
        history = []
        for _ in range(10):
            history.append(self.player.create_player_history_instance())

        PlayerHistory.objects.bulk_create(history)

    def test_player_area_graph(self):
        response = self.client.get(self.player_area_graph_url)
        self.assertEqual(response.status_code, 200)
        # Only the last 8 are returned for a given player
        self.assertEqual(len(response.data), 8)
        all_snapshot_dates = [
            datetime.datetime.strptime(
                snapshot["snapshot_date"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            for snapshot in response.data
        ]
        # The snapshots are ordered by date
        self.assertTrue(min(all_snapshot_dates) == all_snapshot_dates[0])
        self.assertTrue(max(all_snapshot_dates) == all_snapshot_dates[-1])


class SearchUnknownEntityTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            club_tag="#TESTCLUB",
            club_name="Test Club",
            club_description="Test Club Description",
        )
        self.player = Player.objects.create(
            player_tag="#ABCDEFG",
            player_name="Test Player",
            trophy_count=1000,
            club=self.club,
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

    def test_unknown_entity_player(self):
        url = reverse("player_lookup:search_unknown", args=["ABCDEFG"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["player_tag"], self.player.player_tag)

    def test_unknown_entity_club(self):
        url = reverse("player_lookup:search_unknown", args=["TESTCLUB"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["club_tag"], self.club.club_tag)

    @mock.patch.object(requests, "get")
    @mock.patch.object(httpx.AsyncClient, "get")
    def test_unknown_entity_unknown_player(self, mock_httpx_get, mock_requests_get):

        # ##### Mocks
        # See retrieve_unknown_entity_flow.md to see the flow of the requests

        # We will first test the case where the entity is a player
        mock_requests_get.side_effect = [
            # First call to requests.get is to check if the entity is a player
            mock.Mock(status_code=200),
            # Second call to requests.get is get players club info
            mock.MagicMock(json=mock.MagicMock(return_value=self.club_data_P0GVGVRP)),
            # When the player has a club, a third call to requests.get is made
            # to update the club's informations
            mock.MagicMock(json=mock.MagicMock(return_value=self.club_data_P0GVGVRP)),
        ]
        mock_httpx_get.side_effect = [
            # First call is for the player's profile
            httpx.Response(200, json=self.player_data_2RQRYV0L),
            # Second call is for the player's battlelog
            httpx.Response(200, json=self.player_battlelog_2RQRYV0L),
            # Third call is for the club's members
            httpx.Response(200, json=self.club_members_P0GVGVRP),
            # Fourth & fifth calls are for the player's profile,
            # in order in the members list
            httpx.Response(200, json=self.player_data_2RQRYV0L),
            httpx.Response(200, json=self.player_data_9090YYGQ),
            # Sixth and seventh calls are for the players' battlelog
            httpx.Response(200, json=self.player_battlelog_2RQRYV0L),
            httpx.Response(200, json=self.player_battlelog_9090YYGQ),
        ]

        url = reverse("player_lookup:search_unknown", args=["2RQRYV0L"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["player_tag"], "#2RQRYV0L")

    @mock.patch.object(requests, "get")
    @mock.patch.object(httpx.AsyncClient, "get")
    def test_unknown_entity_unknown_club(self, mock_httpx_get, mock_requests_get):

        # ##### Mocks
        # See retrieve_unknown_entity_flow.md to see the flow of the requests

        # We will first test the case where the entity is a club
        mock_requests_get.side_effect = [
            # First call to requests.get is to check if the entity is a player
            mock.Mock(status_code=404),
            # Second call to requests.get is to check if the entity is a club
            mock.Mock(status_code=200),
            # Third call to requests.get is to check get the club's info
            mock.MagicMock(json=mock.MagicMock(return_value=self.club_data_P0GVGVRP)),
            # A fourth call to requests.get is made to update the
            # club's informations
            mock.MagicMock(json=mock.MagicMock(return_value=self.club_data_P0GVGVRP)),
        ]
        mock_httpx_get.side_effect = [
            # 1st call is for the club's members
            httpx.Response(200, json=self.club_members_P0GVGVRP),
            # 2nd & 3r calls are for the player's profile,
            # in order in the members list
            httpx.Response(200, json=self.player_data_2RQRYV0L),
            httpx.Response(200, json=self.player_data_9090YYGQ),
            # 4th and 5th calls are for the players' battlelog
            httpx.Response(200, json=self.player_battlelog_2RQRYV0L),
            httpx.Response(200, json=self.player_battlelog_9090YYGQ),
        ]

        url = reverse("player_lookup:search_unknown", args=["#P0GVGVRP"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["club_tag"], "#P0GVGVRP")

    @mock.patch.object(requests, "get")
    def test_unknown_entity_unknown_invalid(self, mock_requests_get):
        mock_requests_get.side_effect = [
            # First call to requests.get is to check if the entity is a player
            mock.Mock(status_code=404),
            # Second call to requests.get is to check if the entity is a club
            mock.Mock(status_code=404),
        ]
        url = reverse("player_lookup:search_unknown", args=["INVALID"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class SingleEntityViewTests(TestCase):

    def setUp(self):
        self.club = Club.objects.create(
            club_tag="#P0GVGVRP",
            club_name="Test Club",
            club_description="Test Club Description",
        )
        self.player = Player.objects.create(
            player_tag="#2RQRYV0L",
            player_name="Test Player",
            club=self.club
        )

    def test_single_entity_player(self):
        url = reverse("player_lookup:search_specific",
                      args=["player", "2RQRYV0L"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["player_tag"], self.player.player_tag)

    def test_single_entity_club(self):
        url = reverse("player_lookup:search_specific", args=["club", "P0GVGVRP"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["club_tag"], self.club.club_tag)

    def test_single_entity_invalid(self):
        url = reverse("player_lookup:search_specific", args=["invalid", "P0GVGVRP"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_single_entity_invalid_tag(self):
        url = reverse("player_lookup:search_specific", args=["player", "INVALID"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
