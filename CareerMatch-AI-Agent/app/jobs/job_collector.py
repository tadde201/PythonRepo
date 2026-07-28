"""Job collection utilities for web scraping and parsing."""

from typing import List, Dict, Any
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def collect_jobs(url: str) -> List[Dict[str, Any]]:
    """
    Collect job postings from a URL.
    
    Args:
        url: URL to scrape job postings from
        
    Returns:
        List of job dictionaries with title, company, description
    """
    try:
        jobs = []
        
        # Fetch the page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find job postings (this is a generic implementation)
        # Different job sites have different structures, so adjust selectors as needed
        job_elements = soup.find_all(['div', 'article'], class_=lambda x: x and ('job' in x.lower() or 'posting' in x.lower()))
        
        if not job_elements:
            # Fallback: look for common job listing patterns
            job_elements = soup.find_all(['div', 'li'], class_=lambda x: x and ('card' in x.lower() or 'item' in x.lower()))
        
        for element in job_elements[:10]:  # Limit to 10 jobs
            job = _extract_job_from_element(element)
            if job and job.get('title'):
                jobs.append(job)
        
        return jobs if jobs else _get_default_jobs()
        
    except Exception as e:
        print(f"Error collecting jobs from {url}: {str(e)}")
        return _get_default_jobs()


def _extract_job_from_element(element) -> Dict[str, Any]:
    """
    Extract job information from an HTML element.
    
    Args:
        element: BeautifulSoup element
        
    Returns:
        Dictionary with job information
    """
    job = {}
    
    # Try to find title
    title_elem = element.find(['h2', 'h3', 'a'], class_=lambda x: x and 'title' in x.lower())
    if title_elem:
        job['title'] = title_elem.get_text(strip=True)
    
    # Try to find company
    company_elem = element.find(['span', 'p'], class_=lambda x: x and 'company' in x.lower())
    if company_elem:
        job['company'] = company_elem.get_text(strip=True)
    
    # Try to find description
    desc_elem = element.find(['p', 'div'], class_=lambda x: x and ('desc' in x.lower() or 'summary' in x.lower()))
    if desc_elem:
        job['description'] = desc_elem.get_text(strip=True)
    
    # Try to find location
    location_elem = element.find(['span', 'p'], class_=lambda x: x and 'location' in x.lower())
    if location_elem:
        job['location'] = location_elem.get_text(strip=True)
    
    return job


def _get_default_jobs() -> List[Dict[str, Any]]:
    """
    Return default job list when scraping fails.
    
    Returns:
        List of default job postings
    """
    return [
        {
            "id": 1,
            "title": "Software Engineer",
            "company": "Tech Company",
            "location": "Remote",
            "description": "Looking for an experienced software engineer with Python skills.",
            "requirements": ["python", "api design", "problem solving"]
        }
    ]


def parse_job_description(description: str) -> Dict[str, Any]:
    """
    Parse a job description to extract key information.
    
    Args:
        description: Raw job description text
        
    Returns:
        Dictionary with parsed job information
    """
    parsed = {
        "raw_description": description,
        "keywords": [],
        "requirements": [],
        "nice_to_have": []
    }
    
    description_lower = description.lower()
    
    # Extract keywords
    common_keywords = [
        "python", "javascript", "java", "machine learning", "api",
        "docker", "kubernetes", "aws", "cloud", "sql", "agile"
    ]
    
    for keyword in common_keywords:
        if keyword in description_lower:
            parsed["keywords"].append(keyword)
    
    # Try to identify required vs nice-to-have
    lines = description.split('\n')
    for line in lines:
        line_lower = line.lower()
        if 'require' in line_lower or 'must have' in line_lower:
            parsed["requirements"].append(line.strip())
        elif 'prefer' in line_lower or 'nice to have' in line_lower:
            parsed["nice_to_have"].append(line.strip())
    
    return parsed
