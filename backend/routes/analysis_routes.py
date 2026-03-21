"""Analysis Routes - Health score and nutrient gaps"""
from flask import Blueprint, request, jsonify
from services.health_service import HealthService

analysis_bp = Blueprint("analysis", __name__)
svc = HealthService()

@analysis_bp.route("/health-score/<int:user_id>", methods=["GET"])
def health_score(user_id):
    latest = svc.get_latest_analysis(user_id)
    if latest:
        return jsonify({"health_score": latest.get("health_score", 0), "bmi": latest.get("bmi"), "bmi_category": latest.get("bmi_category")}), 200
    return jsonify({"health_score": 0, "message": "No analysis found. Complete your first health analysis."}), 200

@analysis_bp.route("/nutrient-gaps", methods=["POST"])
def nutrient_gaps():
    data = request.get_json()
    user_id = data.get("user_id") if data else None
    if not user_id:
        return jsonify({"message": "User ID required."}), 400
    latest = svc.get_latest_analysis(user_id)
    if latest:
        return jsonify({"deficiencies": latest.get("deficiencies", []), "recommended_foods": latest.get("recommended_foods", []), "foods_to_avoid": latest.get("foods_to_avoid", [])}), 200
    return jsonify({"deficiencies": [], "message": "No analysis yet."}), 200
