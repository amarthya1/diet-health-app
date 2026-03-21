"""User Routes"""
from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint("user", __name__)
svc = UserService()

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"success": False, "message": "Email and password required."}), 400
    result = svc.register(name=data.get("name"), email=data["email"], password=data["password"],
                          age=data.get("age"), gender=data.get("gender"),
                          height=data.get("height"), weight=data.get("weight"))
    code = 201 if result.get("success") else 400
    return jsonify(result), code

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"success": False, "message": "Email and password required."}), 400
    result = svc.login(email=data["email"], password=data["password"])
    code = 200 if result.get("success") else 401
    return jsonify(result), code

@user_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    if not data or not data.get("email"):
        return jsonify({"success": False, "message": "Email required."}), 400
    result = svc.forgot_password(data["email"])
    code = 200 if result.get("success") else 404
    return jsonify(result), code

@user_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    if not data or not data.get("token") or not data.get("password"):
        return jsonify({"success": False, "message": "Token and new password required."}), 400
    result = svc.reset_password(data["token"], data["password"])
    code = 200 if result.get("success") else 400
    return jsonify(result), code

@user_bp.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    profile = svc.get_profile(user_id)
    if profile:
        return jsonify(profile), 200
    return jsonify({"message": "User not found"}), 404

@user_bp.route("/profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    result = svc.update_profile(user_id, data)
    code = 200 if result.get("success") else 400
    return jsonify(result), code

@user_bp.route("/onboarding", methods=["POST"])
def save_onboarding():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    result = svc.save_onboarding(data)
    code = 200 if result.get("success") else 400
    return jsonify(result), code
