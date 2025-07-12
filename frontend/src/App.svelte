<script lang="ts">
  import Header from './components/Header.svelte';
  import Home from './components/Home.svelte';
  import JobFinder from './components/JobFinder.svelte';
  import Applications from './components/Applications.svelte';
  import Bookmarks from './components/Bookmarks.svelte';
  import Profile from './components/Profile.svelte';
  import Register from './components/Register.svelte';
  import Login from './components/Login.svelte';

  type Page = 'home' | 'jobs' | 'applications' | 'bookmarks' | 'profile' | 'register' | 'login';
  let currentPage = $state<Page>('home');

  function handleNavigation(event: CustomEvent<{ page: Page }>) {
    currentPage = event.detail.page;
  }
</script>

<div class="app">
  <Header {currentPage} on:navigate={handleNavigation} />
  
  <main>
    {#if currentPage === 'home'}
      <Home on:navigate={handleNavigation} />
    {:else if currentPage === 'jobs'}
      <JobFinder />
    {:else if currentPage === 'applications'}
      <Applications />
    {:else if currentPage === 'bookmarks'}
      <Bookmarks />
    {:else if currentPage === 'profile'}
      <Profile />
    {:else if currentPage === 'register'}
      <Register on:navigate={handleNavigation} />
    {:else if currentPage === 'login'}
      <Login on:navigate={handleNavigation} />
    {/if}
  </main>
</div>

<style>
  .app {
    min-height: 100vh;
    background-color: #f3f4f6;
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  main {
    padding: 1rem;
    flex: 1;
  }

  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #111827;
    background: #f9fafb;
  }

  :global(*, *::before, *::after) {
    box-sizing: border-box;
  }

  :global(button) {
    font-family: inherit;
  }
</style>
