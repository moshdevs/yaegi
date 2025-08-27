from typing import List, Dict, Any
from yaegi.models.chart import KundaliChart
from yaegi.core.mathutils import is_conjunction


class YogaDetector:
    """Detect various yogas in Kundali charts"""

    def detect_all_yogas(self, chart: KundaliChart) -> List[Dict[str, Any]]:
        yogas = []
        yogas.extend(self.detect_raj_yogas(chart))
        yogas.extend(self.detect_dhan_yogas(chart))
        yogas.extend(self.detect_panch_mahapurush_yogas(chart))
        yogas.extend(self.detect_neecha_bhanga_yogas(chart))
        yogas.extend(self.detect_gajakesari_yoga(chart))
        yogas.extend(self.detect_chandra_mangal_yoga(chart))
        return yogas

    def detect_raj_yogas(self, chart: KundaliChart) -> List[Dict[str, Any]]:
        yogas = []
        kendra_houses = [1, 4, 7, 10]
        trikona_houses = [1, 5, 9]

        for house in chart.houses:
            if house.number in kendra_houses and house.is_occupied:
                for planet_name in house.planets:
                    for trikona in trikona_houses:
                        trikona_house = chart.get_house(trikona)
                        if trikona_house and trikona_house.lord == planet_name:
                            yogas.append(
                                {
                                    "name": "Raj Yoga",
                                    "type": "benefic",
                                    "description": f"{planet_name} in house {house.number} and lord of house {trikona}",
                                    "strength": "strong",
                                    "planets": [planet_name],
                                    "houses": [house.number, trikona],
                                }
                            )
        return yogas

    def detect_dhan_yogas(self, chart: KundaliChart) -> List[Dict[str, Any]]:
        yogas = []
        second_house = chart.get_house(2)
        eleventh_house = chart.get_house(11)

        if second_house and eleventh_house:
            if (
                second_house.lord in eleventh_house.planets
                and eleventh_house.lord in second_house.planets
            ):
                yogas.append(
                    {
                        "name": "Dhan Yoga",
                        "type": "benefic",
                        "description": "2nd and 11th house lords in mutual exchange",
                        "strength": "strong",
                        "planets": [second_house.lord, eleventh_house.lord],
                        "houses": [2, 11],
                    }
                )
        return yogas

    def detect_panch_mahapurush_yogas(self, chart: KundaliChart) -> List[Dict[str, Any]]:
        yogas = []
        exaltation_signs = {"Mars": 10, "Mercury": 6, "Jupiter": 4, "Venus": 12, "Saturn": 7}
        own_signs = {"Mars": [1, 8], "Mercury": [3, 6], "Jupiter": [9, 12], "Venus": [2, 7], "Saturn": [10, 11]}
        yoga_names = {
            "Mars": "Ruchaka Yoga",
            "Mercury": "Bhadra Yoga",
            "Jupiter": "Hamsa Yoga",
            "Venus": "Malavya Yoga",
            "Saturn": "Sasha Yoga",
        }

        for planet_name in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            planet = chart.get_planet(planet_name)
            if planet and planet.house in [1, 4, 7, 10]:
                exalted = planet.rashi == exaltation_signs.get(planet_name, 0)
                own_sign = planet.rashi in own_signs.get(planet_name, [])
                if exalted or own_sign:
                    yogas.append(
                        {
                            "name": yoga_names[planet_name],
                            "type": "benefic",
                            "description": f"{planet_name} in kendra and {'exalted' if exalted else 'own sign'}",
                            "strength": "very strong",
                            "planets": [planet_name],
                            "houses": [planet.house],
                        }
                    )
        return yogas

    def detect_neecha_bhanga_yogas(self, chart: KundaliChart) -> List[Dict[str, Any]]:
        yogas = []
        debilitation_signs = {
            "Sun": 7,
            "Moon": 8,
            "Mars": 4,
            "Mercury": 12,
            "Jupiter": 10,
            "Venus": 6,
            "Saturn": 1,
        }
        exalt_lords = {7: "Saturn", 8: "Jupiter", 4: "Moon", 12: "Jupiter", 10: "Mars", 6: "Mercury", 1: "Sun"}

        for planet_name, debil_sign in debilitation_signs.items():
            planet = chart.get_planet(planet_name)
            if planet and planet.rashi == debil_sign:
                exalt_lord_name = exalt_lords.get(debil_sign)
                exalt_planet = chart.get_planet(exalt_lord_name) if exalt_lord_name else None
                if exalt_planet and exalt_planet.house in [1, 4, 7, 10]:
                    yogas.append(
                        {
                            "name": "Neecha Bhanga Yoga",
                            "type": "benefic",
                            "description": f"{planet_name} debilitation cancelled",
                            "strength": "medium",
                            "planets": [planet_name],
                            "houses": [planet.house],
                        }
                    )
        return yogas

    def detect_gajakesari_yoga(self, chart: KundaliChart) -> List[Dict[str, Any]]:
        yogas = []
        jupiter = chart.get_planet("Jupiter")
        moon = chart.get_planet("Moon")

        if jupiter and moon:
            diff = (jupiter.house - moon.house) % 12
            if diff in [1, 4, 7, 10]:
                yogas.append(
                    {
                        "name": "Gajakesari Yoga",
                        "type": "benefic",
                        "description": "Jupiter and Moon in kendra from each other",
                        "strength": "strong",
                        "planets": ["Jupiter", "Moon"],
                        "houses": [jupiter.house, moon.house],
                    }
                )
        return yogas

    def detect_chandra_mangal_yoga(self, chart: KundaliChart) -> List[Dict[str, Any]]:
        yogas = []
        moon = chart.get_planet("Moon")
        mars = chart.get_planet("Mars")

        if moon and mars and is_conjunction(moon.longitude, mars.longitude, orb=10):
            yogas.append(
                {
                    "name": "Chandra Mangal Yoga",
                    "type": "mixed",
                    "description": "Moon and Mars in conjunction",
                    "strength": "medium",
                    "planets": ["Moon", "Mars"],
                    "houses": [moon.house, mars.house],
                }
            )
        return yogas
  
