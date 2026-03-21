"""Progress Routes"""
from flask import Blueprint, request, jsonify
from services.progress_service import ProgressService

progress_bp = Blueprint("progress", __name__)
svc = ProgressService()

@progress_bp.route("/log", methods=["POST"])
def log():
    data = request.get_json()
    if not data or not data.get("user_id"):
        return jsonify({"message": "User ID required."}), 400
    result = svc.log_progress(data)
    if not result.get("error"):
        return jsonify(result), 200
    return jsonify(result), 400

@progress_bp.route("/<int:user_id>", methods=["GET"])
def history(user_id):
    limit = request.args.get("limit", 30, type=int)
    return jsonify(svc.get_progress_history(user_id, limit)), 200

@progress_bp.route("/weekly/<int:user_id>", methods=["GET"])
def weekly(user_id):
    summary = svc.get_weekly_summary(user_id)
    return jsonify(summary), 200
