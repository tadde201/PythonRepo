import os

from openai import OpenAI

from app.ai.prompts import JOB_MATCH_PROMPT


def analyze_job(resume: str, job_description: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY must be set to use OpenAI analysis.")

    client = OpenAI(api_key=api_key)
    prompt = JOB_MATCH_PROMPT.format(
        resume=resume,
        job_description=job_description,
    )

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert technical recruiter."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    return response.choices[0].message.content.strip()
