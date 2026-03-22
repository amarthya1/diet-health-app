"""Routine Routes"""
from flask import Blueprint, request, jsonify
from services.routine_service import RoutineService

routine_bp = Blueprint("routine", __name__)
svc = RoutineService()

@routine_bp.route("/generate-routine", methods=["POST"])
def generate():
    data = request.get_json()
    if not data or not data.get("user_id"):
        return jsonify({"message": "User ID required."}), 400
    result = svc.generate_routine(data)
    if "error" not in result:
        return jsonify(result), 200
    return jsonify(result), 400

@routine_bp.route("/get-routine/<int:user_id>", methods=["GET"])
def get_routine(user_id):
    result = svc.get_latest_routine(user_id)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "No routine found"}), 404

@routine_bp.route("/current/<int:user_id>", methods=["GET"])
def get_current(user_id):
    result = svc.get_latest_routine(user_id)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "No routine found"}), 404

# --- Reminders API ---
from database import get_connection
import json

@routine_bp.route("/reminders/save", methods=["POST"])
def save_reminders():
    data = request.get_json()
    if not data or not data.get("user_id"):
        return jsonify({"status": "error", "message": "User ID required"}), 400
    
    user_id = data.get("user_id")
    reminders = data.get("reminders", [])
    
    conn = get_connection()
    c = conn.cursor()
    try:
        # Delete only old routine reminders to prevent duplicate defaults
        c.execute("DELETE FROM reminders WHERE user_id=? AND category='routine'", (user_id,))
        for r in reminders:
            c.execute('''INSERT INTO reminders 
                (user_id, title, body, reminder_time, repeat_type, category, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                (user_id, r.get("title"), r.get("body", ""), r.get("time", ""), 
                 r.get("repeat", "daily"), r.get("category", "other"), 1))
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 500
    
    conn.close()
    return jsonify({"status": "success", "message": "Reminders saved"}), 200

@routine_bp.route("/reminders/save-defaults", methods=["POST"])
def save_defaults():
    data = request.get_json()
    if not data or not data.get("user_id"):
        return jsonify({"status": "error", "message": "User ID required"}), 400
    user_id = data.get("user_id")
    reminders = data.get("reminders", [])
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM reminders WHERE user_id=? AND category='routine'", (user_id,))
        for r in reminders:
            c.execute('''INSERT INTO reminders 
                (user_id, title, body, reminder_time, repeat_type, category, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                (user_id, r.get("title"), r.get("body", ""), r.get("time", ""), 
                 r.get("repeat", "daily"), r.get("category", "routine"), 1))
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 500
    conn.close()
    return jsonify({"status": "success", "message": "Default rems saved"}), 200

@routine_bp.route("/reminders/<int:user_id>", methods=["GET"])
def get_reminders(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM reminders WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()
    reminders = [dict(row) for row in rows]
    return jsonify({"status": "success", "reminders": reminders}), 200

@routine_bp.route("/reminders/add-custom", methods=["POST"])
def add_custom_reminder():
    data = request.get_json()
    if not data or not data.get("user_id"):
        return jsonify({"status": "error", "message": "User ID required"}), 400
    
    user_id = data.get("user_id")
    conn = get_connection()
    c = conn.cursor()
    rem_id = None
    try:
        c.execute('''INSERT INTO reminders 
            (user_id, title, body, reminder_time, repeat_type, category, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            (user_id, data.get("title"), data.get("body", ""), data.get("reminder_time", ""), 
             data.get("repeat_type", "once"), data.get("category", "other"), 1))
        conn.commit()
        rem_id = c.lastrowid
    except Exception as e:
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 500
    conn.close()
    return jsonify({"status": "success", "message": "Reminder added", "reminder_id": rem_id}), 200

@routine_bp.route("/reminders/update/<int:reminder_id>", methods=["PUT"])
def update_reminder(reminder_id):
    data = request.get_json()
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('''UPDATE reminders 
            SET title=?, body=?, reminder_time=?, repeat_type=? 
            WHERE id=?''', 
            (data.get("title"), data.get("body", ""), data.get("reminder_time", ""), 
             data.get("repeat_type", "daily"), reminder_id))
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 500
    conn.close()
    return jsonify({"status": "success", "message": "Reminder updated"}), 200

@routine_bp.route("/reminders/<int:reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 500
    conn.close()
    return jsonify({"status": "success", "message": "Reminder deleted"}), 200

