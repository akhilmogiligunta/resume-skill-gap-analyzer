from src.skill_extraction import (
    extract_skills,
    get_skill_names,
)


def test_extract_basic_skills():
    text = """
    I have experience with Python,
    SQL, React and Docker.
    """

    skills = get_skill_names(text)

    assert "Python" in skills
    assert "SQL" in skills
    assert "React" in skills
    assert "Docker" in skills


def test_extract_aliases():
    text = """
    Experienced in PY, JS, ReactJS,
    K8s and sklearn.
    """

    skills = get_skill_names(text)

    assert "Python" in skills
    assert "JavaScript" in skills
    assert "React" in skills
    assert "Kubernetes" in skills
    assert "Scikit-learn" in skills


def test_empty_text():
    result = extract_skills("")

    assert result == {}


def test_no_known_skills():
    text = """
    I am a hardworking student
    who enjoys teamwork.
    """

    result = extract_skills(text)

    assert result == {}


def test_all_skills_have_display_names():
    from src.skill_extraction import load_skills

    skills = load_skills()

    assert len(skills) > 0

    for skill_key, skill_data in skills.items():

        assert "display_name" in skill_data
        assert skill_data["display_name"].strip() != ""

        assert "aliases" in skill_data
        assert len(skill_data["aliases"]) > 0

        assert "category" in skill_data
        assert skill_data["category"].strip() != ""