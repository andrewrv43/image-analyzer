import imghdr
from werkzeug.datastructures import FileStorage

ALLOWED_FORMATS = {"jpeg", "png", "gif", "bmp", "tiff", "webp"}


def validate_image(file: FileStorage) -> tuple[bool, str | None]:
    """Validate that uploaded file looks like an image.

    Returns (is_valid, error_message).
    We only read a small header chunk to identify type.
    """
    if file.filename == "":
        return False, "Nombre de archivo vacío"

    pos = file.stream.tell()
    head = file.stream.read(2048)
    file.stream.seek(pos)
    kind = imghdr.what(None, h=head)
    if kind is None:
        return False, "Archivo no es una imagen válida"
    if kind not in ALLOWED_FORMATS:
        return False, f"Formato no permitido: {kind}"
    return True, None
