from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

from docx import Document
from pypdf import PdfReader


ALLOWED_EXTENSIONS = {".pdf", ".docx"}

WORD_NAMESPACE = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
}


def get_file_extension(filename):
    """
    Return the lowercase file extension.
    """
    return Path(filename).suffix.lower()


def is_supported_file(filename):
    """
    Check whether the uploaded file is PDF or DOCX.
    """
    return get_file_extension(filename) in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    reader = PdfReader(file_path)

    pages_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages_text.append(text)

    return "\n".join(pages_text).strip()


def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX file.

    Text is extracted directly from the DOCX XML so that
    text inside normal paragraphs as well as Word text boxes
    and drawing elements can be detected.
    """

    text_parts = []

    with zipfile.ZipFile(file_path, "r") as archive:

        xml_files = [
            name
            for name in archive.namelist()
            if (
                name == "word/document.xml"
                or name.startswith("word/header")
                and name.endswith(".xml")
                or name.startswith("word/footer")
                and name.endswith(".xml")
            )
        ]

        for xml_file in xml_files:

            xml_content = archive.read(xml_file)

            root = ET.fromstring(xml_content)

            for text_node in root.findall(
                ".//w:t",
                WORD_NAMESPACE
            ):

                if text_node.text:
                    text_parts.append(
                        text_node.text
                    )

    return " ".join(text_parts).strip()


def extract_text(file_path):
    """
    Extract text from a supported PDF or DOCX file.
    """

    extension = get_file_extension(file_path)

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError(
        "Unsupported file type. Only PDF and DOCX files are supported."
    )