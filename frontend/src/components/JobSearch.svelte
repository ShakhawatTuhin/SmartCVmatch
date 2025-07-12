<script lang="ts">
  import type { Job } from '../types/models';
  import { getJobs, addBookmark, removeBookmark } from '../services/api';

  let jobs = $state<Job[]>([]);
  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let searchQuery = $state('');
  let locationFilter = $state('');
  let jobTypeFilter = $state('All');

  const jobTypes = [
    'All',
    'Full-time',
    'Part-time',
    'Contract',
    'Remote',
    'Internship'
  ];

  // Load jobs on mount and when search query changes
  $effect(() => {
    if (searchQuery.length >= 2) {
      loadJobs();
    }
  });

  async function loadJobs() {
    try {
      isLoading = true;
      error = null;
      jobs = await getJobs(searchQuery);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load jobs';
    } finally {
      isLoading = false;
    }
  }

  async function handleBookmarkToggle(job: Job) {
    try {
      if (job.is_bookmarked) {
        await removeBookmark(job.id);
      } else {
        await addBookmark(job.id);
      }
      job.is_bookmarked = !job.is_bookmarked;
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to update bookmark';
    }
  }

  let filteredJobs = $derived(jobs.filter(job => {
    const matchesLocation = !locationFilter || 
      job.location.toLowerCase().includes(locationFilter.toLowerCase());
    
    const matchesType = jobTypeFilter === 'All' || 
      job.title.toLowerCase().includes(jobTypeFilter.toLowerCase());

    return matchesLocation && matchesType;
  }));
</script>

<div class="job-search">
  <div class="search-section">
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

    <div class="filters">
      {#each jobTypes as type}
        <button 
          class="filter-btn"
          class:active={jobTypeFilter === type}
          onclick={() => jobTypeFilter = type}
        >
          {type}
        </button>
      {/each}
    </div>
  </div>

  {#if isLoading}
    <div class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      Loading jobs...
    </div>
  {:else if error}
    <div class="error">
      <i class="fas fa-exclamation-circle"></i>
      {error}
    </div>
  {:else if filteredJobs.length > 0}
    <div class="jobs-grid">
      {#each filteredJobs as job}
        <div class="job-card">
          <div class="job-header">
            <div class="job-title">
              <h3>{job.title}</h3>
              <span class="company">{job.company}</span>
            </div>
            <button 
              class="bookmark-btn"
              class:active={job.is_bookmarked}
              onclick={() => handleBookmarkToggle(job)}
            >
              <i class="fas fa-bookmark"></i>
            </button>
          </div>

          <div class="job-details">
            <div class="detail-item">
              <i class="fas fa-map-marker-alt"></i>
              {job.location}
            </div>
            <div class="detail-item">
              <i class="fas fa-percentage"></i>
              {job.match_score}% Match
            </div>
          </div>

          <p class="job-description">{job.description}</p>

          <div class="job-skills">
            {#each job.required_skills as skill}
              <span class="skill-tag">{skill}</span>
            {/each}
          </div>

          <div class="job-actions">
            <a 
              href={job.apply_url} 
              target="_blank" 
              rel="noopener noreferrer"
              class="apply-btn"
            >
              Apply Now
            </a>
            <button class="share-btn">
              <i class="fas fa-share-alt"></i>
              Share
            </button>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <div class="empty-state">
      <i class="fas fa-search"></i>
      <h2>No jobs found</h2>
      <p>Try adjusting your search terms or filters</p>
    </div>
  {/if}
</div>

<style>
  .job-search {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .search-section {
    margin-bottom: 2rem;
  }

  .search-bar {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 1rem;
    margin-bottom: 1rem;
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

  .filters {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .filter-btn {
    padding: 0.5rem 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 9999px;
    background: white;
    color: #6b7280;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s;
  }

  .filter-btn:hover {
    border-color: #dc2626;
    color: #dc2626;
  }

  .filter-btn.active {
    background: #dc2626;
    color: white;
    border-color: #dc2626;
  }

  .jobs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
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

  .job-title h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.25rem;
  }

  .company {
    color: #6b7280;
    font-size: 0.95rem;
  }

  .bookmark-btn {
    background: none;
    border: none;
    color: #6b7280;
    cursor: pointer;
    padding: 0.5rem;
    transition: color 0.2s;
  }

  .bookmark-btn:hover {
    color: #dc2626;
  }

  .bookmark-btn.active {
    color: #dc2626;
  }

  .job-details {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .detail-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #6b7280;
    font-size: 0.95rem;
  }

  .job-description {
    color: #4b5563;
    margin-bottom: 1rem;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
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

  .share-btn {
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

  .share-btn:hover {
    border-color: #dc2626;
    color: #dc2626;
  }

  .loading, .error, .empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #6b7280;
  }

  .loading i, .error i {
    margin-right: 0.5rem;
  }

  .error {
    color: #ef4444;
  }

  .empty-state i {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .empty-state h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.5rem;
  }

  .empty-state p {
    margin-bottom: 1.5rem;
  }

  @media (max-width: 768px) {
    .search-bar {
      grid-template-columns: 1fr;
    }

    .jobs-grid {
      grid-template-columns: 1fr;
    }
  }
</style> 