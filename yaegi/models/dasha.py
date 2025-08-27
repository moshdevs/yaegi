from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class DashaPeriod:
    planet: str
    start_date: datetime
    end_date: datetime
    duration_years: float
    level: str = "mahadasha"
    parent_dasha: Optional[str] = None

    @property
    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days

    @property
    def remaining_days(self) -> int:
        now = datetime.now()
        if now > self.end_date:
            return 0
        return (self.end_date - now).days

    @property
    def is_active(self) -> bool:
        now = datetime.now()
        return self.start_date <= now <= self.end_date

    def to_dict(self) -> dict[str, any]:
        return {
            "planet": self.planet,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "duration_years": self.duration_years,
            "duration_days": self.duration_days,
            "remaining_days": self.remaining_days,
            "level": self.level,
            "parent_dasha": self.parent_dasha,
            "is_active": self.is_active,
        }


@dataclass
class VimshottariDasha:
    birth_date: datetime
    moon_nakshatra: int
    periods: list[DashaPeriod]

    def get_current_mahadasha(self) -> Optional[DashaPeriod]:
        for period in self.periods:
            if period.is_active and period.level == "mahadasha":
                return period
        return None

    def get_active_periods(self) -> list[DashaPeriod]:
        return [period for period in self.periods if period.is_active]
      
