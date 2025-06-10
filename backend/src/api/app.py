from flask import Flask, jsonify
from flask_cors import CORS
from .dashboard_routes import dashboard_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy", "service": "WildGuard AI"})
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
