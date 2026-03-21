"""
Diet Service - 7-day meal plan generation with goal-based templates.
"""
import json, random
from datetime import datetime
from database import get_connection


class DietService:

    MEAL_TEMPLATES = {
        "weight loss": {
            "veg": {
                "breakfast": [
                    {"name": "Oats with Almonds & Berries", "calories": 350, "protein": 12, "carbs": 45, "fat": 12},
                    {"name": "Greek Yogurt Parfait", "calories": 300, "protein": 18, "carbs": 35, "fat": 8},
                    {"name": "Moong Dal Chilla with Chutney", "calories": 280, "protein": 14, "carbs": 30, "fat": 10},
                    {"name": "Smoothie Bowl with Seeds", "calories": 320, "protein": 10, "carbs": 40, "fat": 12},
                ],
                "lunch": [
                    {"name": "Dal + Brown Rice + Salad", "calories": 450, "protein": 18, "carbs": 55, "fat": 12},
                    {"name": "Quinoa Vegetable Bowl", "calories": 420, "protein": 15, "carbs": 50, "fat": 14},
                    {"name": "Chickpea Salad Wrap", "calories": 400, "protein": 16, "carbs": 45, "fat": 15},
                    {"name": "Rajma Curry + Roti + Raita", "calories": 480, "protein": 20, "carbs": 58, "fat": 12},
                ],
                "dinner": [
                    {"name": "Vegetable Soup + Multigrain Bread", "calories": 300, "protein": 10, "carbs": 35, "fat": 10},
                    {"name": "Palak Paneer + 1 Roti", "calories": 350, "protein": 18, "carbs": 25, "fat": 16},
                    {"name": "Stir-fried Tofu with Vegetables", "calories": 320, "protein": 20, "carbs": 20, "fat": 14},
                    {"name": "Mixed Vegetable Khichdi", "calories": 340, "protein": 12, "carbs": 45, "fat": 8},
                ],
                "snacks": [
                    {"name": "Apple + Handful of Almonds", "calories": 180, "protein": 5, "carbs": 20, "fat": 10},
                    {"name": "Roasted Makhana", "calories": 120, "protein": 4, "carbs": 18, "fat": 3},
                    {"name": "Fruit Salad", "calories": 150, "protein": 2, "carbs": 30, "fat": 1},
                    {"name": "Green Tea + Mixed Seeds", "calories": 130, "protein": 4, "carbs": 8, "fat": 8},
                ],
            },
            "non-veg": {
                "breakfast": [
                    {"name": "Egg White Omelette + Toast", "calories": 320, "protein": 25, "carbs": 30, "fat": 8},
                    {"name": "Boiled Eggs + Avocado Toast", "calories": 380, "protein": 20, "carbs": 28, "fat": 18},
                    {"name": "Chicken Sausage + Oats", "calories": 400, "protein": 28, "carbs": 35, "fat": 12},
                    {"name": "Scrambled Eggs + Spinach", "calories": 300, "protein": 22, "carbs": 10, "fat": 16},
                ],
                "lunch": [
                    {"name": "Grilled Chicken + Quinoa + Salad", "calories": 500, "protein": 40, "carbs": 40, "fat": 14},
                    {"name": "Fish Curry + Brown Rice", "calories": 480, "protein": 35, "carbs": 45, "fat": 12},
                    {"name": "Chicken Salad Bowl", "calories": 420, "protein": 35, "carbs": 30, "fat": 16},
                    {"name": "Tuna Wrap + Veggies", "calories": 450, "protein": 32, "carbs": 38, "fat": 14},
                ],
                "dinner": [
                    {"name": "Baked Salmon + Steamed Veggies", "calories": 400, "protein": 35, "carbs": 15, "fat": 18},
                    {"name": "Chicken Breast + Sweet Potato", "calories": 420, "protein": 38, "carbs": 30, "fat": 10},
                    {"name": "Grilled Fish + Salad", "calories": 350, "protein": 32, "carbs": 12, "fat": 16},
                    {"name": "Egg Curry + 1 Roti", "calories": 380, "protein": 22, "carbs": 30, "fat": 16},
                ],
                "snacks": [
                    {"name": "Hard-boiled Egg + Fruit", "calories": 160, "protein": 8, "carbs": 15, "fat": 7},
                    {"name": "Protein Shake", "calories": 200, "protein": 25, "carbs": 10, "fat": 5},
                    {"name": "Almonds + Dark Chocolate", "calories": 180, "protein": 6, "carbs": 12, "fat": 12},
                    {"name": "Greek Yogurt", "calories": 150, "protein": 12, "carbs": 8, "fat": 6},
                ],
            },
        },
        "muscle gain": {
            "veg": {
                "breakfast": [
                    {"name": "Protein Smoothie + Oats + Banana", "calories": 550, "protein": 30, "carbs": 65, "fat": 15},
                    {"name": "Paneer Paratha + Curd", "calories": 600, "protein": 25, "carbs": 55, "fat": 22},
                    {"name": "Besan Chilla + Protein Shake", "calories": 500, "protein": 28, "carbs": 45, "fat": 18},
                    {"name": "Peanut Butter Toast + Milk + Banana", "calories": 520, "protein": 22, "carbs": 55, "fat": 20},
                ],
                "lunch": [
                    {"name": "Paneer + Brown Rice + Dal", "calories": 650, "protein": 35, "carbs": 70, "fat": 20},
                    {"name": "Soya Chunks Curry + Rice + Salad", "calories": 600, "protein": 38, "carbs": 60, "fat": 15},
                    {"name": "Chole + Rice + Raita", "calories": 620, "protein": 25, "carbs": 75, "fat": 18},
                    {"name": "Tofu Stir-fry + Quinoa", "calories": 550, "protein": 30, "carbs": 55, "fat": 18},
                ],
                "dinner": [
                    {"name": "Dal Makhani + 2 Roti + Paneer", "calories": 580, "protein": 28, "carbs": 55, "fat": 22},
                    {"name": "Tofu Tikka + Rice + Salad", "calories": 520, "protein": 30, "carbs": 50, "fat": 16},
                    {"name": "Mixed Bean Curry + Roti", "calories": 500, "protein": 25, "carbs": 55, "fat": 14},
                    {"name": "Paneer Bhurji + Multigrain Roti", "calories": 550, "protein": 30, "carbs": 40, "fat": 22},
                ],
                "snacks": [
                    {"name": "Protein Bar + Milk", "calories": 350, "protein": 25, "carbs": 30, "fat": 12},
                    {"name": "Peanut Butter Banana Shake", "calories": 400, "protein": 18, "carbs": 40, "fat": 18},
                    {"name": "Trail Mix + Dates", "calories": 300, "protein": 10, "carbs": 35, "fat": 15},
                    {"name": "Paneer Tikka + Chutney", "calories": 280, "protein": 20, "carbs": 10, "fat": 16},
                ],
            },
            "non-veg": {
                "breakfast": [
                    {"name": "4 Eggs + Oatmeal + Banana", "calories": 600, "protein": 35, "carbs": 55, "fat": 20},
                    {"name": "Chicken Omelette + Toast + Juice", "calories": 580, "protein": 38, "carbs": 45, "fat": 18},
                    {"name": "Protein Pancakes + Eggs", "calories": 550, "protein": 35, "carbs": 50, "fat": 16},
                    {"name": "Egg Bhurji + 2 Parathas", "calories": 620, "protein": 28, "carbs": 58, "fat": 22},
                ],
                "lunch": [
                    {"name": "Chicken Breast + Brown Rice + Dal", "calories": 700, "protein": 50, "carbs": 65, "fat": 15},
                    {"name": "Fish Curry + Rice + Salad", "calories": 650, "protein": 42, "carbs": 60, "fat": 18},
                    {"name": "Mutton Curry + Roti + Raita", "calories": 720, "protein": 45, "carbs": 55, "fat": 25},
                    {"name": "Grilled Chicken Bowl + Quinoa", "calories": 680, "protein": 48, "carbs": 55, "fat": 16},
                ],
                "dinner": [
                    {"name": "Grilled Fish + Sweet Potato + Veggies", "calories": 550, "protein": 40, "carbs": 45, "fat": 14},
                    {"name": "Chicken Tikka + Rice", "calories": 580, "protein": 42, "carbs": 50, "fat": 16},
                    {"name": "Egg Curry + 2 Roti", "calories": 500, "protein": 28, "carbs": 45, "fat": 18},
                    {"name": "Salmon + Mashed Potato + Salad", "calories": 560, "protein": 38, "carbs": 40, "fat": 20},
                ],
                "snacks": [
                    {"name": "Protein Shake + Banana", "calories": 350, "protein": 30, "carbs": 35, "fat": 6},
                    {"name": "Boiled Eggs + Nuts", "calories": 300, "protein": 20, "carbs": 8, "fat": 20},
                    {"name": "Chicken Sandwich", "calories": 380, "protein": 28, "carbs": 35, "fat": 10},
                    {"name": "Milk + Dry Fruits", "calories": 320, "protein": 15, "carbs": 25, "fat": 15},
                ],
            },
        },
    }

    def generate_diet(self, data):
        user_id = data.get("user_id")
        pref = str(data.get("food_preference", "veg")).lower().replace("-","").replace(" ","")
        if "non" in pref:
            pref_key = "non-veg"
        elif "vegan" in pref:
            pref_key = "non-veg"  # fallback
        else:
            pref_key = "veg"
        goal = str(data.get("goal") or data.get("health_goals") or "general health").lower()
        calories = int(data.get("calories_target") or 2000)
        allergies = data.get("allergies", [])
        if isinstance(allergies, str):
            try: allergies = json.loads(allergies)
            except: allergies = [a.strip() for a in allergies.split(",") if a.strip()]

        # Pick template
        goal_key = "weight loss" if "loss" in goal else "muscle gain" if "muscle" in goal or "gain" in goal else "weight loss"
        templates = self.MEAL_TEMPLATES.get(goal_key, self.MEAL_TEMPLATES["weight loss"])
        pref_meals = templates.get(pref_key, templates.get("veg"))

        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        plan = {}
        shopping = set()
        for i, day in enumerate(days):
            day_plan = {}
            for meal_type in ["breakfast","lunch","dinner","snacks"]:
                options = pref_meals.get(meal_type, [])
                if options:
                    meal = options[i % len(options)].copy()
                    shopping.add(meal["name"])
                    day_plan[meal_type] = meal
                else:
                    day_plan[meal_type] = {"name":"Balanced meal","calories":400,"protein":20,"carbs":40,"fat":15}
            plan[day] = day_plan

        macros = {"protein": 100, "carbs": 150, "fat": 55}
        if "muscle" in goal_key:
            macros = {"protein": 150, "carbs": 200, "fat": 60}

        # Save
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute('''INSERT INTO diet_plans (user_id,food_preference,allergies,goal,calories_target,
                         meal_plan,macros,shopping_list,created_at) VALUES (?,?,?,?,?,?,?,?,?)''',
                      (user_id, pref_key, json.dumps(allergies), goal, calories,
                       json.dumps(plan), json.dumps(macros), json.dumps(list(shopping)),
                       datetime.utcnow().isoformat()))
            conn.commit()
            conn.close()
        except Exception as e:
            return {"error": str(e)}

        return {"meal_plan": plan, "total_calories": calories, "macros": macros, "shopping_list": list(shopping)}

    def get_latest_diet(self, user_id):
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM diet_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,))
            row = c.fetchone()
            conn.close()
            if row:
                return {
                    "meal_plan": json.loads(row["meal_plan"]),
                    "total_calories": row["calories_target"],
                    "macros": json.loads(row["macros"]),
                    "shopping_list": json.loads(row["shopping_list"] or "[]"),
                    "food_preference": row["food_preference"],
                    "goal": row["goal"],
                }
            return None
        except:
            return None
