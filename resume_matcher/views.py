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
from django.contrib.auth import login, logout
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Bookmark


# Create your views here.



def home(request):
    jobs = load_jobs()
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            if request.user.is_authenticated:
                resume.user = request.user
            resume.save()  # Save first, so file is written to disk and path is valid
            # Only parse if the file is a PDF
            if resume.file and resume.file.name.lower().endswith('.pdf'):
                text = extract_pdf_text(resume.file.path)
                resume.parsed_text = text
                # Extract skills
                skills = extract_skills(text)
                resume.skills = ", ".join(skills)
                resume.save()  # Save again to update parsed_text and skills
            return redirect('home')
    else:
        form = ResumeForm()

    if request.user.is_authenticated:
        resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    else:
        resumes = Resume.objects.none()  # or [] for an empty queryset

    resume_matches = []
    for resume in resumes:
        matches = combined_match_jobs(resume, jobs)
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

# Clean job descriptions to remove boilerplate
import re

def clean_description(text):
    # Remove lines with 'Apply now', 'Share this job', 'rok.co short link'
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if any(phrase in line for phrase in [
            'Apply now', 'Share this job', 'rok.co short link', '👀', '✅', 'applied (', 'views'
        ]):
            continue
        cleaned_lines.append(line)
    cleaned = ' '.join(cleaned_lines)
    # Optionally, remove everything before 'is hiring' or 'at [Company]'
    match = re.search(r'(is hiring|at [A-Za-z0-9 ]+)', cleaned)
    if match:
        cleaned = cleaned[match.start():]
    # Remove excessive whitespace
    cleaned = re.sub(r'\\s+', ' ', cleaned)
    return cleaned.strip()

# TF-IDF matching using cleaned descriptions
def tfidf_match_jobs(resume_text, jobs, top_n=5):
    if not resume_text:
        return []
    job_texts = [clean_description(job['description']) for job in jobs]
    documents = [resume_text] + job_texts
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    ranked_indices = cosine_sim.argsort()[::-1][:top_n]
    matches = []
    for idx in ranked_indices:
            matches.append({
            'job': jobs[idx],
            'tfidf_score': round(float(cosine_sim[idx]), 3)
            })
    return matches

# Skill-overlap matching (as before)
def skill_match_score(resume_skills, job_skills):
    resume_skills_set = set([skill.strip().lower() for skill in resume_skills.split(',')]) if resume_skills else set()
    job_skills_set = set([skill.lower() for skill in job_skills])
    overlap = resume_skills_set & job_skills_set
    return len(overlap), list(overlap)

# Combine both matching methods
def combined_match_jobs(resume, jobs, top_n=5):
    resume_text = resume.parsed_text or ''
    resume_skills = resume.skills or ''
    # Combine cleaned description and skills for each job
    job_texts = [
        clean_description(job['description']) + ' ' + ' '.join(job.get('skills', []))
        for job in jobs
    ]
    documents = [resume_text] + job_texts
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    results = []
    for idx, job in enumerate(jobs):
        tfidf_score = float(cosine_sim[idx])
        skill_score, matched_skills = skill_match_score(resume_skills, job.get('skills', []))
        results.append({
            'job': job,
            'tfidf_score': round(tfidf_score, 3),
            'skill_score': skill_score,
            'matched_skills': matched_skills
        })
    # Sort by tfidf_score, then skill_score
    results.sort(key=lambda x: (x['tfidf_score'], x['skill_score']), reverse=True)
    return results[:top_n]

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
    user_resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    user_bookmarks = Bookmark.objects.filter(user=request.user).order_by('-created_at')
    stats = {
        'resume_count': user_resumes.count(),
        'bookmark_count': user_bookmarks.count(),
    }
    top_bookmarks = user_bookmarks[:3]
    return render(request, 'registration/profile.html', {
        'user': request.user,
        'user_resumes': user_resumes,
        'stats': stats,
        'top_bookmarks': top_bookmarks,
    })

@login_required
def dashboard(request):
    jobs = load_jobs()
    user_resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    resume_matches = []
    for resume in user_resumes:
        matches = combined_match_jobs(resume, jobs)
        resume_matches.append((resume, matches))
    # Prepare set of bookmarked job_ids for this user
    bookmarked_job_ids = set(
        Bookmark.objects.filter(user=request.user).values_list('job_id', flat=True)
    )
    return render(request, 'dashboard.html', {
        'resume_matches': resume_matches,
        'bookmarked_job_ids': bookmarked_job_ids,
    })

@login_required
@require_POST
def bookmark_job(request):
    job_id = request.POST.get('job_id')
    job_title = request.POST.get('job_title')
    job_company = request.POST.get('job_company')
    job_description = request.POST.get('job_description', '')
    # Avoid duplicate bookmarks
    if not Bookmark.objects.filter(user=request.user, job_id=job_id).exists():
        Bookmark.objects.create(
            user=request.user,
            job_id=job_id,
            job_title=job_title,
            job_company=job_company,
            job_description=job_description
        )
    return redirect('dashboard')

@login_required
@require_POST
def unbookmark_job(request):
    job_id = request.POST.get('job_id')
    bookmark = Bookmark.objects.filter(user=request.user, job_id=job_id).first()
    if bookmark:
        bookmark.delete()
    return redirect('dashboard')

@login_required
def bookmarks(request):
    user_bookmarks = Bookmark.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookmarks.html', {
        'user_bookmarks': user_bookmarks,
    })

@require_POST
@login_required
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')