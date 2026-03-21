"""
Health Routes - BMI, vitals tracking, health metrics
"""

from flask import Blueprint, request, jsonify
from services.health_service import HealthService
from services.analysis_service import AnalysisService

health_bp = Blueprint("health", __name__)
health_service = HealthService()
analysis_service = AnalysisService()


@health_bp.route("/bmi", methods=["POST"])
def calculate_bmi():
    """Calculate BMI and provide health category."""
    data = request.get_json()
    result = health_service.calculate_bmi(
        weight_kg=data["weight_kg"],
        height_cm=data["height_cm"],
    )
    return jsonify(result)


@health_bp.route("/tdee", methods=["POST"])
def calculate_tdee():
    """Calculate Total Daily Energy Expenditure."""
    data = request.get_json()
    result = health_service.calculate_tdee(
        weight_kg=data["weight_kg"],
        height_cm=data["height_cm"],
        age=data["age"],
        gender=data["gender"],
        activity_level=data.get("activity_level", "moderate"),
    )
    return jsonify(result)


@health_bp.route("/log-vitals", methods=["POST"])
def log_vitals():
    """Log health vitals for a user."""
    data = request.get_json()
    result = health_service.log_vitals(
        user_id=data["user_id"],
        weight=data.get("weight"),
        blood_pressure=data.get("blood_pressure"),
        blood_sugar=data.get("blood_sugar"),
        heart_rate=data.get("heart_rate"),
    )
    return jsonify(result), 201


@health_bp.route("/vitals/<user_id>", methods=["GET"])
def get_vitals(user_id):
    """Get vitals history for a user."""
    days = request.args.get("days", 30, type=int)
    vitals = health_service.get_vitals_history(user_id, days)
    return jsonify(vitals)


@health_bp.route("/recommendations/<user_id>", methods=["GET"])
def get_recommendations(user_id):
    """Get personalized health recommendations."""
    recommendations = health_service.get_recommendations(user_id)
    return jsonify(recommendations)


@health_bp.route("/analyze-health", methods=["POST"])
def analyze_health():
    """Analyze health metrics and symptoms."""
    data = request.get_json()
    result = analysis_service.analyze_health(
        height=data.get("height", 0),
        weight=data.get("weight", 0),
        age=data.get("age", 0),
        symptoms=data.get("symptoms", []),
        food_preference=data.get("food_preference", "veg")
    )
    return jsonify(result)
