import math
from typing import Dict, List
from yaegi.core.conversions import datetime_to_julian_day
from yaegi.config.settings import DEFAULT_AYANAMSA


class AstronomyEngine:
    """Core astronomical calculations using simplified ephemeris"""

    PLANET_SPEEDS: Dict[str, float] = {
        "Sun": 0.9856,
        "Moon": 13.1763,
        "Mars": 0.5240,
        "Mercury": 1.3833,
        "Jupiter": 0.0831,
        "Venus": 1.6022,
        "Saturn": 0.0334,
    }

    def __init__(self, ayanamsa: str = DEFAULT_AYANAMSA) -> None:
        self.ayanamsa_type: str = ayanamsa

    def get_ayanamsa(self, julian_day: float) -> float:
        """Calculate Lahiri ayanamsa for given Julian Day"""
        t: float = (julian_day - 2451545.0) / 36525.0
        ayanamsa: float = 23.85 + 0.013972 * t
        return ayanamsa

    def get_planet_longitude(self, planet: str, julian_day: float) -> float:
        """Calculate tropical longitude for planet at given Julian Day"""
        t: float = (julian_day - 2451545.0) / 36525.0
        longitudes: Dict[str, float] = {
            "Sun": 280.4665 + 36000.7698 * t,
            "Moon": 218.3165 + 481267.8813 * t,
            "Mars": 355.4330 + 19140.2993 * t,
            "Mercury": 252.2510 + 149472.6746 * t,
            "Jupiter": 34.3515 + 3034.9057 * t,
            "Venus": 181.9798 + 58517.8156 * t,
            "Saturn": 50.0774 + 1222.1138 * t,
        }
        return longitudes.get(planet, 0.0) % 360.0

    def get_sidereal_longitude(self, planet: str, julian_day: float) -> float:
        """Calculate sidereal longitude for planet"""
        tropical_lon: float = self.get_planet_longitude(planet, julian_day)
        ayanamsa: float = self.get_ayanamsa(julian_day)
        return (tropical_lon - ayanamsa) % 360.0

    def calculate_ascendant(
        self, julian_day: float, latitude: float, longitude: float
    ) -> float:
        """Calculate ascendant for given coordinates and time"""
        t: float = (julian_day - 2451545.0) / 36525.0
        gmst: float = 280.46061837 + 360.98564736629 * (julian_day - 2451545.0)
        gmst %= 360.0

        lst: float = (gmst + longitude) % 360.0

        epsilon: float = 23.4393 - 0.0130 * t
        epsilon_rad: float = math.radians(epsilon)
        lat_rad: float = math.radians(latitude)
        lst_rad: float = math.radians(lst)

        y: float = math.sin(lst_rad)
        x: float = math.cos(lst_rad) * math.cos(epsilon_rad) + math.tan(lat_rad) * math.sin(epsilon_rad)
        ascendant: float = math.degrees(math.atan2(y, x))

        if ascendant < 0:
            ascendant += 360.0

        ayanamsa: float = self.get_ayanamsa(julian_day)
        return (ascendant - ayanamsa) % 360.0

    def get_all_planets(self, julian_day: float) -> Dict[str, float]:
        """Get sidereal longitudes for all major planets"""
        return {planet: self.get_sidereal_longitude(planet, julian_day) for planet in self.PLANET_SPEEDS}

    def calculate_houses(self, ascendant: float, method: str = "placidus") -> List[float]:
        """Calculate house cusps using equal house system"""
        return [(ascendant + i * 30) % 360.0 for i in range(12)]
  
