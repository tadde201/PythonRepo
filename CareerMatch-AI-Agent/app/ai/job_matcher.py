from openai import OpenAI

from ai.prompts import JOB_MATCH_PROMPT

client = OpenAI()


def analyze_job(resume: str, job_description: str) -> str:
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
