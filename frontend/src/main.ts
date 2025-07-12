import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'

// Add network request monitoring
const originalFetch = window.fetch;
window.fetch = function(input: RequestInfo | URL, init?: RequestInit) {
  console.log('Fetch request:', { url: input, options: init });
  return originalFetch(input, init)
    .then(response => {
      console.log('Fetch response:', { 
        url: input, 
        status: response.status,
        statusText: response.statusText,
        headers: Object.fromEntries(response.headers.entries())
      });
      return response;
    })
    .catch(error => {
      console.error('Fetch error:', { url: input, error });
      throw error;
    });
};

const app = mount(App, {
  target: document.getElementById('app')!,
})

export default app
