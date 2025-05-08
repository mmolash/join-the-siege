from werkzeug.datastructures import FileStorage
from src.prompts import IMAGE_PROMPT
from dotenv import load_dotenv
import requests
import base64
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
OLLAMMA_URL = os.environ.get("OLLAMA_API_URL")


def classify_image_with_ollama(file: FileStorage, model: str="llava"):
    logger.info(f"Sending image to {model} for classification: {file.filename}")
    
    # Convert image to base64 for model
    image_bytes = file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    
    # Format request body
    data = {
        "model": model,
        "prompt": IMAGE_PROMPT,
        "images": [image_base64],
        "stream": False
    }

    try:
        # Make request to ollama
        response = requests.post(f"{OLLAMMA_URL}/api/generate", json=data, timeout=60)
        response.raise_for_status()

        result = response.json()
        logger.info(f"{model} response for {file.filename}: {result}")

        if "response" in result:
            return result["response"].strip().lower()
        return result.get("message", "unknown").strip().lower()
    except requests.RequestException as e:
        logger.error(f"HTTP error calling {model} for {file.filename}: {e}")
        return f"error: http error - {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error calling {model} for {file.filename}: {e}")
        return f"error: unexpected error - {str(e)}"


def classify_file(file: FileStorage):
    filename = file.filename.lower()
    extension = filename.rsplit(".", 1)[-1]

    if extension in ("jpg", "jpeg", "png"):
        file.seek(0)
        result = classify_image_with_ollama(file)
        logger.info(f"Classification result from Ollama: {result}")
        return result

    if "drivers_license" in filename:
        return "drivers_licence"

    if "bank_statement" in filename:
        return "bank_statement"

    if "invoice" in filename:
        return "invoice"

    return "unknown file"

