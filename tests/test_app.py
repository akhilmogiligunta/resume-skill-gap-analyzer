import io

import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200


def test_empty_submission(client):
    response = client.post(
        "/",
        data={
            "resume_text": "",
            "job_description": ""
        }
    )

    assert response.status_code == 200

    assert (
        b"Please enter a job description."
        in response.data
    )


def test_missing_resume(client):
    response = client.post(
        "/",
        data={
            "resume_text": "",
            "job_description": "We need Python developers."
        }
    )

    assert response.status_code == 200

    assert (
        b"Please upload a PDF/DOCX resume"
        in response.data
    )


def test_manual_resume_analysis(client):
    response = client.post(
        "/",
        data={
            "resume_text": """
                Python, SQL, React and Git
            """,
            "job_description": """
                We need Python, SQL and Docker.
            """
        }
    )

    assert response.status_code == 200

    assert b"Required Skill Coverage" in response.data
    assert b"Python" in response.data
    assert b"Docker" in response.data


def test_unsupported_file(client):
    data = {
        "resume_file": (
            io.BytesIO(b"fake executable content"),
            "resume.exe"
        ),
        "job_description": "Python developer"
    }

    response = client.post(
        "/",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200

    assert (
        b"Unsupported file type"
        in response.data
    )


def test_file_size_limit(client):
    large_file = b"x" * (
        5 * 1024 * 1024 + 1
    )

    data = {
        "resume_file": (
            io.BytesIO(large_file),
            "large_resume.pdf"
        ),
        "job_description": "Python developer"
    }

    response = client.post(
        "/",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 413


def test_corrupted_pdf(client):
    data = {
        "resume_file": (
            io.BytesIO(
                b"This is not a real PDF file."
            ),
            "resume.pdf"
        ),
        "job_description": "Python developer"
    }

    response = client.post(
        "/",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200

    assert (
        b"Unable to read the uploaded resume"
        in response.data
    )


def test_corrupted_docx(client):
    data = {
        "resume_file": (
            io.BytesIO(
                b"This is not a real DOCX file."
            ),
            "resume.docx"
        ),
        "job_description": "Python developer"
    }

    response = client.post(
        "/",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200

    assert (
        b"Unable to read the uploaded resume"
        in response.data
    )