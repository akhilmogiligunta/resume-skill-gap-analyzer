import json
import re
from pathlib import Path

SKILLS_FILE = Path(__file__).resolve().parent.parent / "config" / "skills.json"


def load_skills():
    """Load the configurable skill dictionary."""
    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("skills", {})


def normalize_skill_text(text):
    """
    Normalize resume/JD text before skill matching.

    Handles:
    - Upper/lower case differences
    - Multiple spaces
    - Spaces around dots and punctuation
    - Common PDF extraction formatting issues
    """
    if not text:
        return ""

    text = text.lower()

    # Normalize common punctuation spacing.
    # Example:
    # "React . js" -> "react.js"
    # "Node . js" -> "node.js"
    text = re.sub(r"\s*\.\s*", ".", text)

    # Normalize hyphen spacing.
    # Example:
    # "machine - learning" -> "machine-learning"
    text = re.sub(r"\s*-\s*", "-", text)

    # Normalize slash spacing.
    text = re.sub(r"\s*/\s*", "/", text)

    # Collapse repeated whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_alias(alias):
    """
    Normalize a skill alias in the same way as resume text.
    """
    return normalize_skill_text(alias)


def create_alias_pattern(alias):
    """
    Create a safe regex pattern for matching a complete skill alias.

    Word boundaries prevent partial matches such as:
    'java' matching inside 'javascript'.
    """
    normalized_alias = normalize_alias(alias)

    escaped_alias = re.escape(normalized_alias)

    return rf"(?<!\w){escaped_alias}(?!\w)"


def extract_skills(text):
    """
    Extract recognized skills from resume or job-description text.

    Returns a dictionary keyed by the skill ID defined in skills.json.
    """
    if not text:
        return {}

    normalized_text = normalize_skill_text(text)
    skills = load_skills()

    detected_skills = {}

    for skill_key, skill_data in skills.items():
        aliases = skill_data.get("aliases", [])
        display_name = skill_data.get("display_name", skill_key)
        category = skill_data.get("category", "Other")

        for alias in aliases:
            pattern = create_alias_pattern(alias)

            if re.search(pattern, normalized_text):
                detected_skills[skill_key] = {
                    "name": display_name,
                    "category": category,
                    "matched_alias": alias
                }
                break

    return detected_skills


def get_skill_names(text):
    """
    Return detected skill display names in alphabetical order.
    """
    skills = extract_skills(text)

    return sorted(
        skill["name"]
        for skill in skills.values()
    )