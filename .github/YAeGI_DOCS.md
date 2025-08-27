# Yaegi: Vedic Astrology (Jyotish) Library

## 📖 Overview

Yaegi is a comprehensive **Vedic Astrology (Jyotish) library for
Python**.\
It provides tools for astronomical and astrological calculations such as
**kundali (birth chart), dasha (planetary periods), panchang (Hindu
calendar), yogas, and compatibility**.

This library is designed for developers, astrologers, and researchers
who want to integrate Jyotish-based astrology calculations into their
Python applications.

------------------------------------------------------------------------

## ⚡ Features

-   Compute **Kundali (Janma Patrika)** with houses, planets, and signs.
-   Calculate **Dashas (Mahadasha, Antardasha, etc.)**.
-   Generate **Panchang (Tithi, Nakshatra, Yoga, Karana, Vaar)**.
-   Detect **Yogas** from planetary combinations.
-   Astrology-based **compatibility analysis**.
-   CLI (Command Line Interface) support.
-   Extensible and modular design.

------------------------------------------------------------------------

## 📦 Installation

``` bash
pip install yaegi
```

Or install from source:

``` bash
git clone https://github.com/moshdevs/yaegi.git
cd yaegi
pip install .
```

------------------------------------------------------------------------

## 🚀 Quick Usage

### Example: Basic Kundali

``` python
from yaegi.calculations.kundali import Kundali

# Example birth details
birth = Kundali(date="1998-08-27", time="14:35", place="Delhi, India")

print(birth.get_chart())
```

### Example: Panchang

``` python
from yaegi.calculations.panchang import Panchang

today = Panchang(date="2025-08-27", place="Delhi, India")
print(today.details())
```

### Example: CLI

``` bash
yaegi chart --date 1998-08-27 --time 14:35 --place "Delhi, India"
```

------------------------------------------------------------------------

## 🏗️ Project Structure

    yaegi/
    ├── calculations/   # Kundali, Dasha, Panchang, Compatibility, Yogas
    ├── core/           # Astronomy, Math utils, Conversions
    ├── models/         # Chart, Planet, House, Dasha models
    ├── data/           # Constants, Yogas definitions
    ├── cli/            # Command Line Interface
    ├── examples/       # Example scripts
    └── tests/          # Unit tests

------------------------------------------------------------------------

## 📚 Modules

### 1. `yaegi.calculations`

-   **kundali.py** → Janma Kundali generation
-   **dasha.py** → Mahadasha & Antardasha
-   **panchang.py** → Hindu calendar details
-   **compatibility.py** → Marriage/relationship matching
-   **yogas.py** → Planetary yogas

### 2. `yaegi.core`

-   **astronomy.py** → Astronomical calculations
-   **mathutils.py** → Utility math functions
-   **conversions.py** → Time, date, coordinate conversions

### 3. `yaegi.models`

-   **chart.py** → Kundali chart structure
-   **planet.py** → Planet objects
-   **house.py** → Astrological houses
-   **dasha.py** → Dasha periods

### 4. `yaegi.data`

-   **constants.py** → Astrological constants
-   **yogas.json** → Predefined yogas

------------------------------------------------------------------------

## ✅ Testing

Run unit tests with:

``` bash
pytest tests/
```

------------------------------------------------------------------------

## 🤝 Contribution

We welcome contributions!\
- Fork the repo - Create a feature branch
(`git checkout -b feature-name`) - Commit your changes
(`git commit -m 'Added feature'`) - Push and create a PR

See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for more details.

------------------------------------------------------------------------

## 📜 License

MIT License © 2025\
See [LICENSE](LICENSE) for details.

------------------------------------------------------------------------

## 🌟 Credits

Developed with ❤️ for the Vedic Astrology community.
