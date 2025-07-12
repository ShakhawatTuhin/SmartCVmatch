<script lang="ts">
  import { register } from '../services/api';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  let username = $state('');
  let password = $state('');
  let confirmPassword = $state('');
  let email = $state('');
  let isRegistering = $state(false);
  let error = $state<string | null>(null);

  async function handleRegister(event: Event) {
    event.preventDefault();
    if (password !== confirmPassword) {
      error = 'Passwords do not match';
      return;
    }

    try {
      isRegistering = true;
      error = null;
      
      // Add debugging
      console.log('Attempting to register with:', { username, email });
      
      try {
        await register({
          username,
          email,
          password,
          password2: confirmPassword
        });
        // After successful registration, navigate to home
        dispatch('navigate', { page: 'home' });
      } catch (apiError) {
        console.error('Registration API error:', apiError);
        // Try to extract a more user-friendly error message
        let errorMsg = 'Registration failed';
        if (apiError instanceof Error) {
          try {
            // Try to parse the error message as JSON
            const errorData = JSON.parse(apiError.message);
            if (errorData.username) errorMsg = `Username error: ${errorData.username}`;
            else if (errorData.email) errorMsg = `Email error: ${errorData.email}`;
            else if (errorData.password) errorMsg = `Password error: ${errorData.password}`;
            else if (errorData.password2) errorMsg = `Confirm password error: ${errorData.password2}`;
            else if (errorData.non_field_errors) errorMsg = errorData.non_field_errors;
            else errorMsg = apiError.message;
          } catch {
            errorMsg = apiError.message;
          }
        }
        error = errorMsg;
      }
    } catch (e) {
      console.error('Registration error:', e);
      error = e instanceof Error ? e.message : 'Registration failed';
    } finally {
      isRegistering = false;
    }
  }
</script>

<div class="register-page">
  <div class="register-container">
    <h2>Create Account</h2>
    <form onsubmit={handleRegister} class="register-form">
      <div class="form-group">
        <label for="username">Username</label>
        <input 
          type="text" 
          id="username"
          bind:value={username}
          disabled={isRegistering}
          required
        />
      </div>

      <div class="form-group">
        <label for="email">Email (optional)</label>
        <input 
          type="email" 
          id="email"
          bind:value={email}
          disabled={isRegistering}
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input 
          type="password" 
          id="password"
          bind:value={password}
          disabled={isRegistering}
          required
        />
      </div>

      <div class="form-group">
        <label for="confirm-password">Confirm Password</label>
        <input 
          type="password" 
          id="confirm-password"
          bind:value={confirmPassword}
          disabled={isRegistering}
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
        class="register-button"
        disabled={isRegistering}
      >
        {isRegistering ? 'Creating Account...' : 'Create Account'}
      </button>

      <div class="login-link">
        Already have an account? 
        <button 
          type="button" 
          class="link-button"
          onclick={() => dispatch('navigate', { page: 'login' })}
        >
          Login here
        </button>
      </div>
    </form>
  </div>
</div>

<style>
  .register-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 4rem);
  }

  .register-container {
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

  .register-form {
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

  .register-button {
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

  .register-button:hover:not(:disabled) {
    background: #b91c1c;
  }

  .register-button:disabled {
    background: #e5e7eb;
    cursor: not-allowed;
  }

  .login-link {
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