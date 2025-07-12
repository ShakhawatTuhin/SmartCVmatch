import requests
import json
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_remoteok():
    """Scrape jobs from RemoteOK"""
    logger.info("Scraping RemoteOK jobs...")
    url = "https://remoteok.com/api"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        # RemoteOK returns CORS headers we don't need
        data = response.json()[1:]  # Skip the first item (CORS notice)
        
        jobs = []
        for job in data:
            try:
                # Process job data
                job_data = {
                    'id': job.get('id', ''),
                    'title': job.get('position', ''),
                    'company': job.get('company', ''),
                    'location': 'Remote',
                    'description': job.get('description', ''),
                    'url': f"https://remoteok.com/remote-jobs/{job.get('slug', '')}",
                    'date_posted': job.get('date'),
                    'source': 'RemoteOK',
                    'skills': job.get('tags', []),
                    'salary': job.get('salary', '')
                }
                jobs.append(job_data)
            except Exception as e:
                logger.error(f"Error processing RemoteOK job: {e}")
                continue
                
        logger.info(f"Scraped {len(jobs)} jobs from RemoteOK")
        return jobs
    except Exception as e:
        logger.error(f"Error scraping RemoteOK: {e}")
        return []

def scrape_github_jobs():
    """Scrape jobs from GitHub Jobs"""
    logger.info("Scraping GitHub Jobs...")
    jobs = []
    
    # GitHub Jobs API is deprecated, but we'll simulate data for the demo
    # In a real implementation, you'd use another job board API
    
    simulated_jobs = [
        {
            'id': 'gh-1001',
            'title': 'Senior Python Developer',
            'company': 'Tech Solutions Inc',
            'location': 'Remote / Worldwide',
            'description': 'Looking for a senior Python developer with 5+ years experience in Django and Flask. Must be familiar with AWS and CI/CD pipelines.',
            'url': 'https://example.com/jobs/1001',
            'date_posted': datetime.now().strftime('%Y-%m-%d'),
            'source': 'GitHub Jobs',
            'skills': ['Python', 'Django', 'Flask', 'AWS'],
            'salary': '$120K - $150K'
        },
        {
            'id': 'gh-1002',
            'title': 'Frontend React Developer',
            'company': 'WebApp Labs',
            'location': 'Remote / US Only',
            'description': 'Seeking a React developer with strong TypeScript skills. Experience with Redux, Next.js, and responsive design required.',
            'url': 'https://example.com/jobs/1002',
            'date_posted': datetime.now().strftime('%Y-%m-%d'),
            'source': 'GitHub Jobs',
            'skills': ['React', 'TypeScript', 'Redux', 'Next.js'],
            'salary': '$90K - $120K'
        }
    ]
    
    jobs.extend(simulated_jobs)
    logger.info(f"Added {len(simulated_jobs)} simulated GitHub Jobs")
    return jobs

def scrape_linkedin_jobs():
    """Simulate scraping jobs from LinkedIn"""
    logger.info("Adding simulated LinkedIn jobs...")
    
    simulated_jobs = [
        {
            'id': 'li-2001',
            'title': 'Machine Learning Engineer',
            'company': 'AI Innovations',
            'location': 'Remote / Europe',
            'description': 'Join our AI team to develop cutting-edge ML solutions. Must have experience with PyTorch or TensorFlow and a strong mathematics background.',
            'url': 'https://example.com/jobs/2001',
            'date_posted': datetime.now().strftime('%Y-%m-%d'),
            'source': 'LinkedIn',
            'skills': ['Python', 'Machine Learning', 'PyTorch', 'TensorFlow', 'Mathematics'],
            'salary': '€80K - €110K'
        },
        {
            'id': 'li-2002',
            'title': 'DevOps Engineer',
            'company': 'Cloud Services Ltd',
            'location': 'Remote / Worldwide',
            'description': 'Experienced DevOps engineer needed to manage our cloud infrastructure. Knowledge of Kubernetes, Docker, and major cloud platforms required.',
            'url': 'https://example.com/jobs/2002',
            'date_posted': datetime.now().strftime('%Y-%m-%d'),
            'source': 'LinkedIn',
            'skills': ['DevOps', 'Kubernetes', 'Docker', 'AWS', 'Azure'],
            'salary': '$100K - $130K'
        },
        {
            'id': 'li-2003',
            'title': 'Full Stack JavaScript Developer',
            'company': 'Digital Solutions',
            'location': 'Remote / US Only',
            'description': 'Looking for a full stack developer with strong Node.js and React skills. Experience with MongoDB and GraphQL is a plus.',
            'url': 'https://example.com/jobs/2003',
            'date_posted': datetime.now().strftime('%Y-%m-%d'),
            'source': 'LinkedIn',
            'skills': ['JavaScript', 'Node.js', 'React', 'MongoDB', 'GraphQL'],
            'salary': '$90K - $115K'
        }
    ]
    
    logger.info(f"Added {len(simulated_jobs)} simulated LinkedIn jobs")
    return simulated_jobs

def scrape_indeed_jobs():
    """Simulate scraping jobs from Indeed"""
    logger.info("Adding simulated Indeed jobs...")
    
    simulated_jobs = [
        {
            'id': 'in-3001',
            'title': 'Data Scientist',
            'company': 'Data Analytics Co',
            'location': 'Remote / Worldwide',
            'description': 'Join our data science team to extract insights from large datasets. PhD or MS in a quantitative field preferred.',
            'url': 'https://example.com/jobs/3001',
            'date_posted': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Indeed',
            'skills': ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics'],
            'salary': '$110K - $140K'
        },
        {
            'id': 'in-3002',
            'title': 'iOS Developer',
            'company': 'Mobile Apps Inc',
            'location': 'Remote / US Only',
            'description': 'Experienced iOS developer needed for consumer-facing mobile application. Swift expertise required, UIKit and SwiftUI experience preferred.',
            'url': 'https://example.com/jobs/3002',
            'date_posted': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Indeed',
            'skills': ['Swift', 'iOS', 'UIKit', 'SwiftUI', 'Xcode'],
            'salary': '$95K - $125K'
        }
    ]
    
    logger.info(f"Added {len(simulated_jobs)} simulated Indeed jobs")
    return simulated_jobs

def main():
    all_jobs = []
    
    # Scrape from multiple sources
    all_jobs.extend(scrape_remoteok())
    all_jobs.extend(scrape_github_jobs())
    all_jobs.extend(scrape_linkedin_jobs())
    all_jobs.extend(scrape_indeed_jobs())
    
    # Write jobs to JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'jobs.json')
    
    logger.info(f"Writing {len(all_jobs)} jobs to {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
    
    logger.info("Job scraping complete")

if __name__ == "__main__":
    main()