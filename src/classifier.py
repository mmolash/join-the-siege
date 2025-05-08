from werkzeug.datastructures import FileStorage
from dotenv import load_dotenv
import src.prompts as prompts
import requests
import base64
import logging
import os
import pypdf


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
OLLAMMA_URL = os.environ.get("OLLAMA_API_URL")


def call_ollama(data, file: FileStorage, model: str):
    try:
        logger.info(f"Sending request to {model} for file: {file.filename}")

        response = requests.post(f"{OLLAMMA_URL}/api/generate", json=data, timeout=60)
        response.raise_for_status()

        result = response.json()
        if "response" in result:
            return result["response"].strip().lower()

        return result.get("message", "unknown").strip().lower()

    except requests.RequestException as e:
        logger.error(f"HTTP error calling {model} for {file.filename}: {e}")
        return f"error: http error - {str(e)}"

    except Exception as e:
        logger.error(f"Unexpected error calling {model} for {file.filename}: {e}")
        return f"error: unexpected error - {str(e)}"


def classify_image_with_ollama(file: FileStorage, model: str="llava"):
    logger.info(f"Sending image to {model} for classification: {file.filename}")

    image_bytes = file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    data = {
        "model": model,
        "prompt": prompts.IMAGE_PROMPT.format(filename=file.filename),
        "images": [image_base64],
        "stream": False
    }

    return call_ollama(data, file, model)


def classify_text_with_ollama(file: FileStorage, text: str, model: str="llava"):
    logger.info(f"Sending text to {model} for classification from file: {file.filename}")

    data = {
        "model": model,
        "system": prompts.TEXT_PROMPT.format(filename=file.filename, text=text),
        "prompt": f"File name: {file.filename}\nFile content: {text}",
        "stream": False
    }

    return call_ollama(data, file, model)


def extract_text_from_file(file: FileStorage, extension: str) -> str:
    if extension == "txt":
        return file.read().decode("utf-8", errors="ignore")
    elif extension == "pdf":
        try:
            reader = pypdf.PdfReader(file)

            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            
            return text
        
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            return ""
    return ""


def classify_file(file: FileStorage):
    filename = file.filename.lower()
    extension = filename.rsplit(".", 1)[-1]

    if extension in ("jpg", "jpeg", "png"):
        file.seek(0)
        result = classify_image_with_ollama(file)
        return result
    
    if extension in ("txt", "pdf"):
        text = extract_text_from_file(file, extension)
        result = classify_text_with_ollama(file, text)
        return result

    return "unknown file"

