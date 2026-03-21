"""
User Service - Registration, login, profile, onboarding, password reset.
"""
import json
import secrets
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection


class UserService:

    def register(self, name, email, password, **kwargs):
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE email=?", (email,))
            if c.fetchone():
                conn.close()
                return {"success": False, "message": "Email already registered."}
            hashed = generate_password_hash(password)
            now = datetime.utcnow().isoformat()
            c.execute('''INSERT INTO users (name,email,password_hash,age,gender,height,weight,created_at,updated_at)
                         VALUES (?,?,?,?,?,?,?,?,?)''',
                      (name, email, hashed, kwargs.get("age"), kwargs.get("gender"),
                       kwargs.get("height"), kwargs.get("weight"), now, now))
            conn.commit()
            uid = c.lastrowid
            conn.close()
            return {"success": True, "user_id": uid, "message": "Registration successful."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def login(self, email, password):
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email=?", (email,))
            user = c.fetchone()
            conn.close()
            if user and check_password_hash(user["password_hash"], password):
                return {
                    "success": True,
                    "message": "Login successful.",
                    "user": {
                        "id": user["id"], "name": user["name"], "email": user["email"],
                        "age": user["age"], "gender": user["gender"],
                        "height": user["height"], "weight": user["weight"],
                        "food_preference": user["food_preference"],
                        "health_goals": user["health_goals"],
                        "activity_level": user["activity_level"],
                    }
                }
            return {"success": False, "message": "Invalid email or password."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def forgot_password(self, email):
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE email=?", (email,))
            user = c.fetchone()
            if not user:
                conn.close()
                return {"success": False, "message": "Email not found."}
            token = secrets.token_urlsafe(32)
            c.execute("UPDATE users SET reset_token=? WHERE id=?", (token, user["id"]))
            conn.commit()
            conn.close()
            return {"success": True, "message": "Reset token generated.", "reset_token": token}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def reset_password(self, token, new_password):
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE reset_token=?", (token,))
            user = c.fetchone()
            if not user:
                conn.close()
                return {"success": False, "message": "Invalid or expired token."}
            hashed = generate_password_hash(new_password)
            c.execute("UPDATE users SET password_hash=?, reset_token=NULL, updated_at=? WHERE id=?",
                      (hashed, datetime.utcnow().isoformat(), user["id"]))
            conn.commit()
            conn.close()
            return {"success": True, "message": "Password reset successful."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_profile(self, user_id):
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=?", (user_id,))
            u = c.fetchone()
            conn.close()
            if u:
                return {
                    "id": u["id"], "name": u["name"], "email": u["email"],
                    "age": u["age"], "gender": u["gender"],
                    "height": u["height"], "weight": u["weight"],
                    "food_preference": u["food_preference"],
                    "allergies": u["allergies"],
                    "health_goals": u["health_goals"],
                    "medications": u["medications"],
                    "activity_level": u["activity_level"],
                    "theme_preference": u["theme_preference"],
                    "created_at": u["created_at"],
                }
            return None
        except:
            return None

    def update_profile(self, user_id, data):
        try:
            conn = get_connection()
            c = conn.cursor()
            allowed = ["name","age","gender","height","weight","food_preference","allergies",
                        "health_goals","medications","activity_level","theme_preference"]
            fields, vals = [], []
            for k in allowed:
                if k in data:
                    fields.append(f"{k}=?")
                    v = data[k]
                    if isinstance(v, (list, dict)):
                        v = json.dumps(v)
                    vals.append(v)
            if not fields:
                conn.close()
                return {"success": False, "message": "No fields to update."}
            vals.append(datetime.utcnow().isoformat())
            vals.append(user_id)
            c.execute(f"UPDATE users SET {','.join(fields)}, updated_at=? WHERE id=?", tuple(vals))
            conn.commit()
            conn.close()
            return {"success": True, "message": "Profile updated."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def save_onboarding(self, data):
        user_id = data.get("user_id")
        if not user_id:
            return {"success": False, "message": "User ID required."}
        onboard_fields = {}
        for k in ["age","gender","height","weight","food_preference","allergies",
                   "health_goals","medications","activity_level"]:
            if k in data:
                v = data[k]
                if isinstance(v, (list, dict)):
                    v = json.dumps(v)
                onboard_fields[k] = v
        return self.update_profile(user_id, onboard_fields)
