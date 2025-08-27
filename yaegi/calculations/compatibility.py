from typing import Dict, Any, List
from yaegi.models.chart import KundaliChart


class CompatibilityAnalyzer:
    """Analyze compatibility between two charts using Guna Milan"""

    def __init__(self):
        self.guna_weights = {
            "varna": 1,
            "vashya": 2,
            "tara": 3,
            "yoni": 4,
            "graha_maitri": 5,
            "gana": 6,
            "bhakoot": 7,
            "nadi": 8,
        }

    def analyze_compatibility(
        self, male_chart: KundaliChart, female_chart: KundaliChart
    ) -> Dict[str, Any]:
        """Perform complete Guna Milan analysis"""

        male_moon = male_chart.get_planet("Moon")
        female_moon = female_chart.get_planet("Moon")

        if not male_moon or not female_moon:
            return {"error": "Moon position required for both charts"}

        results = {}
        total_points = 0
        max_points = 36

        # Calculate each Guna
        results["varna"] = self.calculate_varna(male_moon.nakshatra, female_moon.nakshatra)
        results["vashya"] = self.calculate_vashya(male_moon.rashi, female_moon.rashi)
        results["tara"] = self.calculate_tara(male_moon.nakshatra, female_moon.nakshatra)
        results["yoni"] = self.calculate_yoni(male_moon.nakshatra, female_moon.nakshatra)
        results["graha_maitri"] = self.calculate_graha_maitri(male_moon.rashi, female_moon.rashi)
        results["gana"] = self.calculate_gana(male_moon.nakshatra, female_moon.nakshatra)
        results["bhakoot"] = self.calculate_bhakoot(male_moon.rashi, female_moon.rashi)
        results["nadi"] = self.calculate_nadi(male_moon.nakshatra, female_moon.nakshatra)

        # Calculate total points
        for guna, score in results.items():
            if isinstance(score, dict) and "points" in score:
                total_points += score["points"]

        # Determine compatibility level
        if total_points >= 32:
            compatibility = "Excellent"
        elif total_points >= 24:
            compatibility = "Good"
        elif total_points >= 18:
            compatibility = "Average"
        else:
            compatibility = "Poor"

        return {
            "total_points": total_points,
            "max_points": max_points,
            "percentage": (total_points / max_points) * 100,
            "compatibility": compatibility,
            "details": results,
            "recommendations": self.get_recommendations(total_points, results),
        }

    def calculate_varna(self, male_nakshatra: int, female_nakshatra: int) -> Dict[str, Any]:
        """Calculate Varna compatibility (1 point)"""
        varna_groups = {
            1: [1, 5, 9, 13, 17, 21, 25],
            2: [2, 6, 10, 14, 18, 22, 26],
            3: [3, 7, 11, 15, 19, 23, 27],
            4: [4, 8, 12, 16, 20, 24],
        }

        male_varna = None
        female_varna = None

        for varna, nakshatras in varna_groups.items():
            if male_nakshatra in nakshatras:
                male_varna = varna
            if female_nakshatra in nakshatras:
                female_varna = varna

        points = 1 if male_varna and female_varna and male_varna >= female_varna else 0

        return {
            "points": points,
            "max_points": 1,
            "male_varna": male_varna,
            "female_varna": female_varna,
            "compatible": points > 0,
        }

    def calculate_vashya(self, male_rashi: int, female_rashi: int) -> Dict[str, Any]:
        """Calculate Vashya compatibility (2 points)"""
        vashya_groups = {
            "quadruped": [1, 2, 5, 9, 10],
            "human": [3, 6, 7, 11],
            "jalachara": [4, 8, 12],
        }

        male_group = None
        female_group = None

        for group, rashis in vashya_groups.items():
            if male_rashi in rashis:
                male_group = group
            if female_rashi in rashis:
                female_group = group

        points = 2 if male_group == female_group else 0

        return {
            "points": points,
            "max_points": 2,
            "male_group": male_group,
            "female_group": female_group,
            "compatible": points > 0,
        }

    def calculate_tara(self, male_nakshatra: int, female_nakshatra: int) -> Dict[str, Any]:
        """Calculate Tara compatibility (3 points)"""
        count = abs(male_nakshatra - female_nakshatra) + 1
        tara_from_male = count % 9

        count_reverse = abs(female_nakshatra - male_nakshatra) + 1
        tara_from_female = count_reverse % 9

        favorable_taras = [1, 3, 5, 7]

        male_favorable = tara_from_male in favorable_taras
        female_favorable = tara_from_female in favorable_taras

        if male_favorable and female_favorable:
            points = 3
        elif male_favorable or female_favorable:
            points = 1.5
        else:
            points = 0

        return {
            "points": points,
            "max_points": 3,
            "tara_from_male": tara_from_male,
            "tara_from_female": tara_from_female,
            "compatible": points > 1,
        }

    def calculate_yoni(self, male_nakshatra: int, female_nakshatra: int) -> Dict[str, Any]:
        """Calculate Yoni compatibility (4 points)"""
        yoni_animals = {
            1: "Horse",
            2: "Elephant",
            3: "Goat",
            4: "Serpent",
            5: "Dog",
            6: "Cat",
            7: "Rat",
            8: "Cow",
            9: "Buffalo",
            10: "Lion",
            11: "Monkey",
            12: "Mongoose",
            13: "Monkey",
            14: "Lion",
            15: "Mongoose",
            16: "Rat",
            17: "Cat",
            18: "Dog",
            19: "Serpent",
            20: "Goat",
            21: "Elephant",
            22: "Horse",
            23: "Lion",
            24: "Monkey",
            25: "Mongoose",
            26: "Cat",
            27: "Cow",
        }

        male_yoni = yoni_animals.get(male_nakshatra, "Unknown")
        female_yoni = yoni_animals.get(female_nakshatra, "Unknown")

        compatible_pairs = [
            ("Horse", "Horse"),
            ("Elephant", "Elephant"),
            ("Lion", "Lion"),
            ("Horse", "Elephant"),
            ("Dog", "Cat"),
            ("Monkey", "Mongoose"),
        ]

        enemy_pairs = [
            ("Horse", "Buffalo"),
            ("Elephant", "Lion"),
            ("Cat", "Rat"),
            ("Dog", "Monkey"),
            ("Serpent", "Mongoose"),
        ]

        pair = (male_yoni, female_yoni)
        reverse_pair = (female_yoni, male_yoni)

        if pair in compatible_pairs or reverse_pair in compatible_pairs:
            points = 4
        elif pair in enemy_pairs or reverse_pair in enemy_pairs:
            points = 0
        else:
            points = 2

        return {
            "points": points,
            "max_points": 4,
            "male_yoni": male_yoni,
            "female_yoni": female_yoni,
            "compatible": points >= 2,
        }

    def calculate_graha_maitri(self, male_rashi: int, female_rashi: int) -> Dict[str, Any]:
        """Calculate Graha Maitri compatibility (5 points)"""
        rashi_lords = {
            1: "Mars",
            2: "Venus",
            3: "Mercury",
            4: "Moon",
            5: "Sun",
            6: "Mercury",
            7: "Venus",
            8: "Mars",
            9: "Jupiter",
            10: "Saturn",
            11: "Saturn",
            12: "Jupiter",
        }

        male_lord = rashi_lords.get(male_rashi, "Unknown")
        female_lord = rashi_lords.get(female_rashi, "Unknown")

        friends = {
            "Sun": ["Moon", "Mars", "Jupiter"],
            "Moon": ["Sun", "Mercury"],
            "Mars": ["Sun", "Moon", "Jupiter"],
            "Mercury": ["Sun", "Venus"],
            "Jupiter": ["Sun", "Moon", "Mars"],
            "Venus": ["Mercury", "Saturn"],
            "Saturn": ["Venus", "Mercury"],
        }

        if female_lord in friends.get(male_lord, []):
            points = 5
        elif male_lord == female_lord:
            points = 4
        else:
            points = 1

        return {
            "points": points,
            "max_points": 5,
            "male_lord": male_lord,
            "female_lord": female_lord,
            "compatible": points >= 3,
        }

    def calculate_gana(self, male_nakshatra: int, female_nakshatra: int) -> Dict[str, Any]:
        """Calculate Gana compatibility (6 points)"""
        gana_groups = {
            "deva": [1, 5, 7, 8, 13, 15, 17, 22, 27],
            "manushya": [2, 4, 6, 11, 12, 14, 16, 20, 21, 25],
            "rakshasa": [3, 9, 10, 18, 19, 23, 24, 26],
        }

        male_gana = None
        female_gana = None

        for gana, nakshatras in gana_groups.items():
            if male_nakshatra in nakshatras:
                male_gana = gana
            if female_nakshatra in nakshatras:
                female_gana = gana

        if male_gana == female_gana:
            points = 6
        elif (male_gana == "deva" and female_gana == "manushya") or (
            male_gana == "manushya" and female_gana == "deva"
        ):
            points = 5
        elif male_gana == "manushya" and female_gana == "rakshasa":
            points = 1
        else:
            points = 0

        return {
            "points": points,
            "max_points": 6,
            "male_gana": male_gana,
            "female_gana": female_gana,
            "compatible": points >= 3,
        }

    def calculate_bhakoot(self, male_rashi: int, female_rashi: int) -> Dict[str, Any]:
        """Calculate Bhakoot compatibility (7 points)"""
        diff = abs(male_rashi - female_rashi)

        if diff in [5, 6] or diff in [1, 11]:
            points = 0
        else:
            points = 7

        return {
            "points": points,
            "max_points": 7,
            "male_rashi": male_rashi,
            "female_rashi": female_rashi,
            "compatible": points > 0,
        }

    def calculate_nadi(self, male_nakshatra: int, female_nakshatra: int) -> Dict[str, Any]:
        """Calculate Nadi compatibility (8 points)"""
        nadi_groups = {
            "aadi": [1, 2, 7, 8, 9, 13, 14, 15, 21, 22, 23],
            "madhya": [4, 5, 6, 10, 11, 12, 16, 17, 18, 19, 25, 26, 27],
            "antya": [3, 20, 24],
        }

        male_nadi = None
        female_nadi = None

        for nadi, nakshatras in nadi_groups.items():
            if male_nakshatra in nakshatras:
                male_nadi = nadi
            if female_nakshatra in nakshatras:
                female_nadi = nadi

        points = 8 if male_nadi != female_nadi else 0

        return {
            "points": points,
            "max_points": 8,
            "male_nadi": male_nadi,
            "female_nadi": female_nadi,
            "compatible": points > 0,
        }

    def get_recommendations(self, total_points: float, results: Dict[str, Any]) -> List[str]:
        """Get compatibility recommendations"""
        recommendations = []

        if total_points >= 28:
            recommendations.append("Excellent compatibility - Marriage highly recommended")
        elif total_points >= 20:
            recommendations.append(
                "Good compatibility - Marriage recommended with proper rituals"
            )
        elif total_points >= 15:
            recommendations.append("Average compatibility - Consider additional factors")

        if results.get("nadi", {}).get("points", 0) == 0:
            recommendations.append("Same Nadi - Perform Nadi dosha remedies")

        if results.get("bhakoot", {}).get("points", 0) == 0:
            recommendations.append("Bhakoot dosha present - Consult astrologer for remedies")

        if results.get("gana", {}).get("points", 0) <= 2:
            recommendations.append("Gana mismatch - May cause temperament differences")

        return recommendations
      
