import re


def normalize_whitespace(text):
    """
    Replace repeated whitespace with a single space.
    """
    return re.sub(r"\s+", " ", text).strip()


def preprocess_text(text):
    """
    Perform basic text preprocessing.

    The preprocessing is intentionally conservative because
    technical skill names should not be accidentally removed.
    """
    if not text:
        return ""

    text = text.lower()

    text = normalize_whitespace(text)

    return text