from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)


def create_pdf_report(results, recommendations):
    """
    Generate a PDF report from resume skill-gap analysis results.

    Returns:
        BytesIO: PDF file stored in memory.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Resume Skill Gap Analysis Report",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
    )

    story = []

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Resume Skill Gap Analyzer",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Resume Skill Gap Analysis Report",
            subtitle_style,
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.lightgrey,
            spaceAfter=15,
        )
    )

    # ---------------------------------------------------------
    # SCORE SUMMARY
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Analysis Summary",
            heading_style,
        )
    )

    coverage = results.get("required_skill_coverage")

    if coverage is None:
        coverage_text = "N/A"
    else:
        coverage_text = f"{coverage:.1f}%"

    similarity = results.get(
        "cosine_similarity_percentage",
        0,
    )

    summary_data = [
        ["Metric", "Result"],
        [
            "Required Skill Coverage",
            coverage_text,
        ],
        [
            "TF-IDF Cosine Similarity",
            f"{similarity:.1f}%",
        ],
        [
            "Required Skills Identified",
            str(results.get("total_required_skills", 0)),
        ],
        [
            "Matched Skills",
            str(results.get("matched_required_skills", 0)),
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[95 * mm, 70 * mm],
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2563eb"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.lightgrey,
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.whitesmoke,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    story.append(summary_table)
    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # MATCHED SKILLS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Matched Skills",
            heading_style,
        )
    )

    matched = results.get("matched_skills", [])

    if matched:
        matched_text = ", ".join(matched)
    else:
        matched_text = "No matching skills were identified."

    story.append(
        Paragraph(
            matched_text,
            normal_style,
        )
    )

    # ---------------------------------------------------------
    # MISSING SKILLS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Missing Skills",
            heading_style,
        )
    )

    missing = results.get("missing_skills", [])

    if missing:
        missing_text = ", ".join(missing)
    else:
        missing_text = "No missing skills were identified."

    story.append(
        Paragraph(
            missing_text,
            normal_style,
        )
    )

    # ---------------------------------------------------------
    # ADDITIONAL SKILLS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Additional Skills",
            heading_style,
        )
    )

    additional = results.get("additional_skills", [])

    if additional:
        additional_text = ", ".join(additional)
    else:
        additional_text = "No additional skills were identified."

    story.append(
        Paragraph(
            additional_text,
            normal_style,
        )
    )

    # ---------------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Learning Recommendations",
            heading_style,
        )
    )

    if recommendations:
        for recommendation in recommendations:
            story.append(
                Paragraph(
                    f"• {recommendation}",
                    normal_style,
                )
            )
            story.append(Spacer(1, 4))
    else:
        story.append(
            Paragraph(
                "No specific recommendations were generated.",
                normal_style,
            )
        )

    # ---------------------------------------------------------
    # INTERPRETATION
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Important Note",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Required Skill Coverage measures the percentage of "
            "identified job-description skills that were also found "
            "in the resume. TF-IDF cosine similarity measures textual "
            "similarity between the resume and job description. "
            "These metrics are separate and should not be interpreted "
            "as a hiring probability or hiring decision.",
            small_style,
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Generated by Resume Skill Gap Analyzer",
            subtitle_style,
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer