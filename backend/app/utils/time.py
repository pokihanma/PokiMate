from datetime import date, datetime, timedelta


def month_start(d: date) -> date:
    return d.replace(day=1)


def month_end(d: date) -> date:
    if d.month == 12:
        return d.replace(day=31)
    return (d.replace(month=d.month + 1, day=1)) - timedelta(days=1)


def parse_month(s: str) -> date | None:
    """Parse YYYY-MM to first day of month."""
    try:
        y, m = int(s[:4]), int(s[5:7])
        return date(y, m, 1)
    except (ValueError, IndexError):
        return None


def iso_date(d: date | datetime) -> str:
    if isinstance(d, datetime):
        d = d.date()
    return d.isoformat()
