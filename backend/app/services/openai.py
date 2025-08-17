"""Utilidades para analizar una imagen con OpenAI Responses API.

Se expone `analyze_image` (ruta de archivo) y `analyze_image_bytes` (bytes en memoria)
para permitir integración directa con el endpoint de subida sin escribir a disco.
Requiere variable de entorno OPENAI_API_KEY.
"""

import os
import base64
from openai import OpenAI


def encode_image(image_path: str) -> str:
	with open(image_path, "rb") as image_file:
		return base64.b64encode(image_file.read()).decode("utf-8")


def encode_image_bytes(data: bytes) -> str:
	return base64.b64encode(data).decode("utf-8")


def _client() -> OpenAI:
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key:
		raise RuntimeError("OPENAI_API_KEY no configurada")
	return OpenAI()


def _call_model(b64: str, question: str) -> str:
	client = _client()
	response = client.responses.create(
		model=os.getenv("OPENAI_MODEL"),
		instructions=question,
		input=[
			{
				"role": "developer",
				"content": question,
			},
			{
				"role": "user",
				"content": [
					{"type": "input_image", "image_url": f"data:image/jpeg;base64,{b64}"},
				],
			}
		],
		text={"format": {"type": "json_object"}},
		temperature=0.7,
	)
	print(f"OpenAI response: {response}")
	return response.output_text


def analyze_image(image_path: str, question: str = "what's in this image?") -> str:
	b64 = encode_image(image_path)
	return _call_model(b64, question)


def analyze_image_bytes(data: bytes, question: str = "what's in this image?") -> str:
	b64 = encode_image_bytes(data)
	return _call_model(b64, question)


if __name__ == "__main__":
	# Ejecución manual de ejemplo
	path = os.getenv("TEST_IMAGE_PATH", "path_to_your_image.jpg")
	try:
		result = analyze_image(path)
		print(result)
	except Exception as e:  # pragma: no cover - script manual
		print(f"Error: {e}")
