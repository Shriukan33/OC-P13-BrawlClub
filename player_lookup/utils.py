from datetime import datetime, timedelta, timezone
from typing import Union


def get_number_of_weeks_since_date(since: datetime) -> int:
    """Get the number club league weeks since a date.

    Args:
        since (datetime): The date since when the number of club league weeks is
        calculated.

    Returns:
        int: The number of club league weeks since the date.
    """
    if not since:
        # First club war since update started on July 6th 2022,
        # an odd week. Club wars only happen in odd weeks.
        since = datetime(year=2022, month=7, day=6, tzinfo=timezone.utc)

    today = datetime.now(timezone.utc)
    # 2 is wednesday's index in weekdays
    offset = (today.weekday() - 2) % 7
    last_wednesday = today - timedelta(days=offset)

    if last_wednesday.date() == since.date() and since.isocalendar()[1] % 2 != 0:
        # Last week was odd and we're somewhere between Monday and Tuesday
        # This means that the club war was in progress the last week
        # and we're in the next week but next hasn't started yet
        # A full week hasn't passed but the club war is indeed finished
        return 1

    start_week_index = since.isocalendar()[1]
    # So if start index is 52 (last week of the year), next week's index isn't 1
    # but is 53.
    end_week_index = start_week_index + ((last_wednesday - since).days // 7)
    # We get the number of odd number from the start_week_index to the end_week_index
    if start_week_index % 2 != 0:
        start_week_index += 1
    if end_week_index % 2 != 0:
        end_week_index -= 1
    number_of_odd_weeks_between_dates = (end_week_index - start_week_index) // 2

    if since.isocalendar()[1] % 2 != 0:
        number_of_odd_weeks_between_dates += 1
    return number_of_odd_weeks_between_dates


def get_club_league_status() -> bool:
    """Get the club league status.

    Returns:
        bool: True if the club league is currently in progress, False otherwise.
    """
    current_weeks_number = datetime.today().isocalendar()[1]
    today_index = datetime.today().weekday()
    if current_weeks_number % 2 != 0 and today_index >= 2:
        # We're in an odd week and it's wednesday or later
        club_war_in_progress = True
    elif current_weeks_number % 2 == 0 and today_index == 0:
        # We are the monday of the week after the club war,
        # so we have some time to spend the 14 tickets.
        club_war_in_progress = True
    else:
        club_war_in_progress = False

    return club_war_in_progress


def get_this_weeks_number_of_available_tickets() -> int:
    """Get the number of tickets available for this week.

    Returns:
        int: The number of tickets available for this week.
    """
    club_war_in_progress = get_club_league_status()

    if not club_war_in_progress:
        return 0

    # Club league goes from day 2 (Wednesday) to day 0 (Monday) the next week.
    # This means that the only day that has no club war going anywhere is Tuesday
    # We want to compute de playrate accurately, and counting 2 tickets spent on
    # 14 while only 2 were available so far is not accurate.
    this_weeks_number_of_available_tickets = 0
    today_index = datetime.today().weekday()
    if today_index in range(2, 4):
        # From wednesday to thursday, we only have 4 tickets available
        this_weeks_number_of_available_tickets = 4
    elif today_index in range(4, 6):
        # From friday to saturday, we had a total of 8 tickets available
        # over the week
        this_weeks_number_of_available_tickets = 8
    elif today_index == 6 or today_index == 0:
        # From sunday to monday, we had a total 14 tickets available
        # over the week
        this_weeks_number_of_available_tickets = 14

    return this_weeks_number_of_available_tickets


def get_today_number_of_remaining_tickets() -> int:
    """Return the number of available tickets for a given day.

    Every other week, one has 14 tickets to spend, from wednesday to monday.

    A normal match uses 1 ticket and a Power match uses 2 tickets.

    On wednesday, 4 tickets are granted out of 14 tickets. If they aren't used
    before Friday, they are lost.
    On Friday, 4 more tickets are granted. If they aren't used before Sunday, they
    are lost.
    On Sunday, 6 tickets are granted. If they aren't used before Tuesday, they are
    lost.

    Returns:
        int: The number of tickets a given player has available for the day.
    """
    club_league_running = get_club_league_status()
    if not club_league_running:
        return 0

    today = datetime.now(timezone.utc).weekday()

    if today in (2, 3, 4, 5):
        # Wednesday, Thursday, Friday, Saturday
        available_tickets = 4
    elif today in (6, 0):
        # Sunday, Monday
        available_tickets = 6
    else:
        return 0

    return available_tickets


def get_last_club_league_day_start() -> Union[datetime, None]:
    """Get the datetime of the start of the last club league day.

    Returns:
        datetime: The datetime of the start of the last club league day.
        None is no club league is running.
    """
    club_league_running = get_club_league_status()
    if not club_league_running:
        return None

    today = datetime.now(timezone.utc)
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    # 2 is wednesday's index in weekdays
    offset = (today.weekday() - 2) % 7
    if today.weekday() == 2:
        offset = 0
    last_wednesday = today - timedelta(days=offset)
    last_friday = last_wednesday + timedelta(days=2)
    last_sunday = last_wednesday + timedelta(days=4)

    today = datetime.now(timezone.utc).weekday()

    if today in (2, 3, 4, 5):
        # Wednesday, Thursday, Friday, Saturday
        if today in (2, 3):
            club_league_day = last_wednesday
        else:
            club_league_day = last_friday
    elif today in (6, 0):
        # Sunday, Monday
        club_league_day = last_sunday
    else:
        return None

    return club_league_day
