"""
Diet & Health Analysis App - Flask Backend Entry Point
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from routes.user_routes import user_bp
from routes.diet_routes import diet_bp
from routes.health_routes import health_bp
from routes.analysis_routes import analysis_bp
from routes.routine_routes import routine_bp
import os

def create_app():
    app = Flask(__name__, static_folder=None)
    
    # Fix and enforce CORS for Flutter web frontend
    # Ensures port 5001 is recognized by Chrome and no 'Failed to fetch' errors occur
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(user_bp,     url_prefix="/api/user")
    app.register_blueprint(diet_bp,     url_prefix="/api/diet")
    app.register_blueprint(health_bp,   url_prefix="/api/health")
    app.register_blueprint(analysis_bp, url_prefix="/api/analysis")
    app.register_blueprint(routine_bp,  url_prefix="/api/routine")

    # Serve frontend static files
    frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend_web")

    @app.route("/", methods=["GET"])
    def serve_index():
        """Serve the main login.html page."""
        return send_from_directory(frontend_dir, "login.html")

    @app.route("/<path:filename>", methods=["GET"])
    def serve_static(filename):
        """Serve static files (HTML, CSS, JS, etc.) from frontend_web folder."""
        return send_from_directory(frontend_dir, filename)

    @app.before_request
    def log_request_info():
        """Request logging for debugging."""
        print(f"[{request.method}] {request.url}")
        if request.is_json:
            print("Payload:", request.get_json())

    @app.route("/api/status", methods=["GET"])
    def api_status():
        return jsonify({
            "status": "ok", 
            "message": "Diet & Health API is running"
        }), 200

    return app

if __name__ == "__main__":
    app = create_app()
    # Run on 0.0.0.0 to allow access from any device on the network
    print("Starting Flask Backend + Frontend on http://0.0.0.0:5001")
    print("Access from this machine: http://localhost:5001 or http://127.0.0.1:5001")
    print("Access from other devices on network: http://<YOUR-MACHINE-IP>:5001")
    app.run(host="0.0.0.0", port=5001, debug=True)
