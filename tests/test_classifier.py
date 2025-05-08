import pytest
from unittest.mock import patch
from io import BytesIO
from werkzeug.datastructures import FileStorage
from src.classifier import classify_image_with_ollama, classify_text_with_ollama


@pytest.fixture
def dummy_file():
    file = BytesIO(b"fake image data")
    file.filename = "test.png"
    return FileStorage(stream=file, filename="test.png")


@pytest.fixture
def dummy_text_file():
    file = BytesIO(b"some text content")
    file.filename = "test.txt"
    return FileStorage(stream=file, filename="test.txt")


def test_classify_image_with_ollama_retries_and_fails(dummy_file):
    # First call returns unexpected value, second call also unexpected
    with patch("src.classifier.call_ollama") as mock_call:
        mock_call.side_effect = [
            {"type": "success", "value": "not_a_valid_option"},
            {"type": "success", "value": "still_invalid"}
        ]
        with patch("src.classifier.load_categories_for_industry", return_value=["drivers_license", "bank_statement"]):
            result = classify_image_with_ollama(dummy_file, "finance")
            assert result["type"] == "error"
            assert "unexpected value after retry" in result["value"].lower()


def test_classify_image_with_ollama_retries_and_succeeds(dummy_file):
    # First call returns unexpected, second call returns valid
    with patch("src.classifier.call_ollama") as mock_call:
        mock_call.side_effect = [
            {"type": "success", "value": "not_a_valid_option"},
            {"type": "success", "value": "drivers_license"}
        ]
        with patch("src.classifier.load_categories_for_industry", return_value=["drivers_license", "bank_statement"]):
            result = classify_image_with_ollama(dummy_file, "finance")
            assert result["type"] == "success"
            assert result["value"] == "drivers_license"


def test_classify_text_with_ollama_retries_and_fails(dummy_text_file):
    with patch("src.classifier.call_ollama") as mock_call:
        mock_call.side_effect = [
            {"type": "success", "value": "not_a_valid_option"},
            {"type": "success", "value": "still_invalid"}
        ]
        with patch("src.classifier.load_categories_for_industry", return_value=["drivers_license", "bank_statement"]):
            result = classify_text_with_ollama(dummy_text_file, "some text", "finance")
            assert result["type"] == "error"
            assert "unexpected value after retry" in result["value"].lower()


def test_classify_text_with_ollama_retries_and_succeeds(dummy_text_file):
    with patch("src.classifier.call_ollama") as mock_call:
        mock_call.side_effect = [
            {"type": "success", "value": "not_a_valid_option"},
            {"type": "success", "value": "bank_statement"}
        ]
        with patch("src.classifier.load_categories_for_industry", return_value=["drivers_license", "bank_statement"]):
            result = classify_text_with_ollama(dummy_text_file, "some text", "finance")
            assert result["type"] == "success"
            assert result["value"] == "bank_statement" 
