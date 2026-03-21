"""
User Routes - Registration, profile management
"""

import os
import json
from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint("user", __name__)
user_service = UserService()

@user_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Invalid input, email and password required."}), 400
        
    result = user_service.register(
        name=data.get("name"),
        email=data.get("email"),
        password=data.get("password"),
        age=data.get("age"),
        gender=data.get("gender")
    )
    
    if not result.get("success"):
        return jsonify({"message": result.get("message")}), 400
        
    return jsonify({"message": "User registered successfully", "user_id": result.get("user_id")}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    """Authenticate a user and return a token."""
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Email and password required."}), 400
        
    result = user_service.login(email=data["email"], password=data["password"])
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 401


@user_bp.route("/profile", methods=["POST"])
def save_profile():
    """Save or update an extended user profile."""
    data = request.get_json() or {}
    required = ["email", "goal", "problems", "gender", "age", "height", "weight", "food_preference", "allergies", "medications"]
    missing = [key for key in required if key not in data]
    if missing:
        return jsonify({"message": f"Missing fields: {', '.join(missing)}"}), 400

    users_file = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")
    os.makedirs(os.path.dirname(users_file), exist_ok=True)

    if os.path.exists(users_file):
        with open(users_file, "r", encoding="utf-8") as f:
            try:
                users_data = json.load(f)
            except json.JSONDecodeError:
                users_data = {}
    else:
        users_data = {}

    email = data["email"]

    users_data[email] = {
        "email": email,
        "goal": data.get("goal"),
        "problems": data.get("problems", []),
        "gender": data.get("gender"),
        "age": data.get("age"),
        "height": data.get("height"),
        "weight": data.get("weight"),
        "food_preference": data.get("food_preference"),
        "allergies": data.get("allergies"),
        "medications": data.get("medications")
    }

    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users_data, f, indent=4)

    return jsonify({"message": "Profile saved successfully", "status": "ok"}), 200


@user_bp.route("/profile", methods=["GET"])
def profile():
    """Get user profile from token in Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        email = request.args.get("email") # fallback for simplified debugging
        if not email:
            return jsonify({"message": "No token or email provided"}), 401
        token = email
    else:
        # Expected header: 'Bearer token_value'
        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    
    profile_data = user_service.get_profile(token)
    if profile_data:
        return jsonify(profile_data), 200
    return jsonify({"error": "User not found"}), 404
