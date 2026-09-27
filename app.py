#!/usr/bin/env python3
"""Simple CLI for resume analysis."""

import argparse
from pathlib import Path
import sys

from analyzer.matcher import match_resume
from analyzer.parser import parse_resume


def _read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a resume against a job description.")
    parser.add_argument("resume", help="Path to the resume file or '-' to read from stdin.")
    parser.add_argument("job", help="Path to the job description file or '-' to read from stdin.")
    args = parser.parse_args()

    resume_text = _read_text(args.resume)
    job_text = _read_text(args.job)

    parsed = parse_resume(resume_text)
    result = match_resume(resume_text, job_text)

    print(f"Name: {parsed.get('name') or 'Unknown'}")
    print(f"Title: {parsed.get('title') or 'Unknown'}")
    print(f"Skills: {', '.join(parsed.get('skills', [])) or 'None'}")
    print(f"Experience years: {parsed.get('experience_years', 0)}")
    print(f"Match score: {result['match_score']:.2f}%")
    print(f"Matched skills: {', '.join(result['matched_skills']) or 'None'}")
    print(f"Missing skills: {', '.join(result['missing_skills']) or 'None'}")


if __name__ == "__main__":
    main()
