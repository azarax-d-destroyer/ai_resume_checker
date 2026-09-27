from typing import Any, Dict, Set

from .parser import extract_skills, parse_resume


def match_resume(resume_text: Any, job_description: Any) -> Dict[str, Any]:
    """Score how well a resume matches a job description."""
    resume_data = parse_resume(resume_text)
    resume_skills = set(resume_data.get("skills", []))
    required_skills = set(extract_skills(job_description))

    if not required_skills:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "resume_skills": sorted(resume_skills),
            "experience_years": resume_data.get("experience_years", 0),
        }

    matched = sorted(required_skills & resume_skills)
    missing = sorted(required_skills - resume_skills)
    match_score = round((len(matched) / len(required_skills)) * 100, 2)

    if resume_data.get("experience_years", 0) and required_skills:
        match_score = min(100.0, match_score + min(15.0, resume_data["experience_years"] * 2))

    return {
        "match_score": match_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skills": sorted(resume_skills),
        "experience_years": resume_data.get("experience_years", 0),
    }


def score_resume(resume_text: Any, job_description: Any) -> float:
    return match_resume(resume_text, job_description)["match_score"]
