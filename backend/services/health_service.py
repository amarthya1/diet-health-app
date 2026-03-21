"""
Health Service - Orchestrates analysis and DB persistence.
"""
import json
from datetime import datetime
from database import get_connection
from services.analysis_service import AnalysisService


class HealthService:

    def analyze_health(self, data):
        """Run analysis and save results to DB."""
        user_id = data.get("user_id")
        service = AnalysisService()
        result = service.analyze_health(data)

        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute('''INSERT INTO health_analysis (
                user_id, symptoms, bmi, bmi_category, deficiencies,
                health_condition, health_score, recommended_foods,
                foods_to_avoid, lifestyle_advice, supplement_suggestions,
                blood_pressure, blood_sugar, hemoglobin,
                urgency_level, see_doctor, see_doctor_reason,
                combined_diagnosis, created_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
                user_id,
                json.dumps(data.get("symptoms", [])),
                result["bmi"],
                result["bmi_category"],
                json.dumps(result["deficiencies"]),
                result["health_condition"],
                result["health_score"],
                json.dumps(result["recommended_foods"]),
                json.dumps(result["foods_to_avoid"]),
                json.dumps(result["lifestyle_advice"]),
                json.dumps(result["supplement_suggestions"]),
                data.get("blood_pressure", ""),
                data.get("blood_sugar", 0),
                data.get("hemoglobin", 0),
                result["urgency_level"],
                1 if result["see_doctor"] else 0,
                result["see_doctor_reason"],
                result.get("combined_diagnosis", ""),
                datetime.utcnow().isoformat(),
            ))
            conn.commit()
            result["analysis_id"] = c.lastrowid
            conn.close()
        except Exception as e:
            result["db_warning"] = f"Analysis complete but save failed: {e}"

        return result

    def get_user_analyses(self, user_id, limit=5):
        """Fetch analysis history."""
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM health_analysis WHERE user_id=? ORDER BY created_at DESC LIMIT ?", (user_id, limit))
            rows = c.fetchall()
            conn.close()
            results = []
            for r in rows:
                results.append({
                    "id": r["id"],
                    "bmi": r["bmi"],
                    "bmi_category": r["bmi_category"],
                    "health_score": r["health_score"],
                    "deficiencies": json.loads(r["deficiencies"] or "[]"),
                    "health_condition": r["health_condition"],
                    "recommended_foods": json.loads(r["recommended_foods"] or "[]"),
                    "foods_to_avoid": json.loads(r["foods_to_avoid"] or "[]"),
                    "lifestyle_advice": json.loads(r["lifestyle_advice"] or "[]"),
                    "supplement_suggestions": json.loads(r["supplement_suggestions"] or "[]"),
                    "urgency_level": r["urgency_level"],
                    "see_doctor": bool(r["see_doctor"]),
                    "see_doctor_reason": r["see_doctor_reason"],
                    "combined_diagnosis": r["combined_diagnosis"],
                    "blood_pressure": r["blood_pressure"],
                    "blood_sugar": r["blood_sugar"],
                    "hemoglobin": r["hemoglobin"],
                    "symptoms": json.loads(r["symptoms"] or "[]"),
                    "created_at": r["created_at"],
                })
            return results
        except:
            return []

    def get_latest_analysis(self, user_id):
        """Get latest analysis for user."""
        results = self.get_user_analyses(user_id, 1)
        return results[0] if results else None
