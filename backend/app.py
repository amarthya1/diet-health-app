"""
Diet & Health App - Flask Backend
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__, static_folder=None)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    from routes.user_routes import user_bp
    from routes.health_routes import health_bp
    from routes.diet_routes import diet_bp
    from routes.routine_routes import routine_bp
    from routes.progress_routes import progress_bp
    from routes.analysis_routes import analysis_bp

    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(health_bp, url_prefix="/api/health")
    app.register_blueprint(diet_bp, url_prefix="/api/diet")
    app.register_blueprint(routine_bp, url_prefix="/api/routine")
    app.register_blueprint(progress_bp, url_prefix="/api/progress")
    app.register_blueprint(analysis_bp, url_prefix="/api/analysis")

    frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend_web")

    @app.route("/", methods=["GET"])
    def serve_index():
        return send_from_directory(frontend_dir, "login.html")

    @app.route("/<path:filename>", methods=["GET"])
    def serve_static(filename):
        fp = os.path.join(frontend_dir, filename)
        if os.path.isfile(fp):
            return send_from_directory(frontend_dir, filename)
        fp_html = fp + ".html"
        if os.path.isfile(fp_html):
            return send_from_directory(frontend_dir, filename + ".html")
        return send_from_directory(frontend_dir, "login.html")

    @app.route("/api/status", methods=["GET"])
    def status():
        return jsonify({"status": "ok", "message": "Diet & Health API running"}), 200

    @app.before_request
    def log_req():
        if request.path.startswith("/api/"):
            print(f"[API] {request.method} {request.path}")

    # Print routes on start
    for rule in app.url_map.iter_rules():
        print(f"  Route: {rule.rule} [{','.join(rule.methods - {'OPTIONS','HEAD'})}]")

    return app

if __name__ == "__main__":
    from database import init_db, migrate_db
    init_db()
    migrate_db()
    app = create_app()
    print("\n  Diet & Health Backend running on http://0.0.0.0:5001\n")
    app.run(host="0.0.0.0", port=5001, debug=True)
