"""Health Routes"""
from flask import Blueprint, request, jsonify
from services.health_service import HealthService

health_bp = Blueprint("health", __name__)
svc = HealthService()

@health_bp.route("/analyze-health", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or not data.get("user_id"):
        return jsonify({"message": "User ID required."}), 400
    result = svc.analyze_health(data)
    if not result.get("error"):
        return jsonify(result), 200
    return jsonify(result), 400

@health_bp.route("/history/<int:user_id>", methods=["GET"])
def history(user_id):
    limit = request.args.get("limit", 5, type=int)
    return jsonify(svc.get_user_analyses(user_id, limit)), 200

@health_bp.route("/latest/<int:user_id>", methods=["GET"])
def latest(user_id):
    result = svc.get_latest_analysis(user_id)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "No analysis found"}), 404
