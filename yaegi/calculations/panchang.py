from datetime import datetime
from typing import Dict, Any, Tuple
from yaegi.core.astronomy import AstronomyEngine
from yaegi.core.conversions import datetime_to_julian_day
from yaegi.config.settings import NAKSHATRA_NAMES


class PanchangGenerator:
    """Generate Panchang elements (Tithi, Nakshatra, Yoga, Karana) for a given date and location."""

    def __init__(self) -> None:
        self.astronomy = AstronomyEngine()

    def calculate_tithi(self, sun_lon: float, moon_lon: float) -> Tuple[int, str]:
        """Calculate Tithi based on Sun and Moon sidereal longitudes."""
        moon_phase = (moon_lon - sun_lon + 360) % 360
        tithi_num = int(moon_phase / 12) + 1

        tithi_names = [
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
            "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
            "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
        ]

        if tithi_num > 15:
            tithi_num -= 15
            paksha = "Krishna"
        else:
            paksha = "Shukla"

        tithi_name = tithi_names[min(tithi_num - 1, 14)]
        return tithi_num, f"{paksha} {tithi_name}"

    def calculate_nakshatra(self, moon_lon: float) -> Tuple[int, str]:
        """Determine Nakshatra number and name from Moon longitude."""
        nakshatra_num = int(moon_lon * 27 / 360) + 1
        nakshatra_num = min(nakshatra_num, 27)
        nakshatra_name = NAKSHATRA_NAMES[nakshatra_num - 1]
        return nakshatra_num, nakshatra_name

    def calculate_yoga(self, sun_lon: float, moon_lon: float) -> Tuple[int, str]:
        """Determine Yoga number and name from Sun and Moon longitudes."""
        yoga_value = (sun_lon + moon_lon) % 360
        yoga_num = int(yoga_value * 27 / 360) + 1
        yoga_names = [
            "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
            "Sukarman", "Dhriti", "Shoola", "Ganda", "Vriddhi", "Dhruva",
            "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyas",
            "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
            "Brahma", "Mahendra", "Vaidhriti"
        ]
        yoga_name = yoga_names[min(yoga_num - 1, 26)]
        return yoga_num, yoga_name

    def calculate_karana(self, tithi_num: int) -> Tuple[int, str]:
        """Determine Karana number and name based on Tithi."""
        if tithi_num == 30:
            return 4, "Chatushpada"  # Amavasya
        if tithi_num == 15:
            return 3, "Naga"  # Purnima

        karana_names = ["Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti"]
        karana_num = ((tithi_num - 1) % 7) + 1
        return karana_num, karana_names[karana_num - 1]

    def calculate_sunrise(self, jd: float, latitude: float, longitude: float) -> str:
        """Approximate sunrise time based on longitude."""
        hour = 6 + (longitude / 15.0)
        return f"{int(hour):02d}:{int((hour % 1) * 60):02d}"

    def calculate_sunset(self, jd: float, latitude: float, longitude: float) -> str:
        """Approximate sunset time based on longitude."""
        hour = 18 + (longitude / 15.0)
        return f"{int(hour):02d}:{int((hour % 1) * 60):02d}"

    def generate_panchang(self, date: datetime, latitude: float, longitude: float) -> Dict[str, Any]:
        """Generate complete Panchang for a given date and location."""
        jd = datetime_to_julian_day(date)

        # Sidereal longitudes
        sun_lon = self.astronomy.get_sidereal_longitude("Sun", jd)
        moon_lon = self.astronomy.get_sidereal_longitude("Moon", jd)

        # Panchang elements
        tithi_num, tithi_name = self.calculate_tithi(sun_lon, moon_lon)
        nakshatra_num, nakshatra_name = self.calculate_nakshatra(moon_lon)
        yoga_num, yoga_name = self.calculate_yoga(sun_lon, moon_lon)
        karana_num, karana_name = self.calculate_karana(tithi_num)

        # Sunrise and sunset (simplified)
        sunrise_time = self.calculate_sunrise(jd, latitude, longitude)
        sunset_time = self.calculate_sunset(jd, latitude, longitude)

        return {
            "date": date.strftime("%Y-%m-%d"),
            "location": {"latitude": latitude, "longitude": longitude},
            "tithi": {"number": tithi_num, "name": tithi_name},
            "nakshatra": {"number": nakshatra_num, "name": nakshatra_name},
            "yoga": {"number": yoga_num, "name": yoga_name},
            "karana": {"number": karana_num, "name": karana_name},
            "sunrise": sunrise_time,
            "sunset": sunset_time,
            "moon_phase": ((moon_lon - sun_lon + 360) % 360) / 360 * 100
      }
      
