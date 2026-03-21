"""
Diet Service - Business logic for meal planning and food tracking
"""

from datetime import date, timedelta
import json
import os


class DietService:
    def __init__(self):
        # Load sample food database
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data")
        food_db_path = os.path.join(data_dir, "foods.json")
        if os.path.exists(food_db_path):
            with open(food_db_path) as f:
                self.food_db = json.load(f)
        else:
            self.food_db = []

        # In-memory store (replace with DB in production)
        self._meal_logs = {}

    def generate_meal_plan(self, user_id: str, calories: int, goal: str) -> dict:
        """Generate a simple meal plan based on calorie goal."""
        plan = {
            "user_id": user_id,
            "goal": goal,
            "target_calories": calories,
            "meals": {
                "breakfast": {"name": "Oatmeal with berries", "calories": int(calories * 0.25)},
                "morning_snack": {"name": "Greek yogurt", "calories": int(calories * 0.10)},
                "lunch": {"name": "Grilled chicken salad", "calories": int(calories * 0.30)},
                "afternoon_snack": {"name": "Apple with almonds", "calories": int(calories * 0.10)},
                "dinner": {"name": "Baked salmon with vegetables", "calories": int(calories * 0.25)},
            },
        }
        return plan

    def log_meal(self, user_id: str, meal_name: str, calories: int, macros: dict) -> dict:
        """Log a meal to the user's food diary."""
        today = str(date.today())
        if user_id not in self._meal_logs:
            self._meal_logs[user_id] = {}
        if today not in self._meal_logs[user_id]:
            self._meal_logs[user_id][today] = []

        entry = {
            "meal_name": meal_name,
            "calories": calories,
            "macros": macros,
            "timestamp": today,
        }
        self._meal_logs[user_id][today].append(entry)
        return {"success": True, "entry": entry}

    def search_food(self, query: str) -> list:
        """Search food database by name."""
        query = query.lower()
        results = [f for f in self.food_db if query in f.get("name", "").lower()]
        return results[:20]  # Return top 20 matches

    def get_meal_history(self, user_id: str, days: int) -> list:
        """Get meal logs for the past N days."""
        logs = self._meal_logs.get(user_id, {})
        history = []
        for i in range(days):
            day = str(date.today() - timedelta(days=i))
            if day in logs:
                history.append({"date": day, "meals": logs[day]})
        return history

    def get_daily_calories(self, user_id: str) -> dict:
        """Get today's total calorie intake."""
        today = str(date.today())
        today_logs = self._meal_logs.get(user_id, {}).get(today, [])
        total = sum(m["calories"] for m in today_logs)
        return {"date": today, "total_calories": total, "meals": today_logs}

    def generate_diet(self, food_preference: str, deficiency: list) -> dict:
        """Generate a diet plan based on preference and deficiencies."""
        is_veg = food_preference.lower() == "veg"
        if isinstance(deficiency, str):
            deficiency = [deficiency]
        deficiency_lower = [d.lower() for d in deficiency]
        
        # Base plan
        plan = {
            "breakfast": ["Oatmeal with fruits"],
            "lunch": ["Lentil soup and quinoa"] if is_veg else ["Grilled chicken and brown rice"],
            "dinner": ["Mixed vegetable salad"] if is_veg else ["Baked salmon with broccoli"],
            "snacks": ["Nuts and seeds"]
        }
        
        # Modify based on deficiencies
        for d in deficiency_lower:
            if "iron" in d:
                plan["lunch"].append("Spinach salad")
                if not is_veg:
                    plan["dinner"].append("Lean beef cut")
            if "zinc" in d:
                plan["snacks"].append("Pumpkin seeds")
                if not is_veg:
                    plan["lunch"].append("Crab/Oysters based dish")
            if "b12" in d or "vitamin b12" in d:
                if is_veg:
                    plan["breakfast"].append("Fortified cereal or plant milk")
                else:
                    plan["breakfast"].append("Eggs")
            if "vitamin a" in d:
                plan["snacks"].append("Carrots and sweet potatoes")
                
        return {"diet_plan": plan}
