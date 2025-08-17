from flask import Blueprint, request, jsonify, current_app
from ..validation import validate_image
from ..services.openai import analyze_image_bytes
import json
import os

# Cargar prompts.json al iniciar el módulo
PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "prompts.json")
with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
    PROMPTS = json.load(f)

upload_bp = Blueprint("upload", __name__, url_prefix="/api")


@upload_bp.post("/analyze")
def upload_image():
    """Endpoint que recibe y valida una imagen.

    No guarda ni procesa la imagen: solo valida entrada y tipo.
    Respuestas:
      200 OK -> { message, filename, format }
      400 Bad Request -> { error }
    """
    if "file" not in request.files:
        return jsonify({"error": "Campo 'file' requerido (multipart/form-data)"}), 400

    file = request.files["file"]
    is_valid, err = validate_image(file)
    if not is_valid:
        return jsonify({"error": err}), 400

    import imghdr

    head = file.stream.read(2048)
    file.stream.seek(0)
    img_format = imghdr.what(None, h=head)

    description = None
    try:
        # Leer bytes completos (limitado por MAX_CONTENT_LENGTH ya aplicado por Flask)
        data = file.read()
        file.stream.seek(0)
        description = analyze_image_bytes(data, PROMPTS["analyze_img_v2"])
    except Exception as e:  # pragma: no cover - dependencias externas
        # Log a consola (docker logs) con stacktrace
        current_app.logger.exception(
            "Fallo analizando imagen con OpenAI (filename=%s)", file.filename
        )
        # No romper por fallo de OpenAI; devolver advertencia
        return jsonify({
            "message": "Imagen válida recibida, pero fallo analizando con OpenAI",
            "filename": file.filename,
            "format": img_format,
            "analysis_error": str(e),
        }), 200

    return jsonify({
        "message": "Imagen válida recibida",
        "filename": file.filename,
        "format": img_format,
        "analysis": description,
        "max_size_bytes": current_app.config.get("MAX_CONTENT_LENGTH"),
    }), 200
