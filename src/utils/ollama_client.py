import requests
import logging
import os
from werkzeug.datastructures import FileStorage


def call_ollama(data, file: FileStorage, model: str, ollama_url: str):
    try:
        logging.info(f"Sending request to {model} for file: {file.filename}")

        response = requests.post(f"{ollama_url}/api/generate", json=data, timeout=60)
        response.raise_for_status()

        result = response.json()

        if "response" in result:
            return {"type": "success", "value": result["response"].strip().lower()}

        return {"type": "error", "value": result.get("message", "Unknown error.").strip().lower()}
    except requests.RequestException as e:
        logging.error(f"HTTP error calling {model} for {file.filename}: {e}")

        return {"type": "error", "value": f"HTTP Error: {str(e)}"}
    except Exception as e:
        logging.error(f"Unexpected error calling {model} for {file.filename}: {e}")
        
        return {"type": "error", "value": f"Unexpected Error: {str(e)}"} 