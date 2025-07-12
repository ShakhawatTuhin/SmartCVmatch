<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();

  let applications = $state([
    {
      id: 1,
      jobTitle: "Frontend Developer",
      company: "TechCorp",
      status: "Applied",
      appliedDate: "2024-03-01",
      nextStep: "Technical Interview",
      nextStepDate: "2024-03-15"
    },
    {
      id: 2,
      jobTitle: "Full Stack Engineer",
      company: "StartupX",
      status: "Interview",
      appliedDate: "2024-02-28",
      nextStep: "Final Interview",
      nextStepDate: "2024-03-10"
    }
  ]);

  let statusFilters = ["All", "Applied", "Interview", "Offer", "Rejected"];
  let selectedStatus = $state("All");

  let filteredApplications = $derived(applications.filter(app => 
    selectedStatus === "All" || app.status === selectedStatus
  ));

  function setStatusFilter(status: string) {
    selectedStatus = status;
  }
</script>

<div class="applications-page">
  <div class="header">
    <h1>My Applications</h1>
    <div class="status-filters">
      {#each statusFilters as status}
        <button 
          class="filter-btn"
          class:active={selectedStatus === status}
          onclick={() => setStatusFilter(status)}
        >
          {status}
        </button>
      {/each}
    </div>
  </div>

  {#if filteredApplications.length > 0}
    <div class="applications-list">
      {#each filteredApplications as app}
        <div class="application-card">
          <div class="application-header">
            <div class="job-info">
              <h3>{app.jobTitle}</h3>
              <span class="company">{app.company}</span>
            </div>
            <div class="status-badge" class:interview={app.status === "Interview"}>
              {app.status}
            </div>
          </div>
          
          <div class="application-details">
            <div class="detail-item">
              <i class="fas fa-calendar"></i>
              <span>Applied: {new Date(app.appliedDate).toLocaleDateString()}</span>
            </div>
            <div class="detail-item">
              <i class="fas fa-clock"></i>
              <span>Next: {app.nextStep} on {new Date(app.nextStepDate).toLocaleDateString()}</span>
            </div>
          </div>

          <div class="application-actions">
            <button class="action-btn">
              <i class="fas fa-envelope"></i>
              Contact
            </button>
            <button class="action-btn">
              <i class="fas fa-file-alt"></i>
              View CV
            </button>
            <button class="action-btn">
              <i class="fas fa-trash-alt"></i>
              Withdraw
            </button>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <div class="empty-state">
      <i class="fas fa-briefcase"></i>
      <h2>No applications found</h2>
      <p>Start applying to jobs to track your applications here.</p>
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
  .applications-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .header {
    margin-bottom: 2rem;
  }

  h1 {
    font-size: 2rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 1rem;
  }

  .status-filters {
    display: flex;
    gap: 0.5rem;
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

  .applications-list {
    display: grid;
    gap: 1rem;
  }

  .application-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .application-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
  }

  .job-info h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.25rem;
  }

  .company {
    color: #6b7280;
    font-size: 0.95rem;
  }

  .status-badge {
    padding: 0.25rem 0.75rem;
    background: #f3f4f6;
    color: #374151;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
  }

  .status-badge.interview {
    background: #dcfce7;
    color: #15803d;
  }

  .application-details {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .detail-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #6b7280;
    font-size: 0.95rem;
  }

  .application-actions {
    display: flex;
    gap: 0.5rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
  }

  .action-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    background: white;
    color: #6b7280;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s;
  }

  .action-btn:hover {
    border-color: #dc2626;
    color: #dc2626;
  }

  .empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #6b7280;
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

  @media (max-width: 640px) {
    .application-header {
      flex-direction: column;
      gap: 1rem;
    }

    .application-actions {
      flex-wrap: wrap;
    }

    .action-btn {
      flex: 1;
      justify-content: center;
    }
  }
</style> 