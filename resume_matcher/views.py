from django.http import HttpResponse

def home(request):
    return HttpResponse("SmartCVMatch Home Page")

from django.shortcuts import render, redirect
from .forms import ResumeForm
from .models import Resume
import json
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Create your views here.



def home(request):
    jobs = load_jobs()
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            # Only parse if the file is a PDF
            if resume.file and resume.file.name.lower().endswith('.pdf'):
                text = extract_pdf_text(resume.file.path)
                resume.parsed_text = text
                # Extract skills
                skills = extract_skills(text)
                resume.skills = ", ".join(skills)
                resume.save()
            return redirect('home')
    else:
        form = ResumeForm()

    resumes = Resume.objects.all().order_by('-uploaded_at')
    resume_matches = []
    for resume in resumes:
        matches = tfidf_match_jobs(resume.parsed_text, jobs)
        resume_matches.append((resume, matches))
    return render(request, 'home.html', {'form': form, 'resume_matches': resume_matches})


from pdfminer.high_level import extract_text

def extract_pdf_text(file_path):
    try:
        return extract_text(file_path)
    except Exception as e:
        return f"Error extracting text: {e}"
    
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS = [
    "python", "django", "sql", "machine learning", "nlp", "data analysis",
    "pandas", "numpy", "scikit-learn", "deep learning", "flask", "git",
    "docker", "linux", "tensorflow", "keras", "pytorch", "spacy"
]

def extract_skills(text):
    doc = nlp(text.lower())
    found_skills = set()
    for token in doc:
        if token.text in SKILLS:
            found_skills.add(token.text)
    # Also check for multi-word skills
    for skill in SKILLS:
        if skill in text.lower():
            found_skills.add(skill)
    return list(found_skills)

def load_jobs():
    jobs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'jobs.json')
    with open(jobs_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def tfidf_match_jobs(resume_text, jobs, top_n=5):
    if not resume_text:
        return []
    job_texts = [job['description'] for job in jobs]
    job_titles = [job['title'] for job in jobs]
    documents = [resume_text] + job_texts
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    ranked_indices = cosine_sim.argsort()[::-1][:top_n]
    matches = []
    for idx in ranked_indices:
        matches.append({
            'job': jobs[idx],
            'score': round(float(cosine_sim[idx]), 3)
        })
    return matches

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    # Optionally, show user's resumes/bookmarks here in the future
    return render(request, 'registration/profile.html')