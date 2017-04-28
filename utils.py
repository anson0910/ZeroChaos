from datetime import datetime, timedelta


def get_date_by_days_after_with_weekday(year, month, day, days_after):
    """
    Returns date in format Weekday Day-Month(English)-Year,
    with days_after days after the provided date
    """
    date = datetime(year, month, day)
    res_date = date + timedelta(days=days_after)
    return res_date.strftime('%a %d-%b-%Y')


def get_date_by_days_after(year, month, day, days_after):
    """
    Returns date as datetime object
    with days_after days after the provided date
    """
    date = datetime(year, month, day)
    res_date = date + timedelta(days=days_after)
    return res_date


if __name__ == '__main__':
    res_date = get_date_by_days_after(2017, 3, 13, 0)
    print(type(res_date.day))
