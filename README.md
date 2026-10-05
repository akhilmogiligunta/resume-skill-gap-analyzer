# Resume Skill Gap Analyzer

A machine-learning-based web application that analyzes a candidate's resume against a job description and identifies relevant skill gaps.

## Project Overview

The Resume Skill Gap Analyzer helps users understand how well their technical skills match the requirements of a job description.

The system accepts a resume in PDF/DOCX format or manually entered resume text. It extracts technical skills using a configurable skill dictionary, compares them with the skills identified in the job description, calculates required-skill coverage, and measures textual similarity using TF-IDF and cosine similarity.

The application also provides learning recommendations for missing skills.

## Objectives

- Extract text from PDF and DOCX resumes.
- Identify technical skills from resumes and job descriptions.
- Support skill aliases and different skill representations.
- Compare resume skills with job requirements.
- Calculate required-skill coverage.
- Calculate TF-IDF cosine similarity.
- Identify matched, missing, and additional skills.
- Provide learning recommendations.
- Provide a simple and responsive web interface.
- Handle invalid and unsupported files safely.

## Key Features

### 1. Resume Upload

Users can upload:

- PDF resumes
- DOCX resumes

A maximum upload size of 5 MB is enforced.

### 2. Manual Resume Input

Users can paste resume content directly into the application instead of uploading a file.

### 3. Job Description Input

Users can paste the target job description for comparison.

### 4. Skill Extraction

Technical skills are identified using a configurable dictionary stored in:

```text
config/skills.json