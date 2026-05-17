import wx


def bd_to_vn_age(bd: wx.DateTime) -> str:
    if not bd.IsValid():
        return "Invalid Date"

    today = wx.DateTime.Today()
    delta = today.DiffAsDateSpan(bd)
    years = delta.GetYears()

    # Tier 1: 2 Years and older
    if years >= 2:
        return f"{years} tuổi"

    # Tier 2: 2 Months to < 2 Years (Total Months)
    total_months = delta.GetTotalMonths()
    if total_months >= 2:
        return f"{total_months} tháng"

    # Tier 3: Under 2 Months (Total Days)
    return f"{delta.GetTotalDays()} ngày"


VIETNAMESE_WEEKDAYS = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"]


def wxdatetime_to_vietnamese(dt: wx.DateTime) -> str:
    """
    Converts a wx.DateTime to a Vietnamese datetime string format:
    Example: "T2 15/02/1991 19:00"
    """
    # Get weekday index (0=Sunday), day, month, year, hour, minute, second
    weekday = dt.GetWeekDay()  # wx.DateTime.wxDateTimeWeekDay
    day = dt.GetDay()
    month = dt.GetMonth() + 1  # wxPython months go from 0-11
    year = dt.GetYear()
    hour = dt.GetHour()
    minute = dt.GetMinute()

    vietnam_weekday = VIETNAMESE_WEEKDAYS[weekday]
    formatted_date = (
        f"{vietnam_weekday} {day:02d}/{month:02d}/{year} {hour:02d}:{minute:02d}"
    )
    return formatted_date
