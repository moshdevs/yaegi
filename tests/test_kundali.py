import pytest
from datetime import datetime
from yaegi.calculations.kundali import KundaliGenerator
from yaegi.models.chart import KundaliChart


class TestKundaliGenerator:
    def setup_method(self):
        self.generator = KundaliGenerator()
        self.test_birth_date = datetime(1990, 5, 15, 14, 30)
        self.test_latitude = 28.6139
        self.test_longitude = 77.2090

    def test_generate_chart(self):
        chart = self.generator.generate_chart(
            birth_date=self.test_birth_date,
            latitude=self.test_latitude,
            longitude=self.test_longitude,
        )

        assert isinstance(chart, KundaliChart)
        assert chart.birth_date == self.test_birth_date
        assert chart.latitude == self.test_latitude
        assert chart.longitude == self.test_longitude
        assert len(chart.planets) > 0
        assert len(chart.houses) == 12

    def test_planetary_positions(self):
        chart = self.generator.generate_chart(
            birth_date=self.test_birth_date,
            latitude=self.test_latitude,
            longitude=self.test_longitude,
        )

        planet_names = [planet.name for planet in chart.planets]
        expected_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

        for planet_name in expected_planets:
            assert planet_name in planet_names

        for planet in chart.planets:
            if planet.name != "Ascendant":
                assert 0 <= planet.longitude < 360
                assert 1 <= planet.rashi <= 12
                assert 1 <= planet.house <= 12

    def test_house_structure(self):
        chart = self.generator.generate_chart(
            birth_date=self.test_birth_date,
            latitude=self.test_latitude,
            longitude=self.test_longitude,
        )

        for house in chart.houses:
            assert 1 <= house.number <= 12
            assert house.lord in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
            assert 1 <= house.rashi <= 12

    def test_divisional_chart(self):
        chart = self.generator.generate_chart(
            birth_date=self.test_birth_date,
            latitude=self.test_latitude,
            longitude=self.test_longitude,
        )

        navamsa = self.generator.generate_divisional_chart(chart, division=9)

        assert isinstance(navamsa, KundaliChart)
        assert navamsa.chart_type == "D9"
        assert len(navamsa.planets) > 0

        for main_planet, nav_planet in zip(chart.planets, navamsa.planets):
            if main_planet.name != "Ascendant":
                assert main_planet.name == nav_planet.name

    def test_get_planet(self):
        chart = self.generator.generate_chart(
            birth_date=self.test_birth_date,
            latitude=self.test_latitude,
            longitude=self.test_longitude,
        )

        sun = chart.get_planet("Sun")
        assert sun is not None
        assert sun.name == "Sun"

        moon = chart.get_planet("moon")
        assert moon is not None
        assert moon.name == "Moon"

        fake_planet = chart.get_planet("NonExistent")
        assert fake_planet is None

    def test_get_house(self):
        chart = self.generator.generate_chart(
            birth_date=self.test_birth_date,
            latitude=self.test_latitude,
            longitude=self.test_longitude,
        )

        first_house = chart.get_house(1)
        assert first_house is not None
        assert first_house.number == 1

        invalid_house = chart.get_house(13)
        assert invalid_house is None

    def test_lagna_lord(self):
        chart = self.generator.generate_chart(
            birth_date=self.test_birth_date,
            latitude=self.test_latitude,
            longitude=self.test_longitude,
        )

        lagna_lord = chart.lagna_lord
        assert lagna_lord in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    def test_chart_to_dict(self):
        chart = self.generator.generate_chart(
            birth_date=self.test_birth_date,
            latitude=self.test_latitude,
            longitude=self.test_longitude,
        )

        chart_dict = chart.to_dict()

        assert isinstance(chart_dict, dict)
        assert "birth_date" in chart_dict
        assert "latitude" in chart_dict
        assert "longitude" in chart_dict
        assert "planets" in chart_dict
        assert "houses" in chart_dict
        assert "ascendant" in chart_dict
        assert "lagna_lord" in chart_dict
