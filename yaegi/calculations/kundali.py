from datetime import datetime
from typing import List
from yaegi.models.chart import KundaliChart
from yaegi.models.planet import Planet
from yaegi.models.house import House
from yaegi.core.astronomy import AstronomyEngine
from yaegi.core.conversions import datetime_to_julian_day
from yaegi.core.mathutils import calculate_house_position


class KundaliGenerator:
    """Generate Vedic astrology charts (Kundali) from birth details."""

    def __init__(self) -> None:
        self.astronomy = AstronomyEngine()

    def generate_chart(
        self,
        birth_date: datetime,
        latitude: float,
        longitude: float,
        timezone: str = "UTC",
    ) -> KundaliChart:
        """Generate complete Kundali chart with planets and houses."""

        jd = datetime_to_julian_day(birth_date)

        # Calculate ascendant
        ascendant = self.astronomy.calculate_ascendant(jd, latitude, longitude)

        # Get planetary sidereal longitudes
        planet_positions = self.astronomy.get_all_planets(jd)

        # Create Planet objects
        planets: List[Planet] = []
        for name, lon in planet_positions.items():
            house_num = calculate_house_position(lon, ascendant)
            planets.append(
                Planet(
                    name=name,
                    longitude=lon,
                    house=house_num,
                )
            )

        # Add Ascendant as a "planet"
        planets.append(
            Planet(
                name="Ascendant",
                longitude=ascendant,
                house=1,
            )
        )

        # Calculate house cusps
        house_cusps = self.astronomy.calculate_houses(ascendant)

        # Define house lords based on rashi
        house_lords = {
            1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon",
            5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars",
            9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter",
        }

        # Create House objects
        houses: List[House] = []
        for i, cusp in enumerate(house_cusps):
            house_num = i + 1
            rashi = int(cusp // 30) + 1
            lord = house_lords.get(rashi, "Unknown")

            house = House(
                number=house_num,
                lord=lord,
                rashi=rashi,
                degree=cusp % 30,
                cusp=cusp,
            )

            # Assign planets to their respective houses
            for planet in planets:
                if planet.house == house_num:
                    house.add_planet(planet.name)

            houses.append(house)

        # Build the final Kundali chart
        chart = KundaliChart(
            birth_date=birth_date,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            ayanamsa=self.astronomy.get_ayanamsa(jd),
            planets=planets,
            houses=houses,
            ascendant=ascendant,
        )

        return chart

    def generate_divisional_chart(
        self, birth_chart: KundaliChart, division: int
    ) -> KundaliChart:
        """Generate divisional charts (D2, D9, D10, etc.) from the main chart."""

        divisional_planets: List[Planet] = []

        for planet in birth_chart.planets:
            if planet.name == "Ascendant":
                continue

            # Extract sign position and rashi number
            sign_position = planet.longitude % 30
            rashi_num = int(planet.longitude // 30)

            # Calculate divisional longitude
            if division == 9:  # Navamsa
                navamsa_rashi = ((rashi_num * 9) + int(sign_position * 9 / 30)) % 12
                divisional_longitude = navamsa_rashi * 30 + (sign_position * 9 % 30)
            else:
                divisional_longitude = ((rashi_num * division) % 12) * 30 + (
                    sign_position * division % 30
                )

            divisional_longitude %= 360

            # Create Planet object for divisional chart
            divisional_planets.append(
                Planet(
                    name=planet.name,
                    longitude=divisional_longitude,
                    house=calculate_house_position(divisional_longitude, birth_chart.ascendant),
                )
            )

        # Build divisional chart
        divisional_chart = KundaliChart(
            birth_date=birth_chart.birth_date,
            latitude=birth_chart.latitude,
            longitude=birth_chart.longitude,
            timezone=birth_chart.timezone,
            ayanamsa=birth_chart.ayanamsa,
            planets=divisional_planets,
            houses=birth_chart.houses,
            ascendant=birth_chart.ascendant,
            chart_type=f"D{division}",
        )

        return divisional_chart
