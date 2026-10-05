from src.matching import (
    compare_skills,
    calculate_cosine_similarity,
    analyze_match,
)


def test_skill_comparison():
    resume = """
    I know Python, SQL, React and Git.
    """

    job = """
    We need Python, SQL, Docker and AWS.
    """

    result = compare_skills(
        resume,
        job
    )

    assert "Python" in result["matched_skills"]
    assert "SQL" in result["matched_skills"]

    assert "Docker" in result["missing_skills"]
    assert "AWS" in result["missing_skills"]

    assert "React" in result["additional_skills"]
    assert "Git" in result["additional_skills"]

    assert result["matched_required_skills"] == 2
    assert result["total_required_skills"] == 4
    assert result["required_skill_coverage"] == 50.0


def test_cosine_similarity():
    resume = "Python SQL React"
    job = "Python SQL Docker"

    similarity = calculate_cosine_similarity(
        resume,
        job
    )

    assert 0 <= similarity <= 1


def test_empty_similarity():
    result = calculate_cosine_similarity(
        "",
        "Python SQL"
    )

    assert result == 0.0


def test_complete_analysis():
    resume = """
    Python SQL React Git
    """

    job = """
    Python SQL Docker AWS
    """

    result = analyze_match(
        resume,
        job
    )

    assert "matched_skills" in result
    assert "missing_skills" in result
    assert "additional_skills" in result
    assert "required_skill_coverage" in result
    assert "cosine_similarity" in result


def test_skill_categories():
    resume = """
    Python, React, Git
    """

    job = """
    Python, React, Docker, AWS
    """

    result = compare_skills(
        resume,
        job
    )

    assert "Python" in result["matched_by_category"]["Programming"]
    assert "React" in result["matched_by_category"]["Web Development"]

    assert "Docker" in result["missing_by_category"]["DevOps"]
    assert "AWS" in result["missing_by_category"]["Cloud"]

    assert "Git" in result["additional_by_category"]["Tools"]


def test_required_skill_coverage():
    resume = """
    Python, SQL
    """

    job = """
    Python, SQL, Docker, AWS
    """

    result = compare_skills(
        resume,
        job
    )

    assert result["matched_required_skills"] == 2
    assert result["total_required_skills"] == 4
    assert result["required_skill_coverage"] == 50.0


def test_no_required_skills():
    resume = """
    Python, React
    """

    job = """
    We are looking for a motivated developer
    with good communication and teamwork skills.
    """

    result = compare_skills(
        resume,
        job
    )

    assert result["total_required_skills"] == 0
    assert result["matched_required_skills"] == 0
    assert result["required_skill_coverage"] is None


def test_no_known_resume_skills():
    resume = """
    I am a hardworking student with
    good communication and teamwork skills.
    """

    job = """
    Python, SQL and Docker are required.
    """

    result = compare_skills(
        resume,
        job
    )

    assert result["matched_skills"] == []

    assert "Python" in result["missing_skills"]
    assert "SQL" in result["missing_skills"]
    assert "Docker" in result["missing_skills"]

    assert result["matched_required_skills"] == 0
    assert result["total_required_skills"] == 3
    assert result["required_skill_coverage"] == 0.0


def test_no_known_job_skills():
    resume = """
    Python, React and Git.
    """

    job = """
    We are looking for a motivated
    team player with good communication.
    """

    result = compare_skills(
        resume,
        job
    )

    assert result["total_required_skills"] == 0
    assert result["matched_required_skills"] == 0
    assert result["required_skill_coverage"] is None

    assert "Python" in result["additional_skills"]
    assert "React" in result["additional_skills"]
    assert "Git" in result["additional_skills"]


def test_completely_different_skills():
    resume = """
    Python and React.
    """

    job = """
    Java, Docker and AWS.
    """

    result = compare_skills(
        resume,
        job
    )

    assert result["matched_skills"] == []

    assert "Java" in result["missing_skills"]
    assert "Docker" in result["missing_skills"]
    assert "AWS" in result["missing_skills"]

    assert "Python" in result["additional_skills"]
    assert "React" in result["additional_skills"]

    assert result["required_skill_coverage"] == 0.0


def test_skill_alias_matching():
    resume = """
    Experienced with PY, JS, ReactJS,
    K8s and sklearn.
    """

    job = """
    We need Python, JavaScript, React,
    Kubernetes and Scikit-learn.
    """

    result = compare_skills(
        resume,
        job
    )

    assert "Python" in result["matched_skills"]
    assert "JavaScript" in result["matched_skills"]
    assert "React" in result["matched_skills"]
    assert "Kubernetes" in result["matched_skills"]
    assert "Scikit-learn" in result["matched_skills"]

    assert result["required_skill_coverage"] == 100.0


def test_whitespace_inputs():
    result = analyze_match(
        "   ",
        "   "
    )

    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
    assert result["additional_skills"] == []

    assert result["required_skill_coverage"] is None
    assert result["cosine_similarity"] == 0.0