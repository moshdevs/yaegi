from dataclasses import dataclass

@dataclass
class Planet:
    name: str
    longitude: float
    latitude: float = 0.0
    distance: float = 0.0
    speed: float = 0.0
    rashi: int = 0
    degree: float = 0.0
    minute: float = 0.0
    second: float = 0.0
    nakshatra: int = 0
    nakshatra_pada: int = 0
    is_retrograde: bool = False
    house: int = 1

    def __post_init__(self):
        self.rashi = int(self.longitude // 30) + 1
        self.degree = self.longitude % 30
        self.minute = (self.degree % 1) * 60
        self.second = (self.minute % 1) * 60
        self.nakshatra = int(self.longitude * 27 / 360) + 1
        self.nakshatra_pada = int((self.longitude * 27 * 4 / 360) % 4) + 1

    @property
    def dms(self) -> str:
        return f"{int(self.degree)}°{int(self.minute)}'{int(self.second)}\""

    @property
    def formatted_longitude(self) -> str:
        return f"{self.longitude:.6f}°"

    def to_dict(self) -> dict[str, any]:
        return {
            "name": self.name,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "rashi": self.rashi,
            "degree": self.degree,
            "nakshatra": self.nakshatra,
            "nakshatra_pada": self.nakshatra_pada,
            "house": self.house,
            "is_retrograde": self.is_retrograde,
            "dms": self.dms,
      }
      
