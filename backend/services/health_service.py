"""
Health Service - Business logic for BMI, TDEE, and vitals
"""

from datetime import date, timedelta


class HealthService:
    def __init__(self):
        self._vitals_logs = {}  # Replace with DB in production

    def calculate_bmi(self, weight_kg: float, height_cm: float) -> dict:
        """Calculate BMI and return category."""
        height_m = height_cm / 100
        bmi = round(weight_kg / (height_m ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
            advice = "Consider a calorie-surplus diet with nutrient-dense foods."
        elif bmi < 25:
            category = "Normal weight"
            advice = "Great! Maintain your current balanced lifestyle."
        elif bmi < 30:
            category = "Overweight"
            advice = "A slight calorie deficit and regular exercise is recommended."
        else:
            category = "Obese"
            advice = "Please consult a healthcare professional for a personalized plan."

        return {"bmi": bmi, "category": category, "advice": advice}

    def calculate_tdee(
        self,
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: str,
        activity_level: str,
    ) -> dict:
        """Calculate TDEE using Mifflin-St Jeor equation."""
        # Basal Metabolic Rate
        if gender.lower() == "male":
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

        activity_factors = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9,
        }
        factor = activity_factors.get(activity_level, 1.55)
        tdee = round(bmr * factor)

        return {
            "bmr": round(bmr),
            "tdee": tdee,
            "activity_level": activity_level,
            "calorie_targets": {
                "lose_weight": tdee - 500,
                "maintain": tdee,
                "gain_weight": tdee + 500,
            },
        }

    def log_vitals(
        self,
        user_id: str,
        weight: float = None,
        blood_pressure: str = None,
        blood_sugar: float = None,
        heart_rate: int = None,
    ) -> dict:
        """Log vitals for a user."""
        today = str(date.today())
        if user_id not in self._vitals_logs:
            self._vitals_logs[user_id] = []

        entry = {
            "date": today,
            "weight": weight,
            "blood_pressure": blood_pressure,
            "blood_sugar": blood_sugar,
            "heart_rate": heart_rate,
        }
        self._vitals_logs[user_id].append(entry)
        return {"success": True, "entry": entry}

    def get_vitals_history(self, user_id: str, days: int) -> list:
        """Get vitals history for a user."""
        logs = self._vitals_logs.get(user_id, [])
        cutoff = date.today() - timedelta(days=days)
        return [v for v in logs if v["date"] >= str(cutoff)]

    def get_recommendations(self, user_id: str) -> list:
        """Provide basic health recommendations."""
        return [
            {"type": "hydration", "message": "Drink at least 8 glasses of water daily."},
            {"type": "sleep", "message": "Aim for 7-9 hours of quality sleep each night."},
            {"type": "exercise", "message": "Include 30 minutes of moderate exercise 5 days/week."},
            {"type": "nutrition", "message": "Ensure adequate protein: 0.8g per kg of body weight."},
        ]
