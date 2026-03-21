"""
Diet Routes - Meal plans, food logging, calorie tracking
"""

from flask import Blueprint, request, jsonify
from services.diet_service import DietService

diet_bp = Blueprint("diet", __name__)
diet_service = DietService()


@diet_bp.route("/meal-plan", methods=["GET"])
def get_meal_plan():
    """Get a personalized meal plan for the user."""
    user_id = request.args.get("user_id")
    calories = request.args.get("calories", 2000, type=int)
    goal = request.args.get("goal", "maintain")  # lose | maintain | gain
    plan = diet_service.generate_meal_plan(user_id, calories, goal)
    return jsonify(plan)


@diet_bp.route("/log-meal", methods=["POST"])
def log_meal():
    """Log a meal entry for the user."""
    data = request.get_json()
    result = diet_service.log_meal(
        user_id=data["user_id"],
        meal_name=data["meal_name"],
        calories=data["calories"],
        macros=data.get("macros", {}),
    )
    return jsonify(result), 201


@diet_bp.route("/food-search", methods=["GET"])
def search_food():
    """Search for food nutrition information."""
    query = request.args.get("q", "")
    results = diet_service.search_food(query)
    return jsonify(results)


@diet_bp.route("/history/<user_id>", methods=["GET"])
def meal_history(user_id):
    """Get meal history for a user."""
    days = request.args.get("days", 7, type=int)
    history = diet_service.get_meal_history(user_id, days)
    return jsonify(history)


@diet_bp.route("/calories/<user_id>", methods=["GET"])
def daily_calories(user_id):
    """Get today's calorie summary for a user."""
    summary = diet_service.get_daily_calories(user_id)
    return jsonify(summary)


@diet_bp.route("/generate-diet", methods=["POST"])
def generate_diet():
    """Generate a diet plan based on preference and deficiencies."""
    data = request.get_json()
    result = diet_service.generate_diet(
        food_preference=data.get("food_preference", "veg"),
        deficiency=data.get("deficiency", [])
    )
    return jsonify(result)
