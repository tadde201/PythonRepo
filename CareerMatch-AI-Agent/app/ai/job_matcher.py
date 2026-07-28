"""Job matching logic using OpenAI API or local heuristics."""

from app.config import OPENAI_API_KEY
from typing import Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def analyze_job(resume_text: str, job_description: str) -> str:
    """
    Analyze job match using OpenAI API if available, otherwise use local heuristics.
    
    Args:
        resume_text: Formatted resume/profile text
        job_description: Job title and description
        
    Returns:
        Match analysis text
    """
    if OPENAI_AVAILABLE and OPENAI_API_KEY:
        return _analyze_job_with_openai(resume_text, job_description)
    else:
        return _analyze_job_locally(resume_text, job_description)


def _analyze_job_with_openai(resume_text: str, job_description: str) -> str:
    """
    Use OpenAI API to analyze job match.
    
    Args:
        resume_text: Formatted resume/profile text
        job_description: Job title and description
        
    Returns:
        Match analysis from OpenAI
    """
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = f"""
        Analyze how well the following candidate matches this job posting.
        
        CANDIDATE PROFILE:
        {resume_text}
        
        JOB POSTING:
        {job_description}
        
        Please provide:
        1. Overall match score (0-100%)
        2. Key matching skills
        3. Skill gaps
        4. Brief recommendation (1-2 sentences)
        
        Keep response concise and professional.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a career matching expert. Analyze candidate-to-job fit and provide actionable insights."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error analyzing job with OpenAI: {str(e)}"


def _analyze_job_locally(resume_text: str, job_description: str) -> str:
    """
    Analyze job match using local keyword matching.
    
    Args:
        resume_text: Formatted resume/profile text
        job_description: Job title and description
        
    Returns:
        Match analysis based on skill keywords
    """
    # Extract skills from resume
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    
    # Common technical skills to search for
    tech_skills = [
        "python", "javascript", "java", "c++", "c#", "ruby", "go", "rust",
        "machine learning", "deep learning", "nlp", "natural language processing",
        "data analysis", "data science", "analytics",
        "api", "rest", "graphql", "microservices",
        "sql", "nosql", "mongodb", "postgresql", "mysql", "sql server",
        "docker", "kubernetes", "aws", "azure", "gcp", "cloud",
        "react", "angular", "vue", "nodejs", "django", "flask",
        "git", "ci/cd", "devops", "agile", "scrum",
        "power bi", "dax", "ssis", "etl", "data warehouse",
        "azure data factory", "databricks"
    ]
    
    # Find matching skills
    matched_skills = []
    for skill in tech_skills:
        if skill in resume_lower and skill in job_lower:
            matched_skills.append(skill)
    
    # Calculate match score
    resume_skills = [s for s in tech_skills if s in resume_lower]
    job_skills = [s for s in tech_skills if s in job_lower]
    
    if len(job_skills) > 0:
        match_score = int((len(matched_skills) / len(job_skills)) * 100)
    else:
        match_score = 50
    
    # Build analysis
    analysis = f"Local Match Analysis:\n"
    analysis += f"- Overall Match Score: {match_score}%\n"
    analysis += f"- Skills Found: {', '.join(matched_skills) if matched_skills else 'None detected'}\n"
    analysis += f"- Candidate Skills: {', '.join(resume_skills[:5])}\n"
    analysis += f"- Job Requirements: {', '.join(job_skills[:5])}\n"
    
    if match_score >= 80:
        analysis += f"- Recommendation: Excellent match! Strongly consider applying.\n"
    elif match_score >= 60:
        analysis += f"- Recommendation: Good match. Worth applying if interested.\n"
    elif match_score >= 40:
        analysis += f"- Recommendation: Moderate match. May require additional learning.\n"
    else:
        analysis += f"- Recommendation: Poor match. Consider roles that better align with your skills.\n"
    
    return analysis
