"""
Routine Service - Logic for generating daily routines based on goals
"""

class RoutineService:
    def generate_routine(self, user_goal: str) -> dict:
        """Generate a daily routine with morning, afternoon, and evening activities."""
        goal_lower = user_goal.strip().lower()

        # Default routine
        morning = ["Wake up at 7:00 AM", "Drink a glass of water", "15 mins light stretching"]
        afternoon = ["Eat a balanced lunch", "Take a 10 min walk", "Focus on important tasks"]
        evening = ["Eat a light dinner", "Read a book", "Sleep by 10:30 PM"]

        if "weight loss" in goal_lower or "lose weight" in goal_lower:
            morning.append("30 mins cardio exercise")
            afternoon.append("Drink green tea instead of sugary drinks")
            evening.append("Avoid heavy carbs after 7 PM")
        
        elif "muscle" in goal_lower or "gain weight" in goal_lower:
            morning.append("Eat a high-protein breakfast")
            afternoon.append("45 mins strength training session")
            evening.append("Consume a casein protein shake before bed")

        elif "stress" in goal_lower or "relax" in goal_lower:
            morning = ["Wake up naturally", "10 mins mindfulness meditation", "Drink herbal tea"]
            afternoon.append("Take regular short breaks from screen")
            evening.append("Warm bath and chamomile tea before bed")

        return {
            "routine": {
                "morning": morning,
                "afternoon": afternoon,
                "evening": evening
            }
        }
