from src.preprocessing import (
    normalize_whitespace,
    preprocess_text,
)


def test_normalize_whitespace():
    text = "Python    Flask   Machine Learning"

    result = normalize_whitespace(text)

    assert result == "Python Flask Machine Learning"


def test_preprocess_text():
    text = "  Python   FLASK   Machine Learning  "

    result = preprocess_text(text)

    assert result == "python flask machine learning"


def test_empty_text():
    assert preprocess_text("") == ""


def test_none_text():
    assert preprocess_text(None) == ""