"""
Basic usage examples for Yaegi Vedic Astrology Library
"""

from datetime import datetime
import json

from yaegi import KundaliGenerator, PanchangGenerator, YogaDetector, CompatibilityAnalyzer
from yaegi.calculations.dasha import DashaCalculator


def generate_sample_kundali():
    """Generate a sample Kundali chart"""
    print("=== Generating Sample Kundali ===")
    birth_date = datetime(1990, 5, 15, 14, 30)
    latitude = 28.6139
    longitude = 77.2090

    generator = KundaliGenerator()
    chart = generator.generate_chart(
        birth_date=birth_date, latitude=latitude, longitude=longitude, timezone="Asia/Kolkata"
    )

    print(f"Birth Date: {chart.birth_date}")
    print(f"Location: {chart.latitude}, {chart.longitude}")
    print(f"Ascendant: {chart.ascendant:.2f}° ({chart.lagna_lord} Lagna)\n")

    print("Planetary Positions:")
    print("-" * 60)
    for planet in chart.planets:
        if planet.name != "Ascendant":
            print(
                f"{planet.name:10} | {planet.dms:12} | Rashi {planet.rashi:2} | House {planet.house:2}"
            )
    print()

    print("House Information:")
    print("-" * 40)
    for house in chart.houses:
        planets_in_house = ", ".join(house.planets) if house.planets else "Empty"
        print(f"House {house.number:2} | Lord: {house.lord:8} | Planets: {planets_in_house}")

    return chart


def generate_sample_panchang():
    """Generate sample Panchang"""
    print("\n=== Generating Sample Panchang ===")
    date = datetime(2024, 1, 15)
    latitude = 28.6139
    longitude = 77.2090

    generator = PanchangGenerator()
    panchang = generator.generate_panchang(date=date, latitude=latitude, longitude=longitude)

    print(f"Date: {panchang['date']}")
    print(f"Location: {panchang['location']['latitude']}, {panchang['location']['longitude']}\n")
    print(f"Tithi: {panchang['tithi']['name']}")
    print(f"Nakshatra: {panchang['nakshatra']['name']}")
    print(f"Yoga: {panchang['yoga']['name']}")
    print(f"Karana: {panchang['karana']['name']}")
    print(f"Sunrise: {panchang['sunrise']}")
    print(f"Sunset: {panchang['sunset']}")
    print(f"Moon Phase: {panchang['moon_phase']:.1f}%")

    return panchang


def detect_yogas_example(chart):
    """Detect yogas in the chart"""
    print("\n=== Detecting Yogas ===")
    detector = YogaDetector()
    yogas = detector.detect_all_yogas(chart)

    if yogas:
        print(f"Found {len(yogas)} yoga(s):\n")
        for yoga in yogas:
            print(f"Name: {yoga['name']}")
            print(f"Type: {yoga['type']}")
            print(f"Description: {yoga['description']}")
            print(f"Strength: {yoga['strength']}")
            print(f"Planets involved: {', '.join(yoga['planets'])}")
            print(f"Houses involved: {', '.join(map(str, yoga['houses']))}")
            print("-" * 50)
    else:
        print("No major yogas detected in this chart.")

    return yogas


def calculate_dasha_example(chart):
    """Calculate Dasha periods"""
    print("\n=== Calculating Dasha Periods ===")
    calculator = DashaCalculator()
    dasha_system = calculator.calculate_vimshottari_dasha(chart)
    current_dasha = calculator.get_current_dasha(dasha_system)

    if current_dasha["mahadasha"]:
        maha = current_dasha["mahadasha"]
        print(f"Current Mahadasha: {maha['planet']}")
        print(f"Start Date: {maha['start_date'][:10]}")
        print(f"End Date: {maha['end_date'][:10]}")
        print(f"Duration: {maha['duration_years']:.1f} years")
        print(f"Remaining: {maha['remaining_days']} days")
        predictions = calculator.get_dasha_predictions(maha["planet"])
        print(f"\nGeneral Predictions: {predictions['general']}")
        print(f"Career: {predictions['career']}")

    if current_dasha["antardasha"]:
        antar = current_dasha["antardasha"]
        print(f"\nCurrent Antardasha: {antar['planet']}")
        print(f"Period: {antar['start_date'][:10]} to {antar['end_date'][:10]}")
        print(f"Remaining: {antar['remaining_days']} days")

    return dasha_system


def compatibility_example():
    """Demonstrate compatibility analysis"""
    print("\n=== Compatibility Analysis ===")
    generator = KundaliGenerator()

    male_chart = generator.generate_chart(
        birth_date=datetime(1990, 5, 15, 14, 30), latitude=28.6139, longitude=77.2090
    )
    female_chart = generator.generate_chart(
        birth_date=datetime(1992, 8, 20, 10, 15), latitude=28.6139, longitude=77.2090
    )

    analyzer = CompatibilityAnalyzer()
    result = analyzer.analyze_compatibility(male_chart, female_chart)

    print(f"Compatibility Score: {result['total_points']}/36 ({result['percentage']:.1f}%)")
    print(f"Compatibility Level: {result['compatibility']}\n")

    print("Individual Guna Analysis:")
    print("-" * 40)
    for guna, details in result["details"].items():
        if isinstance(details, dict) and "points" in details:
            print(
                f"{guna.title():15} | {details['points']:2}/{details['max_points']:2} | "
                f"{'✓' if details.get('compatible', False) else '✗'}"
            )

    if result["recommendations"]:
        print("\nRecommendations:")
        for rec in result["recommendations"]:
            print(f"• {rec}")

    return result


def main():
    """Run all examples"""
    print("Yaegi Vedic Astrology Library - Example Usage")
    print("=" * 60)

    chart = generate_sample_kundali()
    panchang = generate_sample_panchang()
    yogas = detect_yogas_example(chart)
    dasha_system = calculate_dasha_example(chart)
    compatibility = compatibility_example()

    print("\n=== Exporting Sample Data ===")
    sample_data = {"chart": chart.to_dict(), "panchang": panchang, "yogas": yogas, "compatibility": compatibility}

    with open("sample_output.json", "w") as f:
        json.dump(sample_data, f, indent=2, default=str)

    print("Sample data exported to 'sample_output.json'")
    print("\nExample completed successfully!")


if __name__ == "__main__":
    main()
