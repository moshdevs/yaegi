import math
from typing import Dict


def angular_distance(lon1: float, lon2: float) -> float:
    """Calculate angular distance between two longitudes"""
    diff: float = abs(lon1 - lon2)
    return min(diff, 360 - diff)


def is_conjunction(lon1: float, lon2: float, orb: float = 8.0) -> bool:
    """Check if two planets are in conjunction within given orb"""
    return angular_distance(lon1, lon2) <= orb


def is_opposition(lon1: float, lon2: float, orb: float = 8.0) -> bool:
    """Check if two planets are in opposition within given orb"""
    diff: float = abs(lon1 - lon2)
    opposition_angle: float = min(
        abs(diff - 180), abs(diff - 180 + 360), abs(diff - 180 - 360)
    )
    return opposition_angle <= orb


def is_trine(lon1: float, lon2: float, orb: float = 8.0) -> bool:
    """Check if two planets are in trine (120° aspect) within given orb"""
    diff: float = abs(lon1 - lon2)
    for angle in (120, 240):
        aspect_diff: float = min(
            abs(diff - angle), abs(diff - angle + 360), abs(diff - angle - 360)
        )
        if aspect_diff <= orb:
            return True
    return False


def is_square(lon1: float, lon2: float, orb: float = 8.0) -> bool:
    """Check if two planets are in square (90° aspect) within given orb"""
    diff: float = abs(lon1 - lon2)
    for angle in (90, 270):
        aspect_diff: float = min(
            abs(diff - angle), abs(diff - angle + 360), abs(diff - angle - 360)
        )
        if aspect_diff <= orb:
            return True
    return False


def is_sextile(lon1: float, lon2: float, orb: float = 6.0) -> bool:
    """Check if two planets are in sextile (60° aspect) within given orb"""
    diff: float = abs(lon1 - lon2)
    for angle in (60, 300):
        aspect_diff: float = min(
            abs(diff - angle), abs(diff - angle + 360), abs(diff - angle - 360)
        )
        if aspect_diff <= orb:
            return True
    return False


def calculate_house_position(planet_lon: float, ascendant: float) -> int:
    """Calculate which house a planet is positioned in"""
    relative_position: float = (planet_lon - ascendant + 360) % 360
    house: int = int(relative_position / 30) + 1
    return house if house <= 12 else house - 12


def get_planetary_strength(longitude: float, rashi: int) -> float:
    """Calculate simplified planetary strength based on sign position"""
    exaltation_degrees: Dict[int, int] = {
        1: 10,  # Aries - Sun exalted at 10°
        2: 27,  # Taurus - Moon exalted at 27°
        3: 28,  # Gemini - Rahu exalted at 28°
        4: 5,  # Cancer - Jupiter exalted at 5°
        5: 10,  # Leo - Sun owns
        6: 15,  # Virgo - Mercury exalted at 15°
        7: 20,  # Libra - Saturn exalted at 20°
        8: 28,  # Scorpio - Mars owns
        9: 5,  # Sagittarius - Jupiter owns
        10: 28,  # Capricorn - Mars exalted at 28°
        11: 20,  # Aquarius - Saturn owns
        12: 27,  # Pisces - Venus exalted at 27°
    }

    degree_in_sign: float = longitude % 30
    exalt_degree: int = exaltation_degrees.get(rashi, 15)

    strength: float = 100 - abs(degree_in_sign - exalt_degree) * 2
    return max(0.0, min(100.0, strength))


def calculate_ashtakavarga_points(
    planet_positions: Dict[str, float], house: int
) -> int:
    """Simplified Ashtakavarga calculation"""
    points: int = 0
    base_points: Dict[str, int] = {
        "Sun": 4,
        "Moon": 5,
        "Mars": 3,
        "Mercury": 4,
        "Jupiter": 5,
        "Venus": 4,
        "Saturn": 2,
    }

    asc: float = planet_positions.get("Ascendant", 0.0)

    for planet, position in planet_positions.items():
        if planet in base_points:
            planet_house: int = calculate_house_position(position, asc)
            if abs(planet_house - house) <= 1 or abs(planet_house - house) >= 11:
                points += base_points[planet]

    return min(points, 8)
