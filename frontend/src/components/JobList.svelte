<script lang="ts">
  import type { Job } from '../types/job';

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
      isSaved: false
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
      isSaved: true
    }
  ]);

  let sortBy = $state("Most Recent");
  let totalJobs = $state(1284);
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
            <button class="save-btn">
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