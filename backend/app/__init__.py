from flask import Flask, jsonify
from .config import Config


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    from .routes.upload import upload_bp
    app.register_blueprint(upload_bp)

    @app.get("/health")
    def health():  # pragma: no cover - trivial
        return {"status": "ok"}

    # Error handlers (simple, JSON consistent)
    @app.errorhandler(413)  # Payload too large
    def payload_too_large(_):  # pragma: no cover - trivial
        return jsonify({"error": "Archivo demasiado grande"}), 413

    @app.errorhandler(404)
    def not_found(_):  # pragma: no cover
        return jsonify({"error": "No encontrado"}), 404

    @app.errorhandler(500)
    def server_error(_):  # pragma: no cover
        return jsonify({"error": "Error interno"}), 500

    return app


# Exponer instancia para gunicorn: 'gunicorn app:app'
app = create_app()
