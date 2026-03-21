"""
Routine Service - Personalized daily routine + exercise plan generation.
"""
import json
from datetime import datetime
from database import get_connection


class RoutineService:

    EXERCISE_PLANS = {
        "weight loss": {
            "beginner": {
                "Monday": "30 min brisk walk + 10 min stretching",
                "Tuesday": "Rest or light yoga 20 min",
                "Wednesday": "30 min walk + bodyweight squats 3x10",
                "Thursday": "Rest",
                "Friday": "30 min walk + push-ups 3x10",
                "Saturday": "Light cycling 30 min",
                "Sunday": "Rest",
            },
            "moderate": {
                "Monday": "45 min cardio + core workout 20 min",
                "Tuesday": "Upper body strength 45 min",
                "Wednesday": "45 min cardio",
                "Thursday": "Lower body strength 45 min",
                "Friday": "HIIT 30 min",
                "Saturday": "Active recovery yoga 45 min",
                "Sunday": "Rest",
            },
            "active": {
                "Monday": "60 min run + core 20 min",
                "Tuesday": "Full body strength 60 min",
                "Wednesday": "Interval training 45 min",
                "Thursday": "Swimming or cycling 60 min",
                "Friday": "HIIT 45 min + abs",
                "Saturday": "Long run or hike 60 min",
                "Sunday": "Active recovery yoga",
            },
        },
        "muscle gain": {
            "beginner": {
                "Monday": "Upper body push (chest, shoulders, triceps)",
                "Tuesday": "Rest or light cardio 20 min",
                "Wednesday": "Upper body pull (back, biceps)",
                "Thursday": "Rest",
                "Friday": "Lower body (squats, lunges, calves)",
                "Saturday": "Full body light workout",
                "Sunday": "Rest",
            },
            "moderate": {
                "Monday": "Chest + Triceps 45 min",
                "Tuesday": "Back + Biceps 45 min",
                "Wednesday": "Shoulders + Abs 40 min",
                "Thursday": "Legs + Glutes 50 min",
                "Friday": "Arms + Core 40 min",
                "Saturday": "Full body compound movements",
                "Sunday": "Rest",
            },
            "active": {
                "Monday": "Heavy chest + triceps 60 min",
                "Tuesday": "Heavy back + biceps 60 min",
                "Wednesday": "Shoulders + traps 50 min",
                "Thursday": "Heavy legs 60 min",
                "Friday": "Arms + abs 50 min",
                "Saturday": "Weak point training 45 min",
                "Sunday": "Rest + stretching",
            },
        },
        "general health": {
            "beginner": {
                "Monday": "30 min walk + yoga 20 min",
                "Tuesday": "Light strength training 30 min",
                "Wednesday": "Swimming or cycling 30 min",
                "Thursday": "Yoga or stretching 30 min",
                "Friday": "30 min cardio",
                "Saturday": "Outdoor activity",
                "Sunday": "Rest",
            },
            "moderate": {
                "Monday": "Jogging 30 min + stretching",
                "Tuesday": "Strength training 40 min",
                "Wednesday": "Swimming or cycling 40 min",
                "Thursday": "Yoga 40 min",
                "Friday": "Circuit training 30 min",
                "Saturday": "Sports or hiking",
                "Sunday": "Rest",
            },
            "active": {
                "Monday": "Running 45 min",
                "Tuesday": "Full body strength 50 min",
                "Wednesday": "HIIT or swimming 45 min",
                "Thursday": "Yoga + mobility 40 min",
                "Friday": "Sports or martial arts 60 min",
                "Saturday": "Long hike or cycling",
                "Sunday": "Active recovery",
            },
        },
    }

    def _add_time(self, time_str, mins):
        try:
            h, m = map(int, time_str.split(":"))
            m += mins
            h += m // 60
            m %= 60
            h %= 24
            return f"{h:02d}:{m:02d}"
        except:
            return time_str

    def generate_routine(self, data):
        user_id = data.get("user_id")
        wake = data.get("wake_time", "07:00")
        sleep = data.get("sleep_time", "23:00")
        goal = str(data.get("goal") or data.get("health_goals") or "general health").lower()
        deficiencies = data.get("deficiencies", [])
        medications = data.get("medications", [])
        if isinstance(medications, str):
            medications = [m.strip() for m in medications.split(",") if m.strip()]
        activity = str(data.get("activity_level") or "moderate").lower()
        if activity not in ("beginner", "moderate", "active"):
            if activity in ("sedentary", "light"):
                activity = "beginner"
            elif activity in ("very active",):
                activity = "active"
            else:
                activity = "moderate"

        # Morning tasks
        morning = [
            {"time": wake, "activity": "Drink 2 glasses of warm water", "icon": "💧", "done": False},
            {"time": self._add_time(wake, 15), "activity": "Light stretching 10 min", "icon": "🧘", "done": False},
            {"time": self._add_time(wake, 30), "activity": "Morning walk or exercise", "icon": "🏃", "done": False},
            {"time": self._add_time(wake, 60), "activity": "Breakfast", "icon": "🍳", "done": False},
        ]
        # Check for vitamin D deficiency
        def_names = []
        if isinstance(deficiencies, list):
            for d in deficiencies:
                if isinstance(d, dict):
                    def_names.append(d.get("name", ""))
                elif isinstance(d, str):
                    def_names.append(d)
        if any("Vitamin D" in d for d in def_names):
            morning.append({"time": self._add_time(wake, 90), "activity": "Morning sunlight 15 min", "icon": "☀️", "done": False})

        afternoon = [
            {"time": "13:00", "activity": "Lunch", "icon": "🥗", "done": False},
            {"time": "13:30", "activity": "Short walk 10 min", "icon": "🚶", "done": False},
            {"time": "15:00", "activity": "Healthy snack + water", "icon": "🍎", "done": False},
        ]

        ex_type = "cardio" if "loss" in goal else "strength" if "muscle" in goal or "gain" in goal else "mixed"
        evening = [
            {"time": "18:00", "activity": f"Exercise session ({ex_type})", "icon": "💪", "done": False},
            {"time": "19:00", "activity": "Cool down stretching", "icon": "🧘", "done": False},
            {"time": "19:30", "activity": "Dinner", "icon": "🥘", "done": False},
        ]

        night = [
            {"time": "21:00", "activity": "Light snack if needed", "icon": "🍇", "done": False},
            {"time": self._add_time(sleep, -30), "activity": "No screens, wind down", "icon": "📵", "done": False},
            {"time": self._add_time(sleep, -15), "activity": "Relaxation or meditation", "icon": "🧘", "done": False},
            {"time": sleep, "activity": "Sleep (7-8 hours)", "icon": "🌙", "done": False},
        ]

        # Medications
        med_list = []
        for i, med in enumerate(medications):
            if med:
                t = self._add_time(wake, 60 + i * 180)
                med_list.append({"time": t, "name": str(med), "taken": False})

        # Exercise plan
        goal_key = "weight loss" if "loss" in goal else "muscle gain" if "muscle" in goal or "gain" in goal else "general health"
        exercise_plan = self.EXERCISE_PLANS.get(goal_key, self.EXERCISE_PLANS["general health"]).get(activity, {})

        # Save
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute('''INSERT INTO routines (user_id,wake_time,sleep_time,morning_tasks,afternoon_tasks,
                         evening_tasks,night_tasks,medications,exercise_type,exercise_plan,created_at)
                         VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                      (user_id, wake, sleep, json.dumps(morning), json.dumps(afternoon),
                       json.dumps(evening), json.dumps(night), json.dumps(med_list),
                       ex_type, json.dumps(exercise_plan), datetime.utcnow().isoformat()))
            conn.commit()
            conn.close()
        except Exception as e:
            return {"error": str(e)}

        return {
            "morning": morning, "afternoon": afternoon, "evening": evening, "night": night,
            "medications": med_list, "exercise_plan": exercise_plan
        }

    def get_latest_routine(self, user_id):
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM routines WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,))
            row = c.fetchone()
            conn.close()
            if row:
                return {
                    "morning": json.loads(row["morning_tasks"]),
                    "afternoon": json.loads(row["afternoon_tasks"]),
                    "evening": json.loads(row["evening_tasks"]),
                    "night": json.loads(row["night_tasks"]),
                    "medications": json.loads(row["medications"]),
                    "exercise_plan": json.loads(row["exercise_plan"] or "{}"),
                    "wake_time": row["wake_time"],
                    "sleep_time": row["sleep_time"],
                }
            return None
        except:
            return None
