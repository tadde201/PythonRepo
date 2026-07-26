import argparse
import json
from pathlib import Path
from typing import Any

from app.ai.job_matcher import analyze_job
from app.jobs.job_collector import collect_jobs
from app.notifications.email_sender import send_email
from app.config import EMAIL_FROM, EMAIL_TO, OPENAI_API_KEY, SMTP_SERVER

BASE_DIR = Path(__file__).resolve().parent
PROFILE_PATH = BASE_DIR / "data" / "candidate_profile.json"
JOB_SAMPLE_PATH = BASE_DIR / "data" / "sample_jobs.json"
RESULTS_PATH = BASE_DIR / "data" / "job_matches.json"


def load_candidate_profile() -> dict[str, Any]:
    with PROFILE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_jobs(path: Path | str = JOB_SAMPLE_PATH) -> list[dict[str, Any]]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_resume_text(profile: dict[str, Any]) -> str:
    skills = ", ".join(profile.get("skills", []))
    experience = ", ".join(profile.get("experience", []))
    target_roles = ", ".join(profile.get("target_roles", []))

    return (
        f"Name: {profile.get('name')}\n"
        f"Location: {profile.get('location')}\n"
        f"Target roles: {target_roles}\n"
        f"Skills: {skills}\n"
        f"Experience: {experience}\n"
    )


def save_results(results: list[dict[str, Any]], path: Path = RESULTS_PATH) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


def format_job_output(job: dict[str, Any], match_text: str) -> str:
    title = job.get("title", "Unknown title")
    company = job.get("company", "Unknown company")
    return f"\n=== {title} @ {company} ===\n{match_text}\n"


def extract_resume_skills(resume: str) -> list[str]:
    for line in resume.splitlines():
        if line.lower().startswith("skills:"):
            return [skill.strip().lower() for skill in line[len("skills:"):].split(",") if skill.strip()]
    return []


def local_match_analysis(resume: str, job_description: str) -> str:
    candidate_skills = extract_resume_skills(resume)
    job_text = job_description.lower()
    skills_found = [skill for skill in candidate_skills if skill in job_text]
    match_score = int((len(skills_found) / max(1, len(candidate_skills))) * 100)

    return (
        f"Local dry-run result:\n"
        f"- Estimated match: {match_score}%\n"
        f"- Skills found in job description: {', '.join(skills_found) or 'none'}\n"
        f"- Use OPENAI_API_KEY or --dry-run flag to control analysis mode."
    )


def score_job(resume_text: str, job: dict[str, Any], use_openai: bool) -> str:
    job_description = f"{job.get('title', '')} at {job.get('company', '')}\n{job.get('description', '')}"
    if use_openai:
        return analyze_job(resume_text, job_description)
    return local_match_analysis(resume_text, job_description)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CareerMatch AI Agent pipeline")
    parser.add_argument(
        "--jobs",
        default=str(JOB_SAMPLE_PATH),
        help="Path to a JSON file containing job postings",
    )
    parser.add_argument(
        "--url",
        help="Optional job listing URL to collect jobs from a web page",
    )
    parser.add_argument(
        "--output",
        default=str(RESULTS_PATH),
        help="Output path for job match results",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without OpenAI and use local matching heuristics",
    )
    parser.add_argument(
        "--no-email",
        action="store_true",
        help="Skip sending email notifications",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    profile = load_candidate_profile()
    resume_text = build_resume_text(profile)

    if args.url:
        jobs = collect_jobs(args.url)
    else:
        jobs = load_jobs(args.jobs)

    use_openai = bool(OPENAI_API_KEY and not args.dry_run)
    if not use_openai:
        print("WARNING: Running in local dry-run mode because OpenAI API key is missing or --dry-run was requested.")

    results = []
    for job in jobs:
        match_text = score_job(resume_text, job, use_openai=use_openai)
        print(format_job_output(job, match_text))
        results.append({"job": job, "match": match_text})

    save_results(results, Path(args.output))
    print(f"Saved {len(results)} match results to {args.output}")

    if not args.no_email and EMAIL_FROM and EMAIL_TO:
        message_body = "\n".join(
            [format_job_output(result["job"], result["match"]) for result in results]
        )
        email_sent = send_email(
            subject="CareerMatch AI Job Match Results",
            body=message_body,
            to_address=EMAIL_TO,
            from_address=EMAIL_FROM,
            smtp_server=SMTP_SERVER,
        )
        if email_sent:
            print(f"Notification sent to {EMAIL_TO}")
        else:
            print("Notification not sent. See warning above.")
    elif args.no_email:
        print("Email notifications skipped because --no-email was provided.")


if __name__ == "__main__":
    main()
