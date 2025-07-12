<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { Job } from '../types/models';
  import { getBookmarks, removeBookmark } from '../services/api';

  const dispatch = createEventDispatcher();

  let bookmarkedJobs = $state<Job[]>([]);
  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let searchQuery = $state('');

  // Load bookmarked jobs on mount
  $effect(() => {
    loadBookmarkedJobs();
  });

  async function loadBookmarkedJobs() {
    try {
      isLoading = true;
      error = null;
      const bookmarks = await getBookmarks();
      // Since Bookmark doesn't have a job property, we need to fetch the jobs separately
      // For now, let's assume the bookmarks contain enough job data to display
      bookmarkedJobs = bookmarks.map(bookmark => ({
        id: bookmark.jobId,
        title: 'Job ' + bookmark.jobId,
        company: 'Company',
        location: 'Location',
        description: 'Description',
        match_score: 0,
        required_skills: [],
        apply_url: '',
        posted_at: bookmark.createdAt
      } as Job));
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load bookmarked jobs';
    } finally {
      isLoading = false;
    }
  }

  async function handleRemoveBookmark(jobId: number) {
    try {
      await removeBookmark(jobId);
      bookmarkedJobs = bookmarkedJobs.filter(job => job.id !== jobId);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to remove bookmark';
    }
  }

  let filteredJobs = $derived(bookmarkedJobs.filter(job => 
    !searchQuery || 
    job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    job.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
    job.location.toLowerCase().includes(searchQuery.toLowerCase())
  ));
</script>

<div class="bookmarks-page">
  <div class="header">
    <h1>Saved Jobs</h1>
    <div class="search-bar">
      <i class="fas fa-search"></i>
      <input 
        type="text"
        placeholder="Search saved jobs..."
        bind:value={searchQuery}
      />
    </div>
  </div>

  {#if isLoading}
    <div class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      Loading saved jobs...
    </div>
  {:else if error}
    <div class="error">
      <i class="fas fa-exclamation-circle"></i>
      {error}
    </div>
  {:else if filteredJobs.length > 0}
    <div class="bookmarks-grid">
      {#each filteredJobs as job}
        <div class="job-card">
          <div class="job-header">
            <div class="job-title">
              <h3>{job.title}</h3>
              <span class="company">{job.company}</span>
            </div>
            <button 
              class="remove-btn"
              onclick={() => handleRemoveBookmark(job.id)}
              aria-label="Remove job from bookmarks"
            >
              <i class="fas fa-trash-alt"></i>
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
            <button class="share-btn" aria-label="Share job">
              <i class="fas fa-share-alt"></i>
              Share
            </button>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <div class="empty-state">
      <i class="fas fa-bookmark"></i>
      <h2>No saved jobs</h2>
      <p>Jobs you save will appear here for easy access.</p>
      <button 
        class="primary-btn"
        onclick={() => dispatch('navigate', { page: 'jobs' })}
      >
        Find Jobs
      </button>
    </div>
  {/if}
</div>

<style>
  .bookmarks-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }

  h1 {
    font-size: 2rem;
    font-weight: 600;
    color: #111827;
  }

  .search-bar {
    position: relative;
    width: 300px;
  }

  .search-bar i {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #6b7280;
  }

  .search-bar input {
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 2.5rem;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    font-size: 1rem;
  }

  .search-bar input:focus {
    outline: none;
    border-color: #dc2626;
  }

  .bookmarks-grid {
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

  .remove-btn {
    background: none;
    border: none;
    color: #6b7280;
    cursor: pointer;
    padding: 0.5rem;
    transition: color 0.2s;
  }

  .remove-btn:hover {
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

  .primary-btn {
    padding: 0.75rem 1.5rem;
    background: #dc2626;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .primary-btn:hover {
    background: #b91c1c;
  }

  @media (max-width: 768px) {
    .header {
      flex-direction: column;
      gap: 1rem;
      align-items: stretch;
    }

    .search-bar {
      width: 100%;
    }

    .bookmarks-grid {
      grid-template-columns: 1fr;
    }
  }
</style> 