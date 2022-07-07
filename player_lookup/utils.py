from datetime import datetime, timedelta, timezone


def get_number_of_weeks_since_date(since: datetime) -> int:
    """Get the number of weeks since a date.

    Args:
        since (datetime): The date since when the number of weeks is calculated.

    Returns:
        int: The number of weeks since the date.
    """
    if not since:
        # No values were saved in the database early 2022
        since = datetime(year=2022, month=1, day=1, tzinfo=timezone.utc)

    today = datetime.now(timezone.utc)
    # 2 is wednesday's index in weekdays
    offset = (today.weekday() - 2) % 7
    last_wednesday = today - timedelta(days=offset)

    if last_wednesday < since:
        raise ValueError("Since date must be inferior to the last wednesday.")

    return (last_wednesday - since).days // 7


def get_this_weeks_number_of_available_tickets() -> int:
    """Get the number of tickets available for this week.

    Returns:
        int: The number of tickets available for this week.
    """
    today_index = datetime.today().weekday()
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
