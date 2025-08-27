# 🌌 Yaegi – Vedic Astrology Library  

<p align="center">
  <img width="250" src="./assets/yaegi.webp" />
</p>

<p align="center">
  <b>A modern Python library for Vedic Astrology (Jyotish)</b> – Accurate astronomy, Kundali generation, Panchang, Dashas & compatibility, all in one.
</p>

<p align="center">
  [<a href="https://github.com/moshdevs/yaegi/blob/master/guide/docs.md">📖 Docs</a>] 
  [<a href="https://github.com/moshdevs/yaegi/discussions">💬 Discussions</a>] 
  [<a href="https://pypi.org/project/yaegi/">⬇️ PyPI</a>] 
</p>

<p align="center">
  <a href="https://badge.fury.io/py/yaegi"><img src="https://badge.fury.io/py/yaegi.svg"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
</p>

---

> [!NOTE]
> **Yaegi** brings together classical Vedic astrology principles with modern Python development, making **Kundali, Panchang, Dasha, and Yogas accessible via code or CLI**.  

> [!WARNING]  
> This project is a **calculation engine**, not a substitute for professional astrological guidance.  

---

## ✨ Highlights

- 🪐 **Astronomical Calculations** – Planetary positions, ascendant, house systems  
- 🔮 **Kundali Generation** – D1 Lagna, divisional charts (Navamsa, Dashamsa, D60)  
- 📅 **Panchang** – Tithi, Nakshatra, Yoga, Karana  
- 📊 **Dasha Systems** – Vimshottari with Mahadasha & Antardasha  
- 🧩 **Yoga Detection** – Raj Yogas, Dhan Yogas, Panch Mahapurush Yogas  
- ❤️ **Compatibility** – Full 36-point Guna Milan with recommendations  
- ⚡ **CLI & API** – Use in scripts or command line  
- 📝 **Output Formats** – JSON, dict, formatted text  

---

## 🚀 Quick Start

```bash
pip install yaegi
```

### Kundali Example
```python
from yaegi import KundaliGenerator
from datetime import datetime

generator = KundaliGenerator()
chart = generator.generate_chart(
    birth_date=datetime(1990, 5, 15, 14, 30),
    latitude=28.6139, longitude=77.2090, timezone="Asia/Kolkata"
)

for planet in chart.planets:
    print(f"{planet.name}: {planet.dms} in House {planet.house}")
```

### Panchang Example
```python
from yaegi import PanchangGenerator
panchang = PanchangGenerator().generate_panchang(datetime(2024, 1, 15), 28.6139, 77.2090)

print(f"Tithi: {panchang['tithi']['name']}")
```

---

## 🧮 CLI Usage

```bash
yaegi kundali --date 1990-05-15 --time 14:30 --latitude 28.61 --longitude 77.21
yaegi panchang --date 2024-01-15 --latitude 28.61 --longitude 77.21
yaegi dasha --date 1990-05-15 --time 14:30 --latitude 28.61 --longitude 77.21
```

---

## 📌 Advanced Features

- Custom Ayanamsa (`LAHIRI`, etc.)  
- Divisional charts (D9 Navamsa, D10 Dashamsa, …)  
- Planetary strengths & aspect calculations  
- Configurable outputs (localization, caching, formats)  

---

## 🛠️ Development

```bash
git clone https://github.com/moshdevs/yaegi
cd yaegi
pip install -e .
```

> [!TIP]  
> Start with the CLI for quick results, then move to the Python API for advanced workflows.  

---

## ✅ Roadmap (Current Status)

- [x] Kundali generation (D1, D9, D10, D60)  
- [x] Panchang with Tithi, Nakshatra, Yoga  
- [x] Vimshottari Dasha calculation  
- [x] Compatibility analysis (Guna Milan)  
- [ ] Other Dasha systems (future)  
- [ ] Enhanced Yoga library  

---

## 🤝 Contributing

We welcome contributions of all kinds – calculations, translations, docs, tests.  
👉 See [CONTRIBUTING.md](CONTRIBUTING.md)  

---

## 📜 License

MIT License – see [LICENSE](LICENSE).  

---

## 🙏 Acknowledgments

- Classical Jyotish principles  
- Swiss Ephemeris for astronomical accuracy  
- Python astronomy & astrology community  

---

⭐ [Star us on GitHub](https://github.com/moshdevs/yaegi) if you like the project!  
