from analyzer.parser import parse_resume
from analyzer.matcher import match_resume


def test_parse_resume_extracts_key_fields():
    resume_text = """
    Jane Doe
    Senior Python Developer
    Skills: Python, SQL, Flask, Docker, AWS
    Experience: 5 years building scalable backend systems.
    """

    parsed = parse_resume(resume_text)

    assert parsed["name"] == "Jane Doe"
    assert parsed["title"] == "Senior Python Developer"
    assert "python" in parsed["skills"]
    assert "sql" in parsed["skills"]
    assert "flask" in parsed["skills"]
    assert "docker" in parsed["skills"]
    assert "aws" in parsed["skills"]
    assert parsed["experience_years"] >= 5


def test_match_resume_scores_required_skills():
    resume_text = """
    Jane Doe
    Senior Python Developer
    Skills: Python, SQL, Flask, Docker, AWS
    """
    job_description = """
    We are hiring a backend engineer with Python, SQL, and AWS experience.
    Experience with Docker preferred.
    """

    result = match_resume(resume_text, job_description)

    assert result["match_score"] >= 70
    assert "python" in result["matched_skills"]
    assert "sql" in result["matched_skills"]
    assert "aws" in result["matched_skills"]
    assert result["missing_skills"] == [] or "docker" in result["missing_skills"]
