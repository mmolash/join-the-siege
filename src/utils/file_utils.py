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
            # Only consider the first 2 pages of the PDF
            # for speed and to avoid context window issues
            # Relevant context should be at the beginning of the document
            for page in reader.pages[:2]:
                text += page.extract_text() or ""
            
            return text
        except Exception as e:
            logging.error(f"Failed to extract text from PDF: {e}")
            return ""
    else:
        return "" 