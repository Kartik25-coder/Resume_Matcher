# Resume Matcher

A small Streamlit app that compares a resume PDF against a job description, calculates a skill-match score, and highlights matched and missing skills.

## Features

- Upload a resume in PDF format
- Paste a job description
- Extract text from the PDF with `pypdf`
- Calculate two scores:
  - Skill match based on a curated keyword list
  - Overall text similarity using TF-IDF + cosine similarity
- Show matched skills and missing skills side by side

## Project Structure

- `app.py` - Streamlit UI and result rendering
- `extractor.py` - PDF text extraction helper
- `matcher.py` - Match scoring and keyword comparison logic
- `skills_list.py` - Curated list of skills and keywords
- `Kartik_Sawant_Resume.pdf` - Sample resume file included in the workspace

## Requirements

This project uses:

- `streamlit`
- `pypdf`
- `scikit-learn`

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r skills/requirements.txt
   ```

3. Run the app from the project root:

   ```bash
   streamlit run app.py
   ```

## How It Works

1. The user uploads a PDF resume.
2. The app extracts text from the PDF.
3. The job description text is compared against the resume text.
4. A curated skills list is used to identify matched and missing keywords.
5. The app displays the final score and skill breakdown.

## Notes

- The keyword-based score is often more practical for resume screening than raw text similarity.
- If the PDF does not contain selectable text, text extraction may fail or return little content.
