from datetime import datetime, timezone, timedelta
from django.test import TestCase
from freezegun import freeze_time
from player_lookup import utils


"""
We are testing that the club league status and the number of available
tickets per day are actually valid.
Club league is running from wednesday to monday the next week.
Starting day is in odd weeks, since the first club league happened the 27th
week of 2022.

Each player is given tickets they have to spend in order to participate in
club league. The number of tickets is based on the day of the week, and are lost
if not used.

The number of tickets per day is as follows:
    - Wednesday to Thursday: 4 tickets
    - Friday to Saturday: 4 tickets
    - Sunday to Monday: 6 tickets
"""


class GetClubLeagueStatusTests(TestCase):
    def test_get_club_league_status_and_remaining_tickets(self):
        # Odd week, wednesday
        with freeze_time("2022-10-26", tick=True):
            self.assertTrue(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 4)

        # Odd week, thursday
        with freeze_time("2022-10-27", tick=True):
            self.assertTrue(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 4)

        # Odd week, friday
        with freeze_time("2022-10-28", tick=True):
            self.assertTrue(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 4)

        # Odd week, saturday
        with freeze_time("2022-10-29", tick=True):
            self.assertTrue(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 4)

        # Odd week, sunday
        with freeze_time("2022-10-30", tick=True):
            self.assertTrue(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 6)

        # Even week, monday
        with freeze_time("2022-10-31", tick=True):
            self.assertTrue(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 6)

        # Even week, tuesday
        with freeze_time("2022-11-01", tick=True):
            self.assertFalse(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 0)

        # Even week, wednesday
        with freeze_time("2022-11-02", tick=True):
            self.assertFalse(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 0)

        # Even week, thursday
        with freeze_time("2022-11-03", tick=True):
            self.assertFalse(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 0)

        # Even week, friday
        with freeze_time("2022-11-04", tick=True):
            self.assertFalse(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 0)

        # Even week, saturday
        with freeze_time("2022-11-05", tick=True):
            self.assertFalse(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 0)

        # Even week, sunday
        with freeze_time("2022-11-06", tick=True):
            self.assertFalse(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 0)

        # Odd week, monday
        with freeze_time("2022-11-07", tick=True):
            self.assertFalse(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 0)

        # Odd week, tuesday
        with freeze_time("2022-11-08", tick=True):
            self.assertFalse(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 0)

        # Odd week, wednesday
        with freeze_time("2022-11-09", tick=True):
            self.assertTrue(utils.get_club_league_status())
            self.assertEqual(utils.get_today_number_of_remaining_tickets(), 4)

    def test_numbers_of_weeks_since_date(self):

        # In the following scenarios, the club league has started the 26th of
        # october 2022, which is the 27th week of 2022.
        # We want to test the number of whole club leagues have past between
        # the start date and the current date.
        # If the player is created during a club league, the number of weeks
        # since the start date should be 0 until the player completes a whole
        # club league.

        # #####################################
        # # Player created BEFORE club league #
        # #####################################
        # 5 identified cases :
        # - We're updating the player before the club league starts
        # - We're updating the player during the club league
        # - We're updating the player after the club league but before the next
        #   club league starts
        # - We're updating the player after the next club league starts
        # - We're updating the player after the next club league ends

        starting_date = datetime(2022, 10, 25, tzinfo=timezone.utc)

        # We're updating the player before the club league starts
        with freeze_time("2022-10-25", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 0)

        # We're updating the player's profile the friday of
        # the same week during club league.
        with freeze_time("2022-10-28", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 0)

        # We're updating the player's profile after the club league but before
        # the next one, the 8th of november, a tuesday.
        with freeze_time("2022-11-08", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 1)

        # We're updating the player's profile at the beginning of
        # the next club league
        with freeze_time("2022-11-09", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 1)

        # We're updating the player's profile at the end of
        # the next club league
        with freeze_time("2022-11-15", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 2)

        # ######################################################################
        # # Player created DURING club league, and AFTER Wednesday or Thursday #
        # ######################################################################
        # 4 identified cases :
        # - We're updating the player during the club league
        # - We're updating the player after the club league but before the next
        #   club league starts
        # - We're updating the player after the next club league starts
        # - We're updating the player after the next next club league ends

        starting_date = datetime(2022, 10, 28, tzinfo=timezone.utc)

        # We're updating the player's profile the friday of
        # the same week during club league.
        with freeze_time("2022-10-28", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 0)

        # We're updating the player's profile after the club league but before
        # the next one, the 8th of november, a tuesday.
        with freeze_time("2022-11-08", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 0)

        # We're updating the player's profile at the beginning of
        # the next club league
        with freeze_time("2022-11-09", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 0)

        # We're updating the player's profile at the end of
        # the next next club league
        with freeze_time("2022-11-15", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 1)

        # #########################################################################
        # # Player created DURING club league, and BETWEEN Wednesday and Thursday #
        # #########################################################################
        # 4 identified cases :
        # - We're updating the player during the club league
        # - We're updating the player after the club league but before the next
        #   club league starts
        # - We're updating the player after the next club league starts
        # - We're updating the player after the next next club league ends

        # Wednesday
        starting_date = datetime(2022, 10, 26, tzinfo=timezone.utc)

        # We're updating the player's profile the friday of
        # the same week during club league.
        with freeze_time("2022-10-28", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 0)
            self.assertEqual(
                utils.get_number_of_weeks_since_date(starting_date + timedelta(1)), 0
            )

        # We're updating the player's profile after the club league but before
        # the next one, the 8th of november, a tuesday.
        with freeze_time("2022-11-08", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 1)
            self.assertEqual(
                utils.get_number_of_weeks_since_date(starting_date + timedelta(1)), 1
            )

        # We're updating the player's profile at the beginning of
        # the next club league
        with freeze_time("2022-11-09", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 1)
            self.assertEqual(
                utils.get_number_of_weeks_since_date(starting_date + timedelta(1)), 1
            )

        # We're updating the player's profile at the end of
        # the next next club league
        with freeze_time("2022-11-15", tick=True):
            self.assertEqual(utils.get_number_of_weeks_since_date(starting_date), 2)
            self.assertEqual(
                utils.get_number_of_weeks_since_date(starting_date + timedelta(1)), 2
            )
