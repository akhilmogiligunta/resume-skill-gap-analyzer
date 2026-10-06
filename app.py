from pathlib import Path
import tempfile

from flask import Flask, render_template, request, send_file
from werkzeug.exceptions import RequestEntityTooLarge

from src.matching import analyze_match
from src.recommendations import generate_recommendations
from src.report_generator import create_pdf_report
from src.resume_parser import extract_text, is_supported_file


app = Flask(__name__)

# Maximum uploaded file size: 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return render_template("index.html")

    resume_text = request.form.get(
        "resume_text",
        ""
    ).strip()

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    resume_file = request.files.get("resume_file")

    error = None
    temporary_file = None

    # --------------------------------
    # Validate job description
    # --------------------------------

    if not job_description:
        error = "Please enter a job description."

    # --------------------------------
    # Get resume text
    # --------------------------------

    if not error:

        if resume_file and resume_file.filename:

            if not is_supported_file(resume_file.filename):

                error = (
                    "Unsupported file type. "
                    "Only PDF and DOCX files are supported."
                )

            else:

                try:

                    extension = Path(
                        resume_file.filename
                    ).suffix.lower()

                    temporary_file = tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=extension
                    )

                    temporary_file.close()

                    temporary_path = Path(
                        temporary_file.name
                    )

                    # Save uploaded resume
                    resume_file.save(
                        temporary_path
                    )

                    # Extract text
                    resume_text = extract_text(
                        temporary_path
                    )

                except Exception:

                    error = (
                        "Unable to read the uploaded resume. "
                        "Please check that the file is valid."
                    )

                finally:

                    # Always remove temporary file
                    if temporary_file is not None:

                        try:

                            Path(
                                temporary_file.name
                            ).unlink(
                                missing_ok=True
                            )

                        except Exception:
                            pass

        elif not resume_text:

            error = (
                "Please upload a PDF/DOCX resume "
                "or enter resume text manually."
            )

    # --------------------------------
    # Validate extracted text
    # --------------------------------

    if not error and not resume_text.strip():

        error = (
            "No readable text was found in the resume."
        )

    # --------------------------------
    # Return validation error
    # --------------------------------

    if error:

        return render_template(
            "index.html",
            error=error,
            resume_text=resume_text,
            job_description=job_description
        )

    # --------------------------------
    # Analyze resume
    # --------------------------------

    try:

        results = analyze_match(
            resume_text,
            job_description
        )

        # Keep original text available for PDF generation.
        results["resume_text"] = resume_text
        results["job_description"] = job_description

        recommendations = generate_recommendations(
            results["missing_skills"]
        )

        return render_template(
            "results.html",
            results=results,
            recommendations=recommendations
        )

    except Exception:

        return render_template(
            "index.html",
            error=(
                "An unexpected error occurred "
                "while analyzing the resume."
            ),
            resume_text=resume_text,
            job_description=job_description
        )


# --------------------------------
# File too large
# --------------------------------

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(error):

    return render_template(
        "index.html",
        error=(
            "File too large. "
            "Please upload a resume smaller than 5 MB."
        )
    ), 413


# --------------------------------
# Download PDF Report
# --------------------------------

@app.route("/download-report", methods=["POST"])
def download_report():

    try:

        resume_text = request.form.get(
            "resume_text",
            ""
        ).strip()

        job_description = request.form.get(
            "job_description",
            ""
        ).strip()

        if not resume_text or not job_description:

            return render_template(
                "index.html",
                error=(
                    "Resume text and job description "
                    "are required to generate the report."
                ),
                resume_text=resume_text,
                job_description=job_description
            )

        results = analyze_match(
            resume_text,
            job_description
        )

        recommendations = generate_recommendations(
            results["missing_skills"]
        )

        pdf_file = create_pdf_report(
            results,
            recommendations
        )

        return send_file(
            pdf_file,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="resume_skill_gap_report.pdf"
        )

    except Exception:

        return render_template(
            "index.html",
            error=(
                "Unable to generate the PDF report. "
                "Please try the analysis again."
            )
        )


# --------------------------------
# Run application
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True)