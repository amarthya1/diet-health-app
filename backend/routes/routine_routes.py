"""
Routine Routes - Endpoints for daily routines
"""

from flask import Blueprint, request, jsonify
from services.routine_service import RoutineService

routine_bp = Blueprint("routine", __name__)
routine_service = RoutineService()

@routine_bp.route("/generate-routine", methods=["POST"])
def generate_routine():
    """Generate a daily routine based on user goals."""
    data = request.get_json() or {}
    user_goal = data.get("user_goal", "")
    
    result = routine_service.generate_routine(user_goal)
    return jsonify(result)
