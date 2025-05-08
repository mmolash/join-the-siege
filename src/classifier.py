from werkzeug.datastructures import FileStorage
from dotenv import load_dotenv
import base64
import logging
import os
import src.prompts as prompts

from src.utils.file_utils import extract_text_from_file
from src.utils.config_utils import load_categories_for_industry
from src.utils.prompt_utils import format_options
from src.utils.ollama_client import call_ollama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

OLLAMMA_URL = os.environ.get("OLLAMA_API_URL")


def classify_image_with_ollama(file: FileStorage, industry: str, model: str="llava"):
    options = load_categories_for_industry(industry)
    options_str = format_options(options)

    logger.info(f"Sending image ({file.filename}) to {model} for classification in {industry}. Options are {options}")

    image_bytes = file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    data = {
        "model": model,
        "prompt": prompts.IMAGE_PROMPT.format(filename=file.filename, options=options_str),
        "images": [image_base64],
        "stream": False
    }

    return call_ollama(data, file, model, ollama_url=OLLAMMA_URL)


def classify_text_with_ollama(file: FileStorage, text: str, industry: str, model: str="llava"):
    options = load_categories_for_industry(industry)
    options_str = format_options(options)

    logger.info(f"Sending text ({file.filename}) to {model} for classification in {industry}. Options are {options}")

    data = {
        "model": model,
        "system": prompts.TEXT_PROMPT.format(filename=file.filename, text=text, options=options_str),
        "prompt": f"File name: {file.filename}\nFile content: {text}",
        "stream": False
    }

    return call_ollama(data, file, model, ollama_url=OLLAMMA_URL)


def classify_file(file: FileStorage, industry: str):
    filename = file.filename.lower()
    extension = filename.rsplit(".", 1)[-1]

    if extension in ("jpg", "jpeg", "png"):
        result = classify_image_with_ollama(file, industry)
        return result

    if extension in ("txt", "pdf"):
        text = extract_text_from_file(file, extension)
        result = classify_text_with_ollama(file, text, industry)
        return result
    
    return {"type": "error", "value": "Unsupported file type."}
