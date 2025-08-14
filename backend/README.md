s# API de carga de imagen (validación)

Servicio Flask simple con un único endpoint para validar una imagen enviada vía `multipart/form-data`.

## Endpoint

POST /api/upload-image

Body (multipart/form-data):
  - file: archivo de imagen.

Respuestas:
  - 200: JSON con `message`, `filename`, `format`, `max_size_bytes`.
  - 400: JSON con `error`.

## Ejecución con Docker Compose

```bash
docker compose up --build
```

Luego probar:
```bash
curl -X POST http://localhost:8000/api/upload-image \
  -F "file=@ruta/a/imagen.png"
```

## Variables de entorno soportadas
APP_ENV (dev|prod)  (default: dev)
PORT                (default: 8000)
MAX_CONTENT_LENGTH  (bytes, default 5242880 = 5MB)

## Notas
No se almacena el archivo ni se procesa, sólo se valida su tipo usando `imghdr`.
