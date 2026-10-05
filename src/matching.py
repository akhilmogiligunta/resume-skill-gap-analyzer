from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.preprocessing import preprocess_text
from src.skill_extraction import extract_skills


def compare_skills(resume_text, job_description):
    """
    Compare skills found in the resume and job description.

    Returns matched, missing, and additional skills,
    together with category information and required-skill coverage.
    """

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    resume_skill_keys = set(resume_skills.keys())
    job_skill_keys = set(job_skills.keys())

    matched_keys = resume_skill_keys.intersection(
        job_skill_keys
    )

    missing_keys = job_skill_keys.difference(
        resume_skill_keys
    )

    additional_keys = resume_skill_keys.difference(
        job_skill_keys
    )

    matched_skills = sorted(
        resume_skills[key]["name"]
        for key in matched_keys
    )

    missing_skills = sorted(
        job_skills[key]["name"]
        for key in missing_keys
    )

    additional_skills = sorted(
        resume_skills[key]["name"]
        for key in additional_keys
    )

    # -----------------------------------------
    # Category information
    # -----------------------------------------

    matched_by_category = {}
    missing_by_category = {}
    additional_by_category = {}

    for key in matched_keys:

        category = resume_skills[key]["category"]
        skill_name = resume_skills[key]["name"]

        matched_by_category.setdefault(
            category,
            []
        ).append(skill_name)

    for key in missing_keys:

        category = job_skills[key]["category"]
        skill_name = job_skills[key]["name"]

        missing_by_category.setdefault(
            category,
            []
        ).append(skill_name)

    for key in additional_keys:

        category = resume_skills[key]["category"]
        skill_name = resume_skills[key]["name"]

        additional_by_category.setdefault(
            category,
            []
        ).append(skill_name)

    # Sort skills inside each category
    for category in matched_by_category:
        matched_by_category[category].sort()

    for category in missing_by_category:
        missing_by_category[category].sort()

    for category in additional_by_category:
        additional_by_category[category].sort()

    # -----------------------------------------
    # Required skill coverage
    # -----------------------------------------

    total_required_skills = len(job_skill_keys)
    matched_required_skills = len(matched_keys)

    if total_required_skills == 0:

        required_skill_coverage = None

    else:

        required_skill_coverage = (
            matched_required_skills
            / total_required_skills
        ) * 100

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,

        "matched_by_category": matched_by_category,
        "missing_by_category": missing_by_category,
        "additional_by_category": additional_by_category,

        "matched_required_skills": matched_required_skills,
        "total_required_skills": total_required_skills,
        "required_skill_coverage": required_skill_coverage
    }


def calculate_cosine_similarity(
    resume_text,
    job_description
):
    """
    Calculate TF-IDF cosine similarity between
    the resume and job description.

    Returns a value between 0 and 1.
    """

    resume_text = preprocess_text(resume_text)
    job_description = preprocess_text(job_description)

    if not resume_text or not job_description:
        return 0.0

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer()

    try:

        tfidf_matrix = vectorizer.fit_transform(
            documents
        )

    except ValueError:

        return 0.0

    similarity_matrix = cosine_similarity(
        tfidf_matrix
    )

    similarity = similarity_matrix[0][1]

    return float(similarity)


def analyze_match(
    resume_text,
    job_description
):
    """
    Perform the complete resume/job analysis.
    """

    skill_results = compare_skills(
        resume_text,
        job_description
    )

    similarity = calculate_cosine_similarity(
        resume_text,
        job_description
    )

    skill_results["cosine_similarity"] = similarity

    skill_results["cosine_similarity_percentage"] = (
        similarity * 100
    )

    return skill_results