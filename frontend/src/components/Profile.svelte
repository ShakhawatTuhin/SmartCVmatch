<script lang="ts">
  import type { User } from '../types/models';
  import { getProfile, updateProfile, changePassword } from '../services/api';

  let user = $state<User>({
    username: '',
    email: '',
    firstName: '',
    lastName: '',
    phone: '',
    location: '',
    bio: ''
  });

  let isEditing = $state(false);
  let isChangingPassword = $state(false);
  let error = $state<string | null>(null);
  let success = $state<string | null>(null);
  let isLoading = $state(true);

  let editedUser = $state<User>({ ...user });
  
  // Load user profile on mount
  $effect(() => {
    loadUserProfile();
  });
  
  async function loadUserProfile() {
    try {
      isLoading = true;
      error = null;
      const profileData = await getProfile();
      console.log('Profile data loaded:', profileData);
      
      user = {
        username: profileData.username || '',
        email: profileData.email || '',
        firstName: profileData.first_name || '',
        lastName: profileData.last_name || '',
        phone: profileData.phone || '',
        location: profileData.location || '',
        bio: profileData.bio || '',
        // Store the backend fields too
        first_name: profileData.first_name || '',
        last_name: profileData.last_name || ''
      };
      
      editedUser = { ...user };
      
    } catch (e) {
      console.error('Failed to load profile:', e);
      error = e instanceof Error ? e.message : 'Failed to load profile';
    } finally {
      isLoading = false;
    }
  }
  
  // Create derived values for user data
  let userName = $derived(`${user.firstName || ''} ${user.lastName || ''}`.trim() || user.username);
  let userEmail = $derived(user.email);
  let userPhone = $derived(user.phone || 'Not provided');
  let userLocation = $derived(user.location || 'Not provided');
  let userBio = $derived(user.bio || 'No bio provided');
  
  let passwords = $state({
    current: '',
    new: '',
    confirm: ''
  });

  async function handleUpdateProfile() {
    try {
      error = null;
      
      // Convert to the format expected by the API (snake_case)
      const profileUpdate = {
        first_name: editedUser.firstName,
        last_name: editedUser.lastName,
        email: editedUser.email,
        // Include these if you add them to your backend model later
        // phone: editedUser.phone,
        // location: editedUser.location,
        // bio: editedUser.bio
      };
      
      await updateProfile(profileUpdate);
      
      // Update the local user object with the edited values
      user = { 
        ...user,
        firstName: editedUser.firstName,
        lastName: editedUser.lastName,
        email: editedUser.email,
        phone: editedUser.phone,
        location: editedUser.location,
        bio: editedUser.bio,
        // Also update snake_case fields
        first_name: editedUser.firstName,
        last_name: editedUser.lastName
      };
      
      success = 'Profile updated successfully!';
      isEditing = false;
      setTimeout(() => success = null, 3000);
    } catch (e) {
      console.error('Update profile error:', e);
      error = e instanceof Error ? e.message : 'Failed to update profile';
    }
  }

  async function handleChangePassword() {
    if (passwords.new !== passwords.confirm) {
      error = 'New passwords do not match';
      return;
    }

    try {
      error = null;
      await changePassword(passwords.current, passwords.new);
      success = 'Password changed successfully!';
      isChangingPassword = false;
      passwords = { current: '', new: '', confirm: '' };
      setTimeout(() => success = null, 3000);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to change password';
    }
  }

  function cancelEdit() {
    editedUser = { ...user };
    isEditing = false;
    error = null;
  }

  function cancelPasswordChange() {
    passwords = { current: '', new: '', confirm: '' };
    isChangingPassword = false;
    error = null;
  }
</script>

<div class="profile-page">
  <div class="header">
    <h1>Profile Settings</h1>
    {#if !isEditing && !isLoading}
      <button 
        class="edit-btn"
        onclick={() => isEditing = true}
      >
        <i class="fas fa-edit"></i>
        Edit Profile
      </button>
    {/if}
  </div>

  {#if error}
    <div class="alert error">
      <i class="fas fa-exclamation-circle"></i>
      {error}
    </div>
  {/if}

  {#if success}
    <div class="alert success">
      <i class="fas fa-check-circle"></i>
      {success}
    </div>
  {/if}

  {#if isLoading}
    <div class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      Loading profile...
    </div>
  {:else}
    <div class="profile-section">
      <h2>Personal Information</h2>
      {#if isEditing}
        <div class="form-grid">
          <div class="form-group">
            <label for="firstName">First Name</label>
            <input 
              type="text"
              id="firstName"
              bind:value={editedUser.firstName}
            />
          </div>
          <div class="form-group">
            <label for="lastName">Last Name</label>
            <input 
              type="text"
              id="lastName"
              bind:value={editedUser.lastName}
            />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input 
              type="email"
              id="email"
              bind:value={editedUser.email}
            />
          </div>
          <div class="form-group">
            <label for="phone">Phone</label>
            <input 
              type="tel"
              id="phone"
              bind:value={editedUser.phone}
            />
          </div>
          <div class="form-group full-width">
            <label for="location">Location</label>
            <input 
              type="text"
              id="location"
              bind:value={editedUser.location}
            />
          </div>
          <div class="form-group full-width">
            <label for="bio">Bio</label>
            <textarea 
              id="bio"
              rows="4"
              bind:value={editedUser.bio}
            ></textarea>
          </div>
        </div>
        <div class="form-actions">
          <button 
            class="primary-btn"
            onclick={handleUpdateProfile}
          >
            Save Changes
          </button>
          <button 
            class="secondary-btn"
            onclick={cancelEdit}
          >
            Cancel
          </button>
        </div>
      {:else}
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Username</span>
            <span class="value">{user.username}</span>
          </div>
          <div class="info-item">
            <span class="label">Name</span>
            <span class="value">{userName}</span>
          </div>
          <div class="info-item">
            <span class="label">Email</span>
            <span class="value">{userEmail}</span>
          </div>
          <div class="info-item">
            <span class="label">Phone</span>
            <span class="value">{userPhone}</span>
          </div>
          <div class="info-item">
            <span class="label">Location</span>
            <span class="value">{userLocation}</span>
          </div>
          <div class="info-item full-width">
            <span class="label">Bio</span>
            <span class="value">{userBio}</span>
          </div>
        </div>
      {/if}
    </div>
  {/if}

  <div class="profile-section">
    <h2>Security</h2>
    {#if isChangingPassword}
      <div class="form-grid">
        <div class="form-group">
          <label for="currentPassword">Current Password</label>
          <input 
            type="password"
            id="currentPassword"
            bind:value={passwords.current}
          />
        </div>
        <div class="form-group">
          <label for="newPassword">New Password</label>
          <input 
            type="password"
            id="newPassword"
            bind:value={passwords.new}
          />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm New Password</label>
          <input 
            type="password"
            id="confirmPassword"
            bind:value={passwords.confirm}
          />
        </div>
      </div>
      <div class="form-actions">
        <button 
          class="primary-btn"
          onclick={handleChangePassword}
        >
          Change Password
        </button>
        <button 
          class="secondary-btn"
          onclick={cancelPasswordChange}
        >
          Cancel
        </button>
      </div>
    {:else}
      <button 
        class="secondary-btn"
        onclick={() => isChangingPassword = true}
      >
        <i class="fas fa-key"></i>
        Change Password
      </button>
    {/if}
  </div>
</div>

<style>
  .profile-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }
  
  .loading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    color: #6b7280;
    font-size: 1rem;
  }
  
  .loading i {
    margin-right: 0.5rem;
    color: #dc2626;
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

  h2 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 1.5rem;
  }

  .profile-section {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
  }

  .alert {
    padding: 1rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .alert.error {
    background: #fef2f2;
    color: #dc2626;
  }

  .alert.success {
    background: #dcfce7;
    color: #15803d;
  }

  .form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .form-group.full-width {
    grid-column: span 2;
  }

  label {
    font-size: 0.95rem;
    font-weight: 500;
    color: #374151;
  }

  input, textarea {
    padding: 0.75rem;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    font-size: 1rem;
  }

  input:focus, textarea:focus {
    outline: none;
    border-color: #dc2626;
  }

  textarea {
    resize: vertical;
  }

  .form-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .info-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }

  .info-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .info-item.full-width {
    grid-column: span 2;
  }

  .label {
    font-size: 0.875rem;
    color: #6b7280;
  }

  .value {
    font-size: 1rem;
    color: #111827;
  }

  .edit-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: none;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    color: #6b7280;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.2s;
  }

  .edit-btn:hover {
    border-color: #dc2626;
    color: #dc2626;
  }

  .primary-btn {
    padding: 0.75rem 1.5rem;
    background: #dc2626;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .primary-btn:hover {
    background: #b91c1c;
  }

  .secondary-btn {
    padding: 0.75rem 1.5rem;
    background: white;
    color: #6b7280;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .secondary-btn:hover {
    border-color: #dc2626;
    color: #dc2626;
  }

  @media (max-width: 640px) {
    .form-grid, .info-grid {
      grid-template-columns: 1fr;
    }

    .form-group.full-width {
      grid-column: auto;
    }

    .info-item.full-width {
      grid-column: auto;
    }

    .form-actions {
      flex-direction: column;
    }

    .header {
      flex-direction: column;
      gap: 1rem;
      align-items: flex-start;
    }
  }
</style> 