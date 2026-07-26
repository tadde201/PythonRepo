# CareerMatch AI Agent

Version 1 of the CareerMatch AI Agent.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python app/main.py --dry-run
```

Use `--dry-run` when `OPENAI_API_KEY` is not configured.

```bash
python app/main.py --dry-run --no-email
```

Use `--no-email` to skip email delivery during local tests.

```bash
python app/main.py --dry-run --no-email
```

Use `--no-email` to skip email delivery during local tests.

## Project structure

- `app/main.py` - entry point and pipeline orchestration
- `app/config.py` - settings and environment configuration
- `app/data` - candidate profile, sample jobs, and match results
- `app/database` - SQL Server connection and schema
- `app/ai` - AI matching logic and prompts
- `app/jobs` - job collection and parsing utilities
- `app/notifications` - email delivery helpers

## Notes
- `app/main.py` loads `app/data/candidate_profile.json` and `app/data/sample_jobs.json`.
- Results are saved to `app/data/job_matches.json`.
- Email notification works when `EMAIL_FROM`, `EMAIL_TO`, and `SMTP_SERVER` are configured in `.env`.
- This folder is not yet a git repository. Initialize git locally and add a remote before pushing:

```bash
git init
git add .
git commit -m "Initial CareerMatch AI Agent"
git remote add origin <your-remote-url>
git push -u origin main
```
