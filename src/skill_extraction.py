import json
import re
from pathlib import Path


SKILLS_FILE = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "skills.json"
)


def load_skills():
    """
    Load the configurable skill dictionary.
    """
    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("skills", {})


def normalize_skill_text(text):
    """
    Normalize text for skill matching.
    """
    if not text:
        return ""

    text = text.lower()

    # Normalize common variations of whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def create_alias_pattern(alias):
    """
    Create a regex pattern for a skill alias.

    Word boundaries help prevent accidental partial matches.
    """
    escaped_alias = re.escape(alias.lower())

    return rf"(?<!\w){escaped_alias}(?!\w)"


def extract_skills(text):
    """
    Extract known skills from text.

    Returns a dictionary containing the canonical skill,
    display name, category, and matched alias.
    """
    if not text:
        return {}

    normalized_text = normalize_skill_text(text)
    skills = load_skills()

    detected_skills = {}

    for skill_key, skill_data in skills.items():
        aliases = skill_data.get("aliases", [])

        display_name = skill_data.get(
            "display_name",
            skill_key
        )

        category = skill_data.get(
            "category",
            "Other"
        )

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
    Return only the display names of detected skills.
    """
    skills = extract_skills(text)

    return sorted(
        skill["name"]
        for skill in skills.values()
    )