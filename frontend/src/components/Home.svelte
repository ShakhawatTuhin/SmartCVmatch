<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { uploadResume, login } from '../services/api';

  const dispatch = createEventDispatcher();

  let stats = $state({
    activeJobs: 1284,
    companiesHiring: 326,
    successfulMatches: 15420
  });

  let selectedFile: File | null = $state(null);
  let uploadProgress = $state(0);
  let isDragging = $state(false);
  let isUploading = $state(false);
  let error = $state<string | null>(null);
  let isAuthenticated = $state(false);
  let username = $state('');
  let password = $state('');
  let isLoggingIn = $state(false);

  // Check authentication on mount
  $effect(() => {
    checkAuth();
  });

  async function checkAuth() {
    try {
      // Use the API function rather than direct fetch
      const response = await fetch('http://127.0.0.1:8000/api/users/profile/', {
        credentials: 'include'
      });
      
      if (response.ok) {
        const userData = await response.json();
        console.log('User authenticated:', userData);
        isAuthenticated = true;
      } else {
        console.log('User not authenticated, status:', response.status);
        isAuthenticated = false;
      }
    } catch (e) {
      console.error('Auth check error:', e);
      isAuthenticated = false;
    }
  }

  async function handleLogin() {
    try {
      isLoggingIn = true;
      error = null;
      await login(username, password);
      isAuthenticated = true;
      username = '';
      password = '';
    } catch (e) {
      error = e instanceof Error ? e.message : 'Login failed';
    } finally {
      isLoggingIn = false;
    }
  }

  function handleDragEnter(e: DragEvent) {
    e.preventDefault();
    isDragging = true;
  }

  function handleDragLeave(e: DragEvent) {
    e.preventDefault();
    isDragging = false;
  }

  function handleDrop(e: DragEvent) {
    e.preventDefault();
    isDragging = false;
    
    if (e.dataTransfer?.files.length) {
      const file = e.dataTransfer.files[0];
      if (file && validateFile(file)) {
        selectedFile = file;
        error = null;
      }
    }
  }

  function handleFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      if (file && validateFile(file)) {
        selectedFile = file;
        error = null;
      }
    }
  }

  function validateFile(file: File): boolean {
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!allowedTypes.includes(file.type)) {
      error = 'Please upload a PDF or Word document';
      return false;
    }
    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      error = 'File size should be less than 5MB';
      return false;
    }
    return true;
  }

  async function handleUpload() {
    if (!selectedFile) {
      error = 'Please select a file first';
      return;
    }
    
    if (!isAuthenticated) {
      error = 'You must be logged in to upload a resume';
      return;
    }
    
    try {
      isUploading = true;
      error = null;
      uploadProgress = 0;

      // Simulate upload progress while the actual upload happens
      const progressInterval = setInterval(() => {
        if (uploadProgress < 90) {
          uploadProgress += 10;
        }
      }, 200);

      try {
        // Actual upload
        console.log('Starting resume upload...');
        const result = await uploadResume(selectedFile);
        console.log('Upload successful:', result);
        
        // Complete the progress bar
        clearInterval(progressInterval);
        uploadProgress = 100;

        // Wait a moment to show the complete progress
        await new Promise(resolve => setTimeout(resolve, 500));

        // Navigate to jobs page to see matches
        dispatch('navigate', { page: 'jobs' });
      } catch (uploadError) {
        console.error('Upload error:', uploadError);
        clearInterval(progressInterval);
        
        if (uploadError instanceof Error && uploadError.message.includes('401')) {
          // Session might have expired
          error = 'Authentication failed. Please login again.';
          isAuthenticated = false;
        } else {
          error = uploadError instanceof Error ? uploadError.message : 'Failed to upload resume';
        }
        uploadProgress = 0;
      }
    } finally {
      isUploading = false;
    }
  }
</script>

<div class="home-page">
  <!-- Hero Section -->
  <section class="hero-section">
    <div class="hero-content">
      <h1>Smart Resume Analyzer & Job Matcher</h1>
      <p>Upload your resume and let our AI find the perfect job matches for you</p>
      
      {#if !isAuthenticated}
        <div class="login-container">
          <h2>Login to Upload Resume</h2>
          <form onsubmit={e => { e.preventDefault(); handleLogin(); }} class="login-form">
            <div class="form-group">
              <label for="username">Username</label>
              <input 
                type="text" 
                id="username"
                bind:value={username}
                disabled={isLoggingIn}
              />
            </div>
            <div class="form-group">
              <label for="password">Password</label>
              <input 
                type="password" 
                id="password"
                bind:value={password}
                disabled={isLoggingIn}
              />
            </div>
            {#if error}
              <div class="error-message">
                <i class="fas fa-exclamation-circle"></i>
                {error}
              </div>
            {/if}
            <button 
              type="submit" 
              class="login-button"
              disabled={isLoggingIn}
            >
              {isLoggingIn ? 'Logging in...' : 'Login'}
            </button>
          </form>
        </div>
      {:else}
        <div class="upload-container">
          <div 
            class="upload-box"
            class:dragging={isDragging}
            class:error={error}
            ondragenter={handleDragEnter}
            ondragover={e => e.preventDefault()}
            ondragleave={handleDragLeave}
            ondrop={handleDrop}
            role="button"
            tabindex="0"
          >
            <input 
              type="file" 
              accept=".pdf,.doc,.docx" 
              id="resume-upload"
              onchange={handleFileSelect}
              class="hidden"
              disabled={isUploading}
            />
            <label for="resume-upload" class="upload-label">
              <i class="fas fa-cloud-upload-alt"></i>
              <span class="upload-text">
                {#if selectedFile}
                  Selected: {selectedFile.name}
                {:else}
                  Choose File or Drag & Drop
                {/if}
              </span>
              <span class="upload-hint">Supports PDF, DOC, DOCX (max 5MB)</span>
            </label>
          </div>

          {#if error}
            <div class="error-message">
              <i class="fas fa-exclamation-circle"></i>
              {error}
            </div>
          {/if}

          <button 
            class="upload-button" 
                          onclick={handleUpload}
            disabled={!selectedFile || isUploading}
          >
            {#if isUploading}
              Uploading...
            {:else}
              Upload & Find Matches
            {/if}
          </button>

          {#if uploadProgress > 0}
            <div class="progress-container">
              <div class="progress-bar">
                <div 
                  class="progress" 
                  style="width: {uploadProgress}%"
                  class:complete={uploadProgress === 100}
                ></div>
              </div>
              <span class="progress-text">{uploadProgress}%</span>
            </div>
          {/if}
        </div>
      {/if}
    </div>
  </section>

  <!-- Stats Section -->
  <section class="stats-section">
    <div class="stat-card">
      <div class="stat-value">{stats.activeJobs}</div>
      <div class="stat-label">Active Jobs</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{stats.companiesHiring}</div>
      <div class="stat-label">Companies Hiring</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{stats.successfulMatches}</div>
      <div class="stat-label">Successful Matches</div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="features-section">
    <h2>How It Works</h2>
    <div class="features-grid">
      <div class="feature-card">
        <i class="fas fa-file-upload"></i>
        <h3>Upload Resume</h3>
        <p>Upload your resume in PDF or DOC format</p>
      </div>
      <div class="feature-card">
        <i class="fas fa-brain"></i>
        <h3>AI Analysis</h3>
        <p>Our AI analyzes your skills and experience</p>
      </div>
      <div class="feature-card">
        <i class="fas fa-bullseye"></i>
        <h3>Smart Matching</h3>
        <p>Get matched with relevant job opportunities</p>
      </div>
      <div class="feature-card">
        <i class="fas fa-paper-plane"></i>
        <h3>Quick Apply</h3>
        <p>Apply to jobs with one click</p>
      </div>
    </div>
  </section>
</div>

<style>
  .home-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .hero-section {
    text-align: center;
    margin-bottom: 4rem;
  }

  .hero-content {
    max-width: 800px;
    margin: 0 auto;
  }

  h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 1rem;
  }

  .hero-content p {
    font-size: 1.25rem;
    color: #6b7280;
    margin-bottom: 2rem;
  }

  .login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 2rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .login-container h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 1.5rem;
  }

  .login-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .form-group {
    text-align: left;
  }

  .form-group label {
    display: block;
    font-size: 0.9rem;
    font-weight: 500;
    color: #374151;
    margin-bottom: 0.5rem;
  }

  .form-group input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    font-size: 1rem;
    transition: border-color 0.2s;
  }

  .form-group input:focus {
    outline: none;
    border-color: #dc2626;
  }

  .login-button {
    width: 100%;
    padding: 0.875rem;
    background: #dc2626;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .login-button:hover:not(:disabled) {
    background: #b91c1c;
  }

  .login-button:disabled {
    background: #e5e7eb;
    cursor: not-allowed;
  }

  .upload-container {
    max-width: 600px;
    margin: 0 auto;
  }

  .upload-box {
    background: white;
    border: 2px dashed #e5e7eb;
    border-radius: 8px;
    padding: 2rem;
    margin-bottom: 1rem;
    transition: all 0.2s;
  }

  .upload-box.dragging {
    border-color: #dc2626;
    background: #fef2f2;
  }

  .upload-box.error {
    border-color: #ef4444;
    background: #fef2f2;
  }

  .hidden {
    display: none;
  }

  .upload-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    cursor: pointer;
  }

  .upload-label i {
    font-size: 2.5rem;
    color: #dc2626;
  }

  .upload-text {
    font-size: 1.1rem;
    color: #111827;
  }

  .upload-hint {
    font-size: 0.9rem;
    color: #6b7280;
  }

  .error-message {
    color: #ef4444;
    font-size: 0.9rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .upload-button {
    width: 100%;
    padding: 0.875rem;
    background: #dc2626;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .upload-button:hover:not(:disabled) {
    background: #b91c1c;
  }

  .upload-button:disabled {
    background: #e5e7eb;
    cursor: not-allowed;
  }

  .progress-container {
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .progress-bar {
    flex: 1;
    height: 8px;
    background: #f3f4f6;
    border-radius: 4px;
    overflow: hidden;
  }

  .progress {
    height: 100%;
    background: #10b981;
    transition: width 0.2s;
  }

  .progress.complete {
    background: #059669;
  }

  .progress-text {
    font-size: 0.9rem;
    color: #6b7280;
    min-width: 48px;
  }

  .stats-section {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin-bottom: 4rem;
  }

  .stat-card {
    background: white;
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .stat-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #dc2626;
    margin-bottom: 0.5rem;
  }

  .stat-label {
    color: #6b7280;
    font-size: 1.1rem;
  }

  .features-section {
    text-align: center;
    margin-bottom: 4rem;
  }

  .features-section h2 {
    font-size: 2rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 2rem;
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
  }

  .feature-card {
    background: white;
    border-radius: 8px;
    padding: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .feature-card i {
    font-size: 2rem;
    color: #dc2626;
    margin-bottom: 1rem;
  }

  .feature-card h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.5rem;
  }

  .feature-card p {
    color: #6b7280;
    font-size: 0.95rem;
    line-height: 1.5;
  }

  @media (max-width: 768px) {
    h1 {
      font-size: 2rem;
    }

    .stats-section {
      grid-template-columns: 1fr;
    }

    .features-grid {
      grid-template-columns: 1fr;
    }
  }
</style> 