import argparse
import json
from datetime import datetime
from yaegi.calculations.kundali import KundaliGenerator
from yaegi.calculations.panchang import PanchangGenerator
from yaegi.calculations.yogas import YogaDetector
from yaegi.calculations.compatibility import CompatibilityAnalyzer
from yaegi.calculations.dasha import DashaCalculator


def parse_datetime(date_str: str, time_str: str) -> datetime:
    """Parse date and time strings into datetime object"""
    try:
        date_part = datetime.strptime(date_str, "%Y-%m-%d").date()
        time_part = datetime.strptime(time_str, "%H:%M").time()
        return datetime.combine(date_part, time_part)
    except ValueError as e:
        raise ValueError(f"Invalid date/time format: {e}")


def kundali_command(args):
    """Generate Kundali chart"""
    try:
        birth_datetime = parse_datetime(args.date, args.time)

        generator = KundaliGenerator()
        chart = generator.generate_chart(
            birth_date=birth_datetime,
            latitude=args.latitude,
            longitude=args.longitude,
            timezone=args.timezone,
        )

        if args.format == "json":
            print(json.dumps(chart.to_dict(), indent=2, default=str))
        else:
            print(f"Kundali for {birth_datetime}")
            print(f"Location: {args.latitude}, {args.longitude}")
            print(f"Ascendant: {chart.lagna_lord} at {chart.ascendant:.2f}°")
            print("\nPlanetary Positions:")
            for planet in chart.planets:
                print(f"{planet.name}: {planet.dms} in {planet.rashi} rashi, House {planet.house}")

    except Exception as e:
        print(f"Error generating Kundali: {e}")


def panchang_command(args):
    """Generate Panchang"""
    try:
        date = datetime.strptime(args.date, "%Y-%m-%d")

        generator = PanchangGenerator()
        panchang = generator.generate_panchang(
            date=date,
            latitude=args.latitude,
            longitude=args.longitude,
        )

        if args.format == "json":
            print(json.dumps(panchang, indent=2))
        else:
            print(f"Panchang for {args.date}")
            print(f"Tithi: {panchang['tithi']['name']}")
            print(f"Nakshatra: {panchang['nakshatra']['name']}")
            print(f"Yoga: {panchang['yoga']['name']}")
            print(f"Karana: {panchang['karana']['name']}")
            print(f"Sunrise: {panchang['sunrise']}")
            print(f"Sunset: {panchang['sunset']}")

    except Exception as e:
        print(f"Error generating Panchang: {e}")


def yogas_command(args):
    """Detect yogas in chart"""
    try:
        birth_datetime = parse_datetime(args.date, args.time)

        generator = KundaliGenerator()
        chart = generator.generate_chart(
            birth_date=birth_datetime,
            latitude=args.latitude,
            longitude=args.longitude,
            timezone=args.timezone,
        )

        detector = YogaDetector()
        yogas = detector.detect_all_yogas(chart)

        if args.format == "json":
            print(json.dumps(yogas, indent=2))
        else:
            print(f"Yogas detected: {len(yogas)}")
            for yoga in yogas:
                print(f"\n{yoga['name']} ({yoga['type']})")
                print(f"Description: {yoga['description']}")
                print(f"Strength: {yoga['strength']}")

    except Exception as e:
        print(f"Error detecting yogas: {e}")


def dasha_command(args):
    """Calculate Dasha periods"""
    try:
        birth_datetime = parse_datetime(args.date, args.time)

        generator = KundaliGenerator()
        chart = generator.generate_chart(
            birth_date=birth_datetime,
            latitude=args.latitude,
            longitude=args.longitude,
            timezone=args.timezone,
        )

        calculator = DashaCalculator()
        dasha_system = calculator.calculate_vimshottari_dasha(chart)
        current_dasha = calculator.get_current_dasha(dasha_system)

        if args.format == "json":
            print(json.dumps(current_dasha, indent=2, default=str))
        else:
            if current_dasha["mahadasha"]:
                maha = current_dasha["mahadasha"]
                print(f"Current Mahadasha: {maha['planet']}")
                print(f"Period: {maha['start_date'][:10]} to {maha['end_date'][:10]}")
                print(f"Remaining: {maha['remaining_days']} days")

            if current_dasha["antardasha"]:
                antar = current_dasha["antardasha"]
                print(f"\nCurrent Antardasha: {antar['planet']}")
                print(f"Period: {antar['start_date'][:10]} to {antar['end_date'][:10]}")

    except Exception as e:
        print(f"Error calculating Dasha: {e}")


def compatibility_command(args):
    """Analyze compatibility between two charts"""
    try:
        male_datetime = parse_datetime(args.male_date, args.male_time)
        female_datetime = parse_datetime(args.female_date, args.female_time)

        generator = KundaliGenerator()

        male_chart = generator.generate_chart(
            birth_date=male_datetime,
            latitude=args.male_lat,
            longitude=args.male_lon,
            timezone=args.timezone,
        )

        female_chart = generator.generate_chart(
            birth_date=female_datetime,
            latitude=args.female_lat,
            longitude=args.female_lon,
            timezone=args.timezone,
        )

        analyzer = CompatibilityAnalyzer()
        result = analyzer.analyze_compatibility(male_chart, female_chart)

        if args.format == "json":
            print(json.dumps(result, indent=2, default=str))
        else:
            print(f"Compatibility Analysis")
            print(f"Total Points: {result['total_points']}/36")
            print(f"Percentage: {result['percentage']:.1f}%")
            print(f"Compatibility: {result['compatibility']}")

            if result["recommendations"]:
                print("\nRecommendations:")
                for rec in result["recommendations"]:
                    print(f"- {rec}")

    except Exception as e:
        print(f"Error analyzing compatibility: {e}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Yaegi - Vedic Astrology CLI")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    kundali_parser = subparsers.add_parser("kundali", help="Generate Kundali chart")
    kundali_parser.add_argument("--date", required=True, help="Birth date (YYYY-MM-DD)")
    kundali_parser.add_argument("--time", required=True, help="Birth time (HH:MM)")
    kundali_parser.add_argument("--latitude", type=float, required=True, help="Latitude")
    kundali_parser.add_argument("--longitude", type=float, required=True, help="Longitude")
    kundali_parser.add_argument("--timezone", default="UTC", help="Timezone")

    panchang_parser = subparsers.add_parser("panchang", help="Generate Panchang")
    panchang_parser.add_argument("--date", required=True, help="Date (YYYY-MM-DD)")
    panchang_parser.add_argument("--latitude", type=float, required=True, help="Latitude")
    panchang_parser.add_argument("--longitude", type=float, required=True, help="Longitude")

    yogas_parser = subparsers.add_parser("yogas", help="Detect yogas")
    yogas_parser.add_argument("--date", required=True, help="Birth date (YYYY-MM-DD)")
    yogas_parser.add_argument("--time", required=True, help="Birth time (HH:MM)")
    yogas_parser.add_argument("--latitude", type=float, required=True, help="Latitude")
    yogas_parser.add_argument("--longitude", type=float, required=True, help="Longitude")
    yogas_parser.add_argument("--timezone", default="UTC", help="Timezone")

    dasha_parser = subparsers.add_parser("dasha", help="Calculate Dasha periods")
    dasha_parser.add_argument("--date", required=True, help="Birth date (YYYY-MM-DD)")
    dasha_parser.add_argument("--time", required=True, help="Birth time (HH:MM)")
    dasha_parser.add_argument("--latitude", type=float, required=True, help="Latitude")
    dasha_parser.add_argument("--longitude", type=float, required=True, help="Longitude")
    dasha_parser.add_argument("--timezone", default="UTC", help="Timezone")

    comp_parser = subparsers.add_parser("compatibility", help="Analyze compatibility")
    comp_parser.add_argument("--male-date", required=True, help="Male birth date (YYYY-MM-DD)")
    comp_parser.add_argument("--male-time", required=True, help="Male birth time (HH:MM)")
    comp_parser.add_argument("--male-lat", type=float, required=True, help="Male latitude")
    comp_parser.add_argument("--male-lon", type=float, required=True, help="Male longitude")
    comp_parser.add_argument("--female-date", required=True, help="Female birth date (YYYY-MM-DD)")
    comp_parser.add_argument("--female-time", required=True, help="Female birth time (HH:MM)")
    comp_parser.add_argument("--female-lat", type=float, required=True, help="Female latitude")
    comp_parser.add_argument("--female-lon", type=float, required=True, help="Female longitude")
    comp_parser.add_argument("--timezone", default="UTC", help="Timezone")

    args = parser.parse_args()

    if args.command == "kundali":
        kundali_command(args)
    elif args.command == "panchang":
        panchang_command(args)
    elif args.command == "yogas":
        yogas_command(args)
    elif args.command == "dasha":
        dasha_command(args)
    elif args.command == "compatibility":
        compatibility_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
          
