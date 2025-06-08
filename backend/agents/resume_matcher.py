# from agno import Agent
# from agno.agent import Agent  # or another submodule
from ..utils import Agent  # Use our custom implementation
import pdfplumber
import requests
from bs4 import BeautifulSoup
import openai
import os
from typing import Dict, Any

class ResumeMatcher(Agent):
    def __init__(self):
        super().__init__("ResumeMatcher")
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages)
        return text
    
    def scrape_job_description(self, url: str) -> str:
        if "linkedin.com" in url:
            return self._scrape_linkedin_job(url)
        elif "naukri.com" in url:
            return self._scrape_naukri_job(url)
        else:
            raise ValueError("Unsupported job platform")
    
    def _scrape_linkedin_job(self, url: str) -> str:
        # Note: LinkedIn scraping is more complex and might require Selenium
        # This is a simplified version
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.find('div', {'class': 'description__text'})
        return description.get_text() if description else ""
    
    def _scrape_naukri_job(self, url: str) -> str:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.find('div', {'class': 'jd'})
        return description.get_text() if description else ""
    
    def analyze_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze how well this resume matches the job description.
        Provide a score from 0-100 and specific feedback on improvements.
        
        Resume:
        {resume_text[:3000]}... [truncated]
        
        Job Description:
        {job_description[:3000]}... [truncated]
        
        Output format:
        - Match Score: X/100
        - Strengths: [list]
        - Weaknesses: [list]
        - Suggested Improvements: [list]
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a career advisor."},
                     {"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message['content']
    
    def match(self, job_url: str, resume_path: str) -> Dict[str, Any]:
        resume_text = self.extract_text_from_pdf(resume_path)
        job_description = self.scrape_job_description(job_url)
        analysis = self.analyze_match(resume_text, job_description)
        
        return {
            "job_description": job_description,
            "resume_summary": resume_text[:500] + "...",
            "analysis": analysis
        }