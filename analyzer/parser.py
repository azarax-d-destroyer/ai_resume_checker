import re
from typing import Any, Dict, List, Set


SKILL_ALIASES = {
    "python": "python",
    "py": "python",
    "javascript": "javascript",
    "js": "javascript",
    "typescript": "typescript",
    "ts": "typescript",
    "java": "java",
    "csharp": "c#",
    "c#": "c#",
    "cpp": "c++",
    "c++": "c++",
    "sql": "sql",
    "mysql": "sql",
    "postgres": "sql",
    "postgresql": "sql",
    "flask": "flask",
    "django": "django",
    "fastapi": "fastapi",
    "react": "react",
    "node": "nodejs",
    "node.js": "nodejs",
    "nodejs": "nodejs",
    "aws": "aws",
    "amazon web services": "aws",
    "docker": "docker",
    "kubernetes": "kubernetes",
    "k8s": "kubernetes",
    "terraform": "terraform",
    "azure": "azure",
    "gcp": "gcp",
    "google cloud": "gcp",
    "machine learning": "machine learning",
    "ml": "machine learning",
    "artificial intelligence": "artificial intelligence",
    "ai": "artificial intelligence",
    "data analysis": "data analysis",
    "excel": "excel",
    "powerbi": "power bi",
    "power bi": "power bi",
    "pandas": "pandas",
    "numpy": "numpy",
    "spark": "spark",
    "tableau": "tableau",
    "mongodb": "mongodb",
    "redis": "redis",
}


def normalize_token(value: str) -> str:
    return re.sub(r"[^a-z0-9+#]+", " ", (value or "").lower()).strip()


def _skill_variants(skill: str) -> List[str]:
    clean = normalize_token(skill)
    if not clean:
        return []
    variants = {clean}
    variants.add(clean.replace(" ", ""))
    if clean == "c#":
        variants.add("csharp")
    if clean == "c++":
        variants.add("cpp")
    if clean == "nodejs":
        variants.add("node.js")
    if clean == "power bi":
        variants.add("powerbi")
    return sorted(variants)


def extract_skills(text: Any) -> List[str]:
    """Return a normalized list of detected skills from a resume or job description."""
    if text is None:
        return []
    if isinstance(text, dict):
        text = " ".join(str(value) for value in text.values())
    if not isinstance(text, str):
        text = str(text)

    source = text.lower()
    detected: Set[str] = set()

    for raw_skill, canonical in SKILL_ALIASES.items():
        pattern = re.escape(raw_skill)
        if re.search(rf"(?<![a-z0-9]){pattern}(?![a-z0-9])", source):
            detected.add(canonical)

    for raw_skill in [
        "python",
        "sql",
        "aws",
        "docker",
        "flask",
        "django",
        "react",
        "javascript",
        "typescript",
        "java",
        "go",
        "ruby",
        "rust",
        "kubernetes",
        "terraform",
        "azure",
        "gcp",
        "machine learning",
        "ai",
        "pandas",
        "numpy",
        "spark",
        "tableau",
        "mongodb",
        "postgresql",
        "redis",
        "nodejs",
        "fastapi",
        "excel",
        "power bi",
        "data analysis",
    ]:
        variant_keys = _skill_variants(raw_skill)
        if any(re.search(rf"(?<![a-z0-9]){re.escape(v)}(?![a-z0-9])", source) for v in variant_keys):
            detected.add(SKILL_ALIASES.get(raw_skill, raw_skill))

    if "python" in detected and "developer" in source:
        detected.add("python")

    ordered = []
    for skill in [
        "python",
        "sql",
        "aws",
        "docker",
        "flask",
        "django",
        "fastapi",
        "javascript",
        "typescript",
        "react",
        "nodejs",
        "java",
        "go",
        "kubernetes",
        "terraform",
        "azure",
        "gcp",
        "machine learning",
        "artificial intelligence",
        "pandas",
        "numpy",
        "spark",
        "tableau",
        "mongodb",
        "redis",
        "excel",
        "power bi",
        "data analysis",
        "c#",
        "c++",
    ]:
        if skill in detected:
            ordered.append(skill)
    return ordered


def extract_experience_years(text: Any) -> int:
    if text is None:
        return 0
    if isinstance(text, dict):
        text = " ".join(str(value) for value in text.values())
    if not isinstance(text, str):
        text = str(text)

    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b", text, flags=re.IGNORECASE)
    if match:
        try:
            return int(float(match.group(1)))
        except ValueError:
            return 0
    match = re.search(r"(\d+(?:\.\d+)?)\s*\+\s*(?:years?|yrs?)\b", text, flags=re.IGNORECASE)
    if match:
        try:
            return int(float(match.group(1)))
        except ValueError:
            return 0
    return 0


def parse_resume(text: Any) -> Dict[str, Any]:
    if text is None:
        text = ""
    if isinstance(text, dict):
        resume_text = "\n".join(str(value) for value in text.values())
    else:
        resume_text = str(text)

    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    name = ""
    title = ""

    if lines:
        name = lines[0]
    if len(lines) > 1:
        title = lines[1]

    email = ""
    phone = ""
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text)
    phone_match = re.search(r"(?:\+?\d[\d\s().-]{7,}\d)", resume_text)
    if email_match:
        email = email_match.group(0)
    if phone_match:
        phone = phone_match.group(0)

    skill_list = extract_skills(resume_text)
    experience_years = extract_experience_years(resume_text)

    summary = "\n".join(lines[:3]) if lines else ""
    return {
        "name": name,
        "title": title,
        "email": email,
        "phone": phone,
        "skills": skill_list,
        "experience_years": experience_years,
        "experience_summary": summary,
        "summary": summary,
        "raw_text": resume_text,
    }
