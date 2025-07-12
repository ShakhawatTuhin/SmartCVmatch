<script lang="ts">
  import type { Resume, Job, JobMatch } from '../types/models';
  import { getResumes, getJobMatches } from '../services/api';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  let resumes = $state<Resume[]>([]);
  let selectedResume = $state<Resume | null>(null);
  let jobMatches = $state<JobMatch[]>([]);
  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let searchQuery = $state('');
  let locationFilter = $state('');

  // Load resumes on mount
  $effect(() => {
    loadResumes();
  });

  async function loadResumes() {
    try {
      isLoading = true;
      error = null;
      resumes = await getResumes();
      if (resumes.length > 0) {
        selectedResume = resumes[0] || null;
        if (selectedResume) {
          await loadJobMatches(selectedResume.id);
        }
      }
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load resumes';
    } finally {
      isLoading = false;
    }
  }

  async function loadJobMatches(resumeId: number) {
    try {
      isLoading = true;
      error = null;
      jobMatches = await getJobMatches(resumeId);
      console.log('Job matches loaded:', jobMatches);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load job matches';
    } finally {
      isLoading = false;
    }
  }

  function handleResumeSelect(resume: Resume) {
    selectedResume = resume;
    loadJobMatches(resume.id);
  }

  // Function to generate the correct job URL based on source
  function getJobUrl(job: Job): string {
    if (!job || !job.url) return '#';
    
    // If it's a RemoteOK job, use the provided URL
    if (job.source === 'RemoteOK') {
      return job.url;
    }
    
    // For LinkedIn, create a search URL with the job title and company
    if (job.source === 'LinkedIn') {
      const searchQuery = encodeURIComponent(`${job.title} ${job.company}`);
      return `https://www.linkedin.com/jobs/search/?keywords=${searchQuery}`;
    }
    
    // For Indeed, create a search URL with the job title and company
    if (job.source === 'Indeed') {
      const searchQuery = encodeURIComponent(`${job.title} ${job.company}`);
      return `https://www.indeed.com/jobs?q=${searchQuery}`;
    }
    
    // For any other source or if missing info, return the original URL or a fallback
    return job.url;
  }

  let filteredJobs = $derived(jobMatches.filter(jobMatch => {
    const job = jobMatch.job;
    
    if (!job) return false;
    
    const matchesSearch = !searchQuery || 
      job.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.company?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.description?.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesLocation = !locationFilter ||
      job.location?.toLowerCase().includes(locationFilter.toLowerCase());

    return matchesSearch && matchesLocation;
  }));
</script>

<div class="job-finder">
  <div class="sidebar">
    <h2>Your Resumes</h2>
    {#if resumes.length > 0}
      <div class="resume-list">
        {#each resumes as resume}
          <button 
            class="resume-item"
            class:active={selectedResume?.id === resume.id}
            onclick={() => handleResumeSelect(resume)}
          >
            <div class="resume-name">{resume.name}</div>
            <div class="resume-date">
              Uploaded {new Date(resume.uploadedAt).toLocaleDateString()}
            </div>
            <div class="resume-skills">
              {resume.skills.split(',').slice(0, 3).join(', ')}
              {#if resume.skills.split(',').length > 3}
                <span>+{resume.skills.split(',').length - 3} more</span>
              {/if}
            </div>
          </button>
        {/each}
      </div>
    {:else}
      <div class="empty-state">
        <p>No resumes uploaded yet.</p>
        <button 
          class="upload-btn"
          onclick={() => dispatch('navigate', { page: 'home' })}
        >
          Upload Resume
        </button>
      </div>
    {/if}
  </div>

  <div class="main-content">
    <div class="search-bar">
      <div class="search-input">
        <i class="fas fa-search"></i>
        <input 
          type="text"
          placeholder="Search jobs by title, company, or keywords"
          bind:value={searchQuery}
        />
      </div>
      <div class="search-input">
        <i class="fas fa-map-marker-alt"></i>
        <input 
          type="text"
          placeholder="Filter by location"
          bind:value={locationFilter}
        />
      </div>
    </div>

    {#if isLoading}
      <div class="loading">
        <i class="fas fa-spinner fa-spin"></i>
        Loading...
      </div>
    {:else if error}
      <div class="error">
        <i class="fas fa-exclamation-circle"></i>
        {error}
      </div>
    {:else if filteredJobs.length > 0}
      <div class="job-list">
        {#each filteredJobs as jobMatch}
          <div class="job-card">
            <div class="job-header">
              <h3>{jobMatch.job?.title || 'Untitled Job'}</h3>
              <div class="match-score">
                {Math.round(jobMatch.tfidf_score * 100)}% Match
              </div>
            </div>
            <div class="job-company">
              <i class="fas fa-building"></i>
              {jobMatch.job?.company || 'Unknown Company'}
            </div>
            <div class="job-location">
              <i class="fas fa-map-marker-alt"></i>
              {jobMatch.job?.location || 'Remote'}
            </div>
            <div class="job-source">
              <i class="fas fa-globe"></i>
              Source: {jobMatch.job?.source || 'Unknown'}
            </div>
            <p class="job-description">
              {jobMatch.job?.description?.substring(0, 200) || 'No description available'}
              {jobMatch.job?.description?.length > 200 ? '...' : ''}
            </p>
            <div class="job-skills">
              <h4>Skills:</h4>
              {#if jobMatch.matched_skills && jobMatch.matched_skills.length > 0}
                <div class="matched-skills">
                  <span class="skill-label">Matched Skills:</span>
                  {#each jobMatch.matched_skills as skill}
                    <span class="skill-tag matched">{skill}</span>
                  {/each}
                </div>
              {/if}
              {#if jobMatch.job?.skills && jobMatch.job.skills.length > 0}
                {#each jobMatch.job.skills.slice(0, 5) as skill}
                  <span class="skill-tag">{skill}</span>
                {/each}
                {#if jobMatch.job.skills.length > 5}
                  <span class="more-skills">+{jobMatch.job.skills.length - 5} more</span>
                {/if}
              {/if}
            </div>
            <div class="job-actions">
              <a 
                href={getJobUrl(jobMatch.job)} 
                target="_blank" 
                rel="noopener noreferrer"
                class="apply-btn"
              >
                Apply Now
              </a>
              <button class="bookmark-btn">
                <i class="far fa-bookmark"></i>
                Save
              </button>
            </div>
          </div>
        {/each}
      </div>
    {:else}
      <div class="empty-state">
        <p>No matching jobs found.</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .job-finder {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
  }

  .sidebar {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  h2 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 1rem;
  }

  .resume-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .resume-item {
    background: none;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 1rem;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s;
  }

  .resume-item:hover {
    border-color: #dc2626;
  }

  .resume-item.active {
    border-color: #dc2626;
    background: #fef2f2;
  }

  .resume-name {
    font-weight: 500;
    color: #111827;
    margin-bottom: 0.25rem;
  }

  .resume-date {
    font-size: 0.875rem;
    color: #6b7280;
    margin-bottom: 0.5rem;
  }

  .resume-skills {
    font-size: 0.875rem;
    color: #4b5563;
  }

  .main-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .search-bar {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 1rem;
  }

  .search-input {
    position: relative;
  }

  .search-input i {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #6b7280;
  }

  .search-input input {
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 2.5rem;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    font-size: 1rem;
  }

  .search-input input:focus {
    outline: none;
    border-color: #dc2626;
  }

  .job-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .job-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .job-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
  }

  .job-header h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
  }

  .match-score {
    background: #dcfce7;
    color: #15803d;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
  }

  .job-company, .job-location {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #6b7280;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
  }

  .job-description {
    color: #4b5563;
    margin: 1rem 0;
    line-height: 1.5;
  }

  .job-skills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .skill-tag {
    background: #f3f4f6;
    color: #374151;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
  }

  .job-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }

  .apply-btn {
    flex: 1;
    background: #dc2626;
    color: white;
    padding: 0.75rem;
    border-radius: 6px;
    text-align: center;
    text-decoration: none;
    font-weight: 500;
    transition: background-color 0.2s;
  }

  .apply-btn:hover {
    background: #b91c1c;
  }

  .bookmark-btn {
    background: none;
    border: 1px solid #e5e7eb;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    color: #6b7280;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
  }

  .bookmark-btn:hover {
    border-color: #dc2626;
    color: #dc2626;
  }

  .loading, .error, .empty-state {
    text-align: center;
    padding: 2rem;
    color: #6b7280;
  }

  .loading i, .error i {
    margin-right: 0.5rem;
  }

  .error {
    color: #ef4444;
  }

  .upload-btn {
    background: #dc2626;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    border: none;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
    margin-top: 1rem;
  }

  .upload-btn:hover {
    background: #b91c1c;
  }

  @media (max-width: 1024px) {
    .job-finder {
      grid-template-columns: 1fr;
    }

    .search-bar {
      grid-template-columns: 1fr;
    }
  }
</style> 