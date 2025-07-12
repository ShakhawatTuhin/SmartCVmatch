<script lang="ts">
  import { login } from '../services/api';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  let username = $state('');
  let password = $state('');
  let isLoggingIn = $state(false);
  let error = $state<string | null>(null);

  async function handleLogin(event: Event) {
    event.preventDefault();
    
    try {
      isLoggingIn = true;
      error = null;
      
      console.log('Attempting to login with username:', username);
      
      await login(username, password);
      dispatch('navigate', { page: 'home' });
    } catch (e) {
      console.error('Login error:', e);
      error = e instanceof Error ? e.message : 'Login failed';
    } finally {
      isLoggingIn = false;
    }
  }
</script>

<div class="login-page">
  <div class="login-container">
    <h2>Login</h2>
    <form onsubmit={handleLogin} class="login-form">
      <div class="form-group">
        <label for="username">Username</label>
        <input 
          type="text" 
          id="username"
          bind:value={username}
          disabled={isLoggingIn}
          required
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input 
          type="password" 
          id="password"
          bind:value={password}
          disabled={isLoggingIn}
          required
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

      <div class="register-link">
        Don't have an account? 
        <button 
          type="button" 
          class="link-button"
          onclick={() => dispatch('navigate', { page: 'register' })}
        >
          Register here
        </button>
      </div>
    </form>
  </div>
</div>

<style>
  .login-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 4rem);
  }

  .login-container {
    width: 100%;
    max-width: 400px;
    padding: 2rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 1.5rem;
    text-align: center;
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

  .error-message {
    color: #ef4444;
    font-size: 0.9rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
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

  .register-link {
    text-align: center;
    margin-top: 1rem;
    font-size: 0.9rem;
    color: #6b7280;
  }

  .link-button {
    background: none;
    border: none;
    color: #dc2626;
    font-weight: 500;
    cursor: pointer;
    padding: 0;
    font-size: inherit;
  }

  .link-button:hover {
    text-decoration: underline;
  }
</style> 