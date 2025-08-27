from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from yaegi.models.planet import Planet
from yaegi.models.house import House


@dataclass
class KundaliChart:
    birth_date: datetime
    latitude: float
    longitude: float
    timezone: str
    ayanamsa: float = 0.0
    planets: list[Planet] = field(default_factory=list)
    houses: list[House] = field(default_factory=list)
    ascendant: float = 0.0
    chart_type: str = "lagna"

    def get_planet(self, name: str) -> Optional[Planet]:
        for planet in self.planets:
            if planet.name.lower() == name.lower():
                return planet
        return None

    def get_house(self, number: int) -> Optional[House]:
        for house in self.houses:
            if house.number == number:
                return house
        return None

    def get_planets_in_house(self, house_number: int) -> list[Planet]:
        return [planet for planet in self.planets if planet.house == house_number]

    def get_planets_in_rashi(self, rashi: int) -> list[Planet]:
        return [planet for planet in self.planets if planet.rashi == rashi]

    @property
    def lagna_lord(self) -> str:
        lagna_rashi = int(self.ascendant // 30) + 1
        lords = {
            1: "Mars",
            2: "Venus",
            3: "Mercury",
            4: "Moon",
            5: "Sun",
            6: "Mercury",
            7: "Venus",
            8: "Mars",
            9: "Jupiter",
            10: "Saturn",
            11: "Saturn",
            12: "Jupiter",
        }
        return lords.get(lagna_rashi, "Unknown")

    def to_dict(self) -> dict[str, any]:
        return {
            "birth_date": self.birth_date.isoformat(),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": self.timezone,
            "ayanamsa": self.ayanamsa,
            "ascendant": self.ascendant,
            "lagna_lord": self.lagna_lord,
            "chart_type": self.chart_type,
            "planets": [planet.to_dict() for planet in self.planets],
            "houses": [house.to_dict() for house in self.houses],
        }
      
