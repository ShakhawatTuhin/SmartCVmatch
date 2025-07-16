<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { logout } from '../services/api';

  const dispatch = createEventDispatcher();

  const { currentPage } = $props<{ currentPage: string }>();

  let isAuthenticated = $state(false);
  let isMenuOpen = $state(false);
  let userProfile = $state<any>(null);

  // Check authentication on mount
  $effect(() => {
    checkAuth();
  });

  async function checkAuth() {
    try {
      // Use direct fetch like in Home.svelte to ensure consistency
      const response = await fetch('/api/users/profile/', {
        credentials: 'include'
      });
      
      if (response.ok) {
        const profile = await response.json();
        isAuthenticated = true;
        userProfile = profile;
        console.log('User authenticated in Header:', profile);
      } else {
        console.log('User not authenticated in Header, status:', response.status);
        isAuthenticated = false;
        userProfile = null;
      }
    } catch (e) {
      console.error('Auth check error in Header:', e);
      isAuthenticated = false;
      userProfile = null;
    }
  }

  async function handleLogout() {
    try {
      await logout();
      isAuthenticated = false;
      userProfile = null;
      dispatch('navigate', { page: 'home' });
    } catch (e) {
      console.error('Logout failed:', e);
    }
  }

  function navigate(page: string) {
    isMenuOpen = false;
    dispatch('navigate', { page });
  }

  // Add a derived value to use userProfile
  let username = $derived(userProfile?.username || 'Guest');
</script>

<header class="header">
  <div class="container">
    <button 
      class="logo" 
      onclick={() => navigate('home')}
      aria-label="Go to home page"
    >
      <span>SmartCV Match</span>
    </button>

    <nav class="nav-menu" class:open={isMenuOpen}>
      {#if isAuthenticated}
        <div class="user-greeting">Hello, {username}</div>
        <button 
          class="nav-item" 
          class:active={currentPage === 'jobs'}
          onclick={() => navigate('jobs')}
        >
          <i class="fas fa-search"></i>
          <span>Find Jobs</span>
        </button>

        <button 
          class="nav-item" 
          class:active={currentPage === 'applications'}
          onclick={() => navigate('applications')}
        >
          <i class="fas fa-file-alt"></i>
          <span>Applications</span>
        </button>

        <button 
          class="nav-item" 
          class:active={currentPage === 'bookmarks'}
          onclick={() => navigate('bookmarks')}
        >
          <i class="fas fa-bookmark"></i>
          <span>Bookmarks</span>
        </button>

        <button 
          class="nav-item" 
          class:active={currentPage === 'profile'}
          onclick={() => navigate('profile')}
        >
          <i class="fas fa-user"></i>
          <span>Profile</span>
        </button>

        <button 
          class="nav-item" 
          onclick={handleLogout}
        >
          <i class="fas fa-sign-out-alt"></i>
          <span>Logout</span>
        </button>
      {:else}
        <button 
          class="nav-item" 
          class:active={currentPage === 'login'}
          onclick={() => navigate('login')}
        >
          <i class="fas fa-sign-in-alt"></i>
          <span>Login</span>
        </button>
        
        <button 
          class="nav-item" 
          class:active={currentPage === 'register'}
          onclick={() => navigate('register')}
        >
          <i class="fas fa-user-plus"></i>
          <span>Register</span>
        </button>
      {/if}
    </nav>

    <div class="mobile-menu">
      <button 
        class="menu-toggle" 
        aria-label="Toggle menu"
        onclick={() => isMenuOpen = !isMenuOpen}
      >
        <i class="fas fa-bars"></i>
      </button>
    </div>
  </div>
</header>

<style>
  .header {
    background: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    cursor: pointer;
    background: none;
    border: none;
  }

  .nav-menu {
    display: flex;
    gap: 1rem;
  }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border: none;
    background: none;
    color: #6b7280;
    font-size: 1rem;
    cursor: pointer;
    transition: color 0.2s;
    border-radius: 6px;
  }

  .nav-item:hover {
    color: #111827;
    background: #f3f4f6;
  }

  .nav-item.active {
    color: #dc2626;
    background: #fef2f2;
  }

  .user-greeting {
    padding: 0.5rem 1rem;
    font-weight: 500;
    color: #111827;
  }

  .mobile-menu {
    display: none;
  }

  .menu-toggle {
    background: none;
    border: none;
    color: #6b7280;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0.5rem;
  }

  @media (max-width: 768px) {
    .nav-menu {
      display: none;
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: white;
      padding: 1rem;
      flex-direction: column;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .nav-menu.open {
      display: flex;
    }

    .mobile-menu {
      display: block;
    }
  }
</style> 