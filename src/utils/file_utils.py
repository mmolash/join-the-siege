import logging
import pypdf
from werkzeug.datastructures import FileStorage


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
            logging.error(f"Failed to extract text from PDF: {e}")
            return ""
    else:
        return "" 