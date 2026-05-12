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
