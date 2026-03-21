"""
Analysis Routes - AI-powered diet & health analysis
"""

from flask import Blueprint, request, jsonify
from services.analysis_service import AnalysisService

analysis_bp = Blueprint("analysis", __name__)
analysis_service = AnalysisService()


@analysis_bp.route("/weekly-report/<user_id>", methods=["GET"])
def weekly_report(user_id):
    """Generate a weekly health & diet analysis report."""
    report = analysis_service.generate_weekly_report(user_id)
    return jsonify(report)


@analysis_bp.route("/nutrient-gaps/<user_id>", methods=["GET"])
def nutrient_gaps(user_id):
    """Identify nutritional deficiencies or excesses."""
    gaps = analysis_service.analyze_nutrient_gaps(user_id)
    return jsonify(gaps)


@analysis_bp.route("/vitamin-check/<user_id>", methods=["GET"])
def vitamin_check(user_id):
    """Check vitamin and mineral intake levels."""
    result = analysis_service.check_vitamins(user_id)
    return jsonify(result)


@analysis_bp.route("/progress/<user_id>", methods=["GET"])
def progress(user_id):
    """Get progress towards user's health goals."""
    result = analysis_service.get_progress(user_id)
    return jsonify(result)


@analysis_bp.route("/ai-insights/<user_id>", methods=["GET"])
def ai_insights(user_id):
    """Get AI-generated personalized health insights."""
    insights = analysis_service.generate_ai_insights(user_id)
    return jsonify(insights)
