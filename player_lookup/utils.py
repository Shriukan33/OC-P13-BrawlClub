from datetime import datetime, timedelta, timezone


def get_number_of_weeks_since_date(since: datetime) -> int:
    """Get the number club league weeks since a date.

    Args:
        since (datetime): The date since when the number of club league weeks is calculated.

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



def get_this_weeks_number_of_available_tickets() -> int:
    """Get the number of tickets available for this week.

    Returns:
        int: The number of tickets available for this week.
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

    if not club_war_in_progress:
        return 0

    
    # Club league goes from day 2 (Wednesday) to day 0 (Monday) the next week.
    # This means that the only day that has no club war going anywhere is Tuesday
    # We want to compute de playrate accurately, and counting 2 tickets spent on
    # 14 while only 2 were available so far is not accurate.
    this_weeks_number_of_available_tickets = 0
    if today_index in range(2, 4):
        # From wednesday to thursday, we only have 4 tickets available
        this_weeks_number_of_available_tickets = 4
    elif today_index in range(5, 6):
        # From friday to saturday, we had a total of 8 tickets available
        # over the week
        this_weeks_number_of_available_tickets = 8
    elif today_index == 6 or today_index == 0:
        # From sunday to monday, we had a total 14 tickets available
        # over the week
        this_weeks_number_of_available_tickets = 14

    return this_weeks_number_of_available_tickets
