# Yaegi - Vedic Astrology Library

[![PyPI version](https://badge.fury.io/py/yaegi.svg)](https://badge.fury.io/py/yaegi)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive, modern Python library for Vedic Astrology (Jyotish) calculations. Yaegi provides accurate astronomical calculations, Kundali generation, Panchang, Dasha systems, and compatibility analysis.

## Features

- **Astronomical Calculations**: Accurate planetary positions using simplified ephemeris
- **Kundali Generation**: Birth charts with planetary positions and house calculations
- **Divisional Charts**: Support for Navamsa (D9), Dashamsa (D10), and other divisional charts
- **Panchang System**: Daily Panchang with Tithi, Nakshatra, Yoga, and Karana
- **Dasha Calculations**: Complete Vimshottari Dasha system with Mahadasha and Antardasha
- **Yoga Detection**: Automatic detection of Raj Yogas, Dhan Yogas, and other combinations
- **Compatibility Analysis**: Guna Milan for marriage compatibility (36-point system)
- **CLI Interface**: Command-line tool for quick calculations
- **Multiple Output Formats**: JSON, dictionary, and formatted text output

## Installation

```bash
pip install yaegi
```

## Quick Start

### Generate a Kundali

```python
from datetime import datetime
from yaegi import KundaliGenerator

# Create a Kundali
generator = KundaliGenerator()
chart = generator.generate_chart(
    birth_date=datetime(1990, 5, 15, 14, 30),
    latitude=28.6139,   # Delhi
    longitude=77.2090,
    timezone="Asia/Kolkata"
)

# Access planetary positions
for planet in chart.planets:
    print(f"{planet.name}: {planet.dms} in House {planet.house}")

# Get chart as dictionary
chart_data = chart.to_dict()
```

### Generate Panchang

```python
from datetime import datetime
from yaegi import PanchangGenerator

generator = PanchangGenerator()
panchang = generator.generate_panchang(
    date=datetime(2024, 1, 15),
    latitude=28.6139,
    longitude=77.2090
)

print(f"Tithi: {panchang['tithi']['name']}")
print(f"Nakshatra: {panchang['nakshatra']['name']}")
print(f"Yoga: {panchang['yoga']['name']}")
```

### Detect Yogas

```python
from yaegi import YogaDetector

detector = YogaDetector()
yogas = detector.detect_all_yogas(chart)

for yoga in yogas:
    print(f"{yoga['name']}: {yoga['description']}")
```

### Calculate Dasha Periods

```python
from yaegi.calculations.dasha import DashaCalculator

calculator = DashaCalculator()
dasha_system = calculator.calculate_vimshottari_dasha(chart)
current_dasha = calculator.get_current_dasha(dasha_system)

print(f"Current Mahadasha: {current_dasha['mahadasha']['planet']}")
print(f"Current Antardasha: {current_dasha['antardasha']['planet']}")
```

### Compatibility Analysis

```python
from yaegi import CompatibilityAnalyzer

analyzer = CompatibilityAnalyzer()
result = analyzer.analyze_compatibility(male_chart, female_chart)

print(f"Compatibility Score: {result['total_points']}/36")
print(f"Compatibility Level: {result['compatibility']}")
```

## Command Line Interface

Yaegi includes a powerful CLI for quick calculations:

### Generate Kundali
```bash
yaegi kundali --date 1990-05-15 --time 14:30 --latitude 28.6139 --longitude 77.2090
```

### Generate Panchang
```bash
yaegi panchang --date 2024-01-15 --latitude 28.6139 --longitude 77.2090
```

### Detect Yogas
```bash
yaegi yogas --date 1990-05-15 --time 14:30 --latitude 28.6139 --longitude 77.2090 --format json
```

### Calculate Dasha
```bash
yaegi dasha --date 1990-05-15 --time 14:30 --latitude 28.6139 --longitude 77.2090
```

### Compatibility Analysis
```bash
yaegi compatibility \
  --male-date 1990-05-15 --male-time 14:30 --male-lat 28.61 --male-lon 77.21 \
  --female-date 1992-08-20 --female-time 10:15 --female-lat 28.61 --female-lon 77.21
```

## Advanced Usage

### Divisional Charts

```python
# Generate Navamsa chart (D9)
navamsa = generator.generate_divisional_chart(chart, division=9)

# Generate Dashamsa chart (D10) for career
dashamsa = generator.generate_divisional_chart(chart, division=10)
```

### Custom Ayanamsa

```python
from yaegi.core.astronomy import AstronomyEngine

# Use custom ayanamsa
astronomy = AstronomyEngine(ayanamsa="LAHIRI")
```

### Planetary Strengths

```python
from yaegi.core.mathutils import get_planetary_strength

for planet in chart.planets:
    strength = get_planetary_strength(planet.longitude, planet.rashi)
    print(f"{planet.name} strength: {strength}")
```

## Configuration

Yaegi supports various configuration options:

```python
from yaegi.config.settings import CONFIG

# Modify global settings
CONFIG["locale"] = "hi"  # Hindi names
CONFIG["ayanamsa"] = "LAHIRI"
CONFIG["cache_enabled"] = True
```

## Supported Features

### Astronomical Calculations
- Planetary positions (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn)
- Lunar nodes (Rahu, Ketu)
- Ascendant calculation
- House systems (Equal House, Placidus)
- Sidereal zodiac with Lahiri Ayanamsa

### Chart Systems
- Lagna Chart (D1)
- Navamsa Chart (D9)
- All divisional charts (D1-D60)
- House lord calculations
- Planetary aspects

### Panchang Elements
- Tithi (Lunar day)
- Nakshatra (Lunar mansion)
- Yoga (Solar-Lunar combination)
- Karana (Half-tithi)
- Sunrise/Sunset times

### Dasha Systems
- Vimshottari Dasha (120-year cycle)
- Mahadasha periods
- Antardasha periods
- Current period identification

### Yoga Detection
- Raj Yogas (Royal combinations)
- Dhan Yogas (Wealth combinations)
- Panch Mahapurush Yogas
- Neecha Bhanga Yogas
- Gajakesari Yoga
- Many other classical yogas

### Compatibility Analysis
- Complete Guna Milan (36 points)
- Individual Guna analysis
- Compatibility recommendations
- Dosha identification

## Requirements

- Python 3.8+
- No external dependencies for core functionality

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [https://yaegi.readthedocs.io](https://yaegi.readthedocs.io)
- Issues: [https://github.com/yaegi/yaegi/issues](https://github.com/yaegi/yaegi/issues)
- Discussions: [https://github.com/yaegi/yaegi/discussions](https://github.com/yaegi/yaegi/discussions)

## Acknowledgments

- Vedic Astrology principles and calculations
- Swiss Ephemeris for astronomical accuracy
- The Python astronomy community
