import pytest
from src.utils.config_utils import get_supported_industries, load_categories_for_industry
from src.utils.prompt_utils import format_options
from src.utils.file_utils import extract_text_from_file
from io import BytesIO


def test_get_supported_industries():
    industries = get_supported_industries()
    assert "finance" in industries
    assert "legal" in industries
    assert "notrealindustry" not in industries
    assert isinstance(industries, list)


def test_load_categories_for_industry():
    categories = load_categories_for_industry("finance")
    assert "drivers_license" in categories
    assert "bank_statement" in categories
    assert "invoice" in categories
    assert "notrealcategory" not in categories
    assert load_categories_for_industry("notarealindustry") == []


def test_format_options():
    options = ["foo", "bar"]
    formatted = format_options(options)
    assert formatted == "- foo\n- bar"


def test_extract_text_from_txt_file():
    file = BytesIO(b"hello world")
    file.filename = "test.txt"
    text = extract_text_from_file(file, "txt")
    assert "hello world" in text


def test_extract_text_from_unsupported_file():
    file = BytesIO(b"")
    file.filename = "test.xyz"
    text = extract_text_from_file(file, "xyz")
    assert text == ""
