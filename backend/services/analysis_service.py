"""
Analysis Service - AI-driven health and nutrition analysis
"""

from datetime import date


class AnalysisService:
    # Reference Daily Intake values
    RDI = {
        "calories":   2000,
        "protein_g":  50,
        "carbs_g":    300,
        "fat_g":      65,
        "fiber_g":    25,
        "vitamin_c_mg": 90,
        "vitamin_d_iu": 600,
        "calcium_mg": 1000,
        "iron_mg":    18,
    }

    def generate_weekly_report(self, user_id: str) -> dict:
        """Generate a weekly diet & health report."""
        # Placeholder — in production, query DB for real data
        return {
            "user_id": user_id,
            "week_ending": str(date.today()),
            "average_daily_calories": 1850,
            "goal_calories": 2000,
            "adherence_percent": 92,
            "top_nutrients_met": ["protein", "fiber", "vitamin_c"],
            "nutrients_to_improve": ["vitamin_d", "calcium"],
            "summary": "Good week! You stayed close to your calorie goal. Focus on getting more vitamin D.",
        }

    def analyze_nutrient_gaps(self, user_id: str) -> dict:
        """Identify nutritional deficiencies based on logged meals."""
        # Placeholder analysis
        return {
            "user_id": user_id,
            "deficiencies": [
                {"nutrient": "Vitamin D", "current_iu": 200, "recommended_iu": 600, "gap_percent": 67},
                {"nutrient": "Calcium", "current_mg": 600, "recommended_mg": 1000, "gap_percent": 40},
            ],
            "excesses": [
                {"nutrient": "Sodium", "current_mg": 3200, "recommended_mg": 2300, "excess_percent": 39},
            ],
        }

    def check_vitamins(self, user_id: str) -> list:
        """Check vitamin and mineral intake levels."""
        return [
            {"vitamin": "Vitamin A",  "status": "adequate",    "level": "900 mcg"},
            {"vitamin": "Vitamin B12","status": "adequate",    "level": "2.8 mcg"},
            {"vitamin": "Vitamin C",  "status": "adequate",    "level": "95 mg"},
            {"vitamin": "Vitamin D",  "status": "deficient",   "level": "200 IU"},
            {"vitamin": "Vitamin E",  "status": "adequate",    "level": "15 mg"},
            {"vitamin": "Iron",       "status": "low",         "level": "12 mg"},
            {"vitamin": "Calcium",    "status": "low",         "level": "700 mg"},
            {"vitamin": "Zinc",       "status": "adequate",    "level": "11 mg"},
        ]

    def get_progress(self, user_id: str) -> dict:
        """Get progress towards user health goals."""
        return {
            "user_id": user_id,
            "start_weight_kg": 85.0,
            "current_weight_kg": 82.5,
            "target_weight_kg": 75.0,
            "progress_percent": 33,
            "weeks_active": 3,
            "on_track": True,
            "estimated_goal_date": "2026-06-15",
        }

    def generate_ai_insights(self, user_id: str) -> list:
        """Generate AI-driven personalized health insights."""
        return [
            {
                "category": "Nutrition",
                "insight": "Your protein intake is on track. Consider adding fatty fish twice a week for omega-3 and vitamin D.",
                "priority": "high",
            },
            {
                "category": "Hydration",
                "insight": "Based on your activity level, aim for 3L of water daily.",
                "priority": "medium",
            },
            {
                "category": "Sleep & Recovery",
                "insight": "Quality sleep boosts metabolism. A consistent bedtime will help your weight-loss goal.",
                "priority": "medium",
            },
            {
                "category": "Exercise",
                "insight": "Adding 20 minutes of strength training 3x/week would accelerate fat loss.",
                "priority": "high",
            },
        ]

    def analyze_health(self, height: float, weight: float, age: int, symptoms: list, food_preference: str) -> dict:
        """Analyze health based on symptoms and vitals."""
        deficiencies = []
        foods = []
        advice = []
        
        symptoms_lower = [s.strip().lower() for s in symptoms]
        is_veg = food_preference.lower() == "veg"
        
        if "hair fall" in symptoms_lower:
            deficiencies.append("iron deficiency")
            foods.extend(["Spinach", "Lentils"] if is_veg else ["Red meat", "Spinach"])
        if "dandruff" in symptoms_lower:
            deficiencies.append("zinc deficiency")
            foods.extend(["Nuts", "Seeds"] if is_veg else ["Chicken", "Oysters"])
        if "fatigue" in symptoms_lower:
            deficiencies.append("vitamin B12 deficiency")
            foods.extend(["Fortified cereals", "Nutritional yeast"] if is_veg else ["Eggs", "Fish"])
            
        height_m = height / 100
        bmi = weight / (height_m ** 2) if height_m > 0 else 0
        
        if bmi < 18.5:
            condition = "Underweight"
            advice.append("Increase caloric intake with nutrient-dense foods.")
        elif bmi <= 25:
            condition = "Healthy Weight"
            advice.append("Maintain current balanced lifestyle and regular exercise.")
        else:
            condition = "Overweight"
            advice.append("Focus on portion control and increase daily physical activity.")
            
        return {
            "health_condition": condition,
            "possible_deficiencies": deficiencies,
            "recommended_foods": list(set(foods)),
            "lifestyle_advice": advice
        }
