from typing import Any

AYANAMSA_LAHIRI = "LAHIRI"
DEFAULT_AYANAMSA = AYANAMSA_LAHIRI

TIMEZONE_UTC = "UTC"
DEFAULT_TIMEZONE = TIMEZONE_UTC

RASHI_NAMES_EN = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

RASHI_NAMES_HI = [
    "मेष",
    "वृष",
    "मिथुन",
    "कर्क",
    "सिंह",
    "कन्या",
    "तुला",
    "वृश्चिक",
    "धनु",
    "मकर",
    "कुम्भ",
    "मीन",
]

PLANET_NAMES = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
    "Ketu",
    "Ascendant",
]

NAKSHATRA_NAMES = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
]

CONFIG: dict[str, Any] = {
    "ayanamsa": DEFAULT_AYANAMSA,
    "timezone": DEFAULT_TIMEZONE,
    "locale": "en",
    "cache_enabled": True,
    "log_level": "INFO",
}
