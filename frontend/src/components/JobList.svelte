<script lang="ts">
  import type { Job } from '../types/job';
  import type { Bookmark } from '../types/models';
  import { addBookmark, removeBookmark, getBookmarks } from '../services/api';
  import { onMount } from 'svelte';

  let jobs = $state<Job[]>([
    {
      id: 1,
      title: "Office Assistant / Social Media Assistant",
      company: "JD",
      location: "London, UK",
      matchScore: 92,
      description: "As the Digital Marketing Manager, E-Commerce, you will be collaborating with E-Commerce department and Communication department...",
      postedDate: "2 days ago",
      isRecommended: true,
      isSaved: false,
      salary: "Competitive",
      jobType: "Full-time",
      experience: "1-3 years",
      skills: ["Marketing", "Social Media"]
    },
    {
      id: 2,
      title: "Marketing & Communications Manager",
      company: "Unilever",
      location: "London, UK",
      matchScore: 78,
      description: "Looking for a fun and rewarding career cheering people on as they gain their health and life back? Our clinic is a rewarding and positive place to work.",
      postedDate: "3 days ago",
      isRecommended: false,
      isSaved: true,
      salary: "£40,000 - £50,000",
      jobType: "Full-time",
      experience: "3-5 years",
      skills: ["Marketing", "Communications", "Management"]
    }
  ]);

  let sortBy = $state("Most Recent");
  let totalJobs = $state(1284);
  let saveInProgress = $state<Record<number, boolean>>({});
  let isLoading = $state(true);
  
  onMount(async () => {
    try {
      // Fetch bookmarks from API
      const bookmarks = await getBookmarks();
      
      // Create a set of bookmarked job IDs for easy lookup
      const bookmarkedJobIds = new Set(bookmarks.map(bookmark => bookmark.jobId));
      
      // Update the isSaved property for each job
      jobs = jobs.map(job => ({
        ...job,
        isSaved: bookmarkedJobIds.has(job.id)
      }));
    } catch (error) {
      console.error('Failed to fetch bookmarks:', error);
    } finally {
      isLoading = false;
    }
  });
  
  async function toggleSave(jobId: number) {
    if (saveInProgress[jobId]) return; // Prevent double clicks
    
    saveInProgress[jobId] = true;
    
    try {
      const job = jobs.find(j => j.id === jobId);
      if (!job) return;
      
      if (job.isSaved) {
        // Remove bookmark
        await removeBookmark(jobId);
        console.log(`Job ${jobId} has been unbookmarked`);
      } else {
        // Add bookmark
        await addBookmark(jobId);
        console.log(`Job ${jobId} has been bookmarked`);
      }
      
      // Update local state
      jobs = jobs.map(job => {
        if (job.id === jobId) {
          return { ...job, isSaved: !job.isSaved };
        }
        return job;
      });
    } catch (error) {
      console.error(`Error toggling bookmark for job ${jobId}:`, error);
      alert('Failed to save job. Please try again.');
    } finally {
      saveInProgress[jobId] = false;
    }
  }
</script>

<div class="job-list">
  <div class="list-header">
    <div class="sort-dropdown">
      <select bind:value={sortBy}>
        <option>Most Recent</option>
        <option>Best Match</option>
        <option>Salary</option>
      </select>
    </div>
    <div class="job-count">
      Showing {totalJobs} jobs
    </div>
  </div>

  {#if isLoading}
    <div class="loading">Loading jobs...</div>
  {:else}
    <div class="jobs">
      {#each jobs as job}
        <div class="job-card">
          <div class="job-score">
            <div class="score-circle">
              {job.matchScore}
            </div>
          </div>
          <div class="job-content">
            <div class="job-header">
              <h3>{job.title}</h3>
              <button 
                class="save-btn" 
                on:click={() => toggleSave(job.id)}
                disabled={saveInProgress[job.id]}
                title={job.isSaved ? "Remove from saved jobs" : "Save this job"}
              >
                {job.isSaved ? '★' : '☆'}
              </button>
            </div>
            <div class="job-meta">
              <span class="company">{job.company}</span>
              <span class="location">{job.location}</span>
              <span class="date">{job.postedDate}</span>
            </div>
            <p class="job-description">{job.description}</p>
            {#if job.isRecommended}
              <div class="recommendation">
                <span class="star">★</span> Recommended
              </div>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .job-list {
    padding: 1rem 2rem;
  }

  .list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .sort-dropdown select {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
  }

  .job-count {
    color: #666;
  }
  
  .loading {
    text-align: center;
    padding: 2rem;
    color: #666;
  }

  .jobs {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .job-card {
    display: flex;
    gap: 1rem;
    padding: 1.5rem;
    background: white;
    border: 1px solid #eee;
    border-radius: 8px;
  }

  .job-score {
    display: flex;
    align-items: flex-start;
  }

  .score-circle {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #e8f5e9;
    color: #2e7d32;
    border-radius: 50%;
    font-weight: bold;
  }

  .job-content {
    flex: 1;
  }

  .job-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.5rem;
  }

  .job-header h3 {
    margin: 0;
    font-size: 1.2rem;
  }

  .save-btn {
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    color: #ffd700;
    transition: transform 0.2s ease;
  }
  
  .save-btn:hover {
    transform: scale(1.2);
  }
  
  .save-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .job-meta {
    display: flex;
    gap: 1rem;
    color: #666;
    margin-bottom: 0.5rem;
  }

  .job-description {
    color: #444;
    margin: 0.5rem 0;
  }

  .recommendation {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #666;
    font-size: 0.9rem;
  }

  .star {
    color: #ffd700;
  }
</style> 