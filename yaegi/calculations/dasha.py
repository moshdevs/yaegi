def __init__(self):
    # Vimshottari Dasha periods in years
    self.dasha_periods = {
        "Ketu": 7,
        "Venus": 20,
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17,
    }

    # Nakshatra lords sequence
    self.nakshatra_lords = [
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn",
        "Mercury",
    ] * 3  # Repeat for 27 nakshatras

def calculate_vimshottari_dasha(self, chart: KundaliChart) -> VimshottariDasha:
    """Calculate complete Vimshottari Dasha system"""

    moon = chart.get_planet("Moon")
    if not moon:
        raise ValueError("Moon position required for Dasha calculation")

    # Calculate birth nakshatra
    birth_nakshatra = moon.nakshatra

    # Find starting dasha lord
    start_lord = self.nakshatra_lords[birth_nakshatra - 1]

    # Calculate how much of first dasha is completed at birth
    nakshatra_position = (moon.longitude * 27 / 360) % 1
    first_dasha_remaining = self.dasha_periods[start_lord] * (1 - nakshatra_position)

    # Generate all dasha periods
    periods = self._generate_mahadasha_periods(chart.birth_date, start_lord, first_dasha_remaining)

    return VimshottariDasha(
        birth_date=chart.birth_date,
        moon_nakshatra=birth_nakshatra,
        periods=periods,
    )

def _generate_mahadasha_periods(
    self, start_date: datetime, start_lord: str, first_remaining: float
) -> List[DashaPeriod]:
    """Generate all Mahadasha periods"""
    periods = []
    current_date = start_date

    # Find starting index in the sequence
    start_index = None
    for i, lord in enumerate(self.nakshatra_lords[:9]):
        if lord == start_lord:
            start_index = i
            break

    if start_index is None:
        raise ValueError(f"Invalid dasha lord: {start_lord}")

    # Generate periods for multiple cycles
    for cycle in range(3):  # Usually 2-3 cycles cover a lifetime
        for i in range(9):
            lord_index = (start_index + i) % 9
            lord = self.nakshatra_lords[lord_index]

            if cycle == 0 and i == 0:
                # First dasha - use remaining period
                duration = first_remaining
            else:
                duration = self.dasha_periods[lord]

            end_date = current_date + timedelta(days=duration * 365.25)

            period = DashaPeriod(
                planet=lord,
                start_date=current_date,
                end_date=end_date,
                duration_years=duration,
                level="mahadasha",
            )

            periods.append(period)
            current_date = end_date

            # Stop if we've generated enough periods (120+ years)
            if (current_date - start_date).days > 120 * 365:
                return periods

    return periods

def calculate_antardasha(self, mahadasha: DashaPeriod) -> List[DashaPeriod]:
    """Calculate Antardasha periods within a Mahadasha"""
    periods = []

    # Find mahadasha lord index
    lord_index = None
    for i, lord in enumerate(self.nakshatra_lords[:9]):
        if lord == mahadasha.planet:
            lord_index = i
            break

    if lord_index is None:
        return periods

    total_duration = mahadasha.duration_years
    current_date = mahadasha.start_date

    # Calculate antardasha periods
    for i in range(9):
        antarlord_index = (lord_index + i) % 9
        antarlord = self.nakshatra_lords[antarlord_index]

        # Antardasha duration = (Antarlord period / Total cycle) * Mahadasha period
        antardasha_duration = (self.dasha_periods[antarlord] / 120) * total_duration
        end_date = current_date + timedelta(days=antardasha_duration * 365.25)

        period = DashaPeriod(
            planet=antarlord,
            start_date=current_date,
            end_date=end_date,
            duration_years=antardasha_duration,
            level="antardasha",
            parent_dasha=mahadasha.planet,
        )

        periods.append(period)
        current_date = end_date

        if current_date >= mahadasha.end_date:
            break

    return periods

def get_current_dasha(
    self, dasha_system: VimshottariDasha, date: datetime = None
) -> Dict[str, Any]:
    """Get current running Dasha periods"""
    if date is None:
        date = datetime.now()

    current_mahadasha = None
    current_antardasha = None

    # Find current Mahadasha
    for period in dasha_system.periods:
        if period.start_date <= date <= period.end_date and period.level == "mahadasha":
            current_mahadasha = period
            break

    if current_mahadasha:
        # Calculate Antardasha for current Mahadasha
        antardasha_periods = self.calculate_antardasha(current_mahadasha)

        # Find current Antardasha
        for period in antardasha_periods:
            if period.start_date <= date <= period.end_date:
                current_antardasha = period
                break

    return {
        "mahadasha": current_mahadasha.to_dict() if current_mahadasha else None,
        "antardasha": current_antardasha.to_dict() if current_antardasha else None,
        "query_date": date.isoformat(),
    }

def get_dasha_predictions(self, planet: str) -> Dict[str, Any]:
    """Get general predictions for a dasha planet"""
    predictions = {
        "Sun": {
            "general": "Authority, government favor, success in leadership roles",
            "career": "Promotion, recognition, government jobs",
            "health": "Heart, eyes, bones - take care",
            "relationships": "Ego conflicts possible",
        },
        "Moon": {
            "general": "Emotional growth, travel, public recognition",
            "career": "Success in creative fields, public relations",
            "health": "Mental health, stomach issues",
            "relationships": "Strong emotional bonds",
        },
        "Mars": {
            "general": "Energy, courage, property gains",
            "career": "Technical fields, sports, military",
            "health": "Blood pressure, accidents - be careful",
            "relationships": "Passionate but conflict prone",
        },
        "Mercury": {
            "general": "Communication, learning, business success",
            "career": "Writing, teaching, commerce",
            "health": "Nervous system, skin issues",
            "relationships": "Good communication with partner",
        },
        "Jupiter": {
            "general": "Wisdom, spirituality, children's happiness",
            "career": "Teaching, law, consulting",
            "health": "Liver, weight gain",
            "relationships": "Marriage prospects, harmony",
        },
        "Venus": {
            "general": "Luxury, arts, beauty, relationships",
            "career": "Arts, entertainment, fashion",
            "health": "Reproductive system, diabetes",
            "relationships": "Love, marriage, harmony",
        },
        "Saturn": {
            "general": "Discipline, hard work, delays but steady progress",
            "career": "Slow but steady growth, mining, oil",
            "health": "Chronic diseases, bones, teeth",
            "relationships": "Delays in marriage, older partners",
        },
        "Rahu": {
            "general": "Foreign connections, technology, sudden changes",
            "career": "IT, foreign companies, unconventional fields",
            "health": "Mysterious ailments, mental stress",
            "relationships": "Unconventional relationships",
        },
        "Ketu": {
            "general": "Spirituality, detachment, research",
            "career": "Research, occult sciences, healing",
            "health": "Mysterious diseases, accidents",
            "relationships": "Detachment, spiritual connections",
        },
    }

    return predictions.get(planet, {"general": "Consult astrologer for specific predictions"})
