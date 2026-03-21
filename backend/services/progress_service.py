"""
Progress Service - Daily logging and weekly summaries.
"""
from datetime import datetime, timedelta
from database import get_connection


class ProgressService:

    def log_progress(self, data):
        user_id = data.get("user_id")
        date = data.get("date", str(datetime.now().date()))
        water = int(data.get("water_glasses") or 0)
        exercise = int(data.get("exercise_done") or 0)
        meals = int(data.get("meals_followed") or 0)
        weight = float(data.get("weight") or 0)
        mood = str(data.get("mood") or "neutral")
        energy = int(data.get("energy_level") or 5)
        notes = str(data.get("notes") or "")

        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT id FROM progress WHERE user_id=? AND date=?", (user_id, date))
            entry = c.fetchone()
            if entry:
                c.execute('''UPDATE progress SET water_glasses=?,exercise_done=?,meals_followed=?,
                             weight=?,mood=?,energy_level=?,notes=? WHERE id=?''',
                          (water, exercise, meals, weight, mood, energy, notes, entry["id"]))
            else:
                c.execute('''INSERT INTO progress (user_id,date,water_glasses,exercise_done,meals_followed,
                             weight,mood,energy_level,notes) VALUES (?,?,?,?,?,?,?,?,?)''',
                          (user_id, date, water, exercise, meals, weight, mood, energy, notes))
            conn.commit()
            conn.close()
            return {"success": True, "message": "Progress logged."}
        except Exception as e:
            return {"error": str(e)}

    def get_progress_history(self, user_id, limit=30):
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM progress WHERE user_id=? ORDER BY date DESC LIMIT ?", (user_id, limit))
            rows = c.fetchall()
            conn.close()
            return [dict(r) for r in rows]
        except:
            return []

    def get_weekly_summary(self, user_id):
        try:
            conn = get_connection()
            c = conn.cursor()
            week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            c.execute("SELECT * FROM progress WHERE user_id=? AND date>=? ORDER BY date DESC", (user_id, week_ago))
            rows = c.fetchall()
            conn.close()
            if not rows:
                return {"total_water": 0, "exercise_days": 0, "avg_weight": 0, "meals_compliance": 0, "avg_mood": "neutral", "avg_energy": 5, "days_logged": 0, "history": []}
            total_water = sum(r["water_glasses"] for r in rows)
            exercise_days = sum(1 for r in rows if r["exercise_done"])
            weights = [r["weight"] for r in rows if r["weight"] and r["weight"] > 0]
            avg_weight = round(sum(weights) / len(weights), 1) if weights else 0
            meals_total = sum(r["meals_followed"] for r in rows)
            energies = [r["energy_level"] for r in rows if r["energy_level"]]
            avg_energy = round(sum(energies) / len(energies), 1) if energies else 5
            return {
                "total_water": total_water,
                "exercise_days": exercise_days,
                "avg_weight": avg_weight,
                "meals_compliance": meals_total,
                "avg_energy": avg_energy,
                "days_logged": len(rows),
                "history": [dict(r) for r in rows],
            }
        except Exception as e:
            return {"error": str(e)}
