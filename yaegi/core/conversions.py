from datetime import datetime, timezone
from typing import Tuple


def datetime_to_julian_day(dt: datetime) -> float:
    """Convert datetime to Julian Day Number"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    utc_dt: datetime = dt.astimezone(timezone.utc)
    year: int = utc_dt.year
    month: int = utc_dt.month
    day: int = utc_dt.day
    hour: int = utc_dt.hour
    minute: int = utc_dt.minute
    second: int = utc_dt.second
    microsecond: int = utc_dt.microsecond

    if month <= 2:
        year -= 1
        month += 12

    a: int = year // 100
    b: int = 2 - a + (a // 4)

    if year < 1582 or (year == 1582 and month < 10) or (year == 1582 and month == 10 and day < 15):
        b = 0

    jd: float = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5
    time_fraction: float = (hour + minute / 60 + (second + microsecond / 1_000_000) / 3600) / 24
    jd += time_fraction

    return jd


def julian_day_to_datetime(jd: float) -> datetime:
    """Convert Julian Day Number to datetime"""
    jd += 0.5
    z: int = int(jd)
    f: float = jd - z

    if z >= 2299161:
        alpha: int = int((z - 1867216.25) / 36524.25)
        a: int = z + 1 + alpha - alpha // 4
    else:
        a: int = z

    b: int = a + 1524
    c: int = int((b - 122.1) / 365.25)
    d: int = int(365.25 * c)
    e: int = int((b - d) / 30.6001)

    day: int = b - d - int(30.6001 * e)
    month: int = e - 1 if e < 14 else e - 13
    year: int = c - 4716 if month > 2 else c - 4715

    hours: float = f * 24
    hour: int = int(hours)
    minutes: float = (hours - hour) * 60
    minute: int = int(minutes)
    seconds: float = (minutes - minute) * 60
    second: int = int(seconds)
    microsecond: int = int((seconds - second) * 1_000_000)

    return datetime(year, month, day, hour, minute, second, microsecond, timezone.utc)


def degrees_to_dms(degrees: float) -> Tuple[int, int, float]:
    """Convert decimal degrees to degrees, minutes, seconds"""
    d: int = int(abs(degrees))
    m: int = int((abs(degrees) - d) * 60)
    s: float = ((abs(degrees) - d) * 60 - m) * 60
    if degrees < 0:
        d = -d
    return d, m, s


def dms_to_degrees(degrees: int, minutes: int, seconds: float) -> float:
    """Convert degrees, minutes, seconds to decimal degrees"""
    result: float = abs(degrees) + minutes / 60 + seconds / 3600
    return -result if degrees < 0 else result


def normalize_longitude(longitude: float) -> float:
    """Normalize longitude to 0-360 range"""
    longitude %= 360
    if longitude < 0:
        longitude += 360
    return longitude


def get_rashi_from_longitude(longitude: float) -> int:
    """Get rashi number (1-12) from longitude"""
    return int(normalize_longitude(longitude) / 30) + 1


def get_nakshatra_from_longitude(longitude: float) -> Tuple[int, int]:
    """Get nakshatra number (1-27) and pada (1-4) from longitude"""
    normalized_lon: float = normalize_longitude(longitude)
    nakshatra: int = int(normalized_lon * 27 / 360) + 1
    pada: int = int((normalized_lon * 27 * 4 / 360) % 4) + 1
    return nakshatra, pada
