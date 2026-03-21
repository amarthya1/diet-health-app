"""Diet Routes"""
from flask import Blueprint, request, jsonify
from services.diet_service import DietService

diet_bp = Blueprint("diet", __name__)
svc = DietService()

@diet_bp.route("/generate-diet", methods=["POST"])
def generate():
    data = request.get_json()
    if not data or not data.get("user_id"):
        return jsonify({"message": "User ID required."}), 400
    result = svc.generate_diet(data)
    if "error" not in result:
        return jsonify(result), 200
    return jsonify(result), 400

@diet_bp.route("/get-plan/<int:user_id>", methods=["GET"])
def get_plan(user_id):
    plan = svc.get_latest_diet(user_id)
    if plan:
        return jsonify(plan), 200
    return jsonify({"message": "No diet plan found"}), 404

# Keep backward compat
@diet_bp.route("/current/<int:user_id>", methods=["GET"])
def get_current(user_id):
    plan = svc.get_latest_diet(user_id)
    if plan:
        return jsonify(plan), 200
    return jsonify({"message": "No diet plan found"}), 404
