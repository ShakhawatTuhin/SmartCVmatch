import type { User, Resume, Job, Bookmark, Application, JobMatch } from '../types/models';

// Use the proxy in development, absolute URL in production
const isProduction = import.meta.env.PROD;
const API_BASE_URL = isProduction 
  ? (import.meta.env['VITE_API_URL'] || 'https://smartcvmatch-backend.vercel.app/api')
  : '/api'; // This will use the Vite proxy

console.log('Using API URL:', API_BASE_URL);

// Store auth token in localStorage
let authToken: string | null = null;

// Try to load token from localStorage on module initialization
try {
  authToken = localStorage.getItem('authToken');
  console.log('Auth token loaded from storage:', authToken ? 'Found' : 'Not found');
} catch (e) {
  console.error('Failed to access localStorage:', e);
}

// Helper to add auth token to headers
function addAuthHeaders(headers: Record<string, string> = {}): Record<string, string> {
  const newHeaders = { ...headers };
  
  if (authToken) {
    newHeaders['Authorization'] = `Token ${authToken}`;
  }
  
  return newHeaders;
}

// Function to set auth token
export function setAuthToken(token: string | null): void {
  authToken = token;
  
  if (token) {
    try {
      localStorage.setItem('authToken', token);
    } catch (e) {
      console.error('Failed to store auth token:', e);
    }
  } else {
    try {
      localStorage.removeItem('authToken');
    } catch (e) {
      console.error('Failed to remove auth token:', e);
    }
  }
}

// Function to get CSRF token from cookies
function getCsrfToken(): string | null {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i]?.trim();
      if (cookie && cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Helper function to add CSRF token to headers
function addCsrfHeader(headers: Record<string, string> = {}): Record<string, string> {
  const csrfToken = getCsrfToken();
  if (csrfToken) {
    return {
      ...headers,
      'X-CSRFToken': csrfToken
    };
  }
  return headers;
}

// Helper function to initialize the API connection and fetch CSRF token
export async function initializeAPI(): Promise<void> {
  try {
    console.log('Initializing API connection');
    const response = await fetch(`${API_BASE_URL}/`, {
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      }
    });
    
    if (!response.ok) {
      console.error(`API initialization failed with status: ${response.status}`);
      return;
    }
    
    try {
      const data = await response.json();
      console.log('API initialization response:', data);
      
      // Get CSRF token from cookies
      const csrfToken = getCsrfToken();
      console.log('CSRF Token:', csrfToken ? 'Found' : 'Not found');
    } catch (jsonError) {
      console.error('Failed to parse API initialization response:', jsonError);
    }
  } catch (error) {
    console.error('Failed to initialize API:', error);
  }
}

// Call initializeAPI when this module is loaded
initializeAPI();

// Simplified error handling function
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorStatus = `HTTP error ${response.status}`;
    
    // Try to get more detailed error information
    let errorDetail = '';
    try {
      const data = await response.json();
      errorDetail = data && typeof data === 'object' ? JSON.stringify(data) : '';
    } catch {
      // Ignore JSON parsing errors
    }
    
    throw new Error(errorDetail || errorStatus);
  }
  
  return response.json();
}

// Auth endpoints
export async function login(username: string, password: string): Promise<{ token: string }> {
  console.log('Logging in user:', username);
  try {
    const csrfToken = getCsrfToken();
    const headers: Record<string, string> = { 
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };
    
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }
    
    const response = await fetch(`${API_BASE_URL}/users/login/`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({ username, password }),
      credentials: 'include',
    });
    
    if (!response.ok) {
      console.error('Login failed with status:', response.status);
      let errorText = `HTTP error ${response.status}`;
      
      try {
        const errorData = await response.json();
        console.error('Error data:', errorData);
        errorText = JSON.stringify(errorData);
      } catch (e) {
        console.error('Failed to parse error response:', e);
      }
      
      throw new Error(errorText);
    }
    
    const userData = await response.json();
    console.log('Login successful:', userData);
    
    // Save the auth token
    if (userData.token) {
      setAuthToken(userData.token);
      console.log('Auth token saved');
    } else {
      console.warn('No token received during login');
    }
    
    return userData;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}

export async function register(userData: {
  username: string;
  email: string;
  password: string;
  password2: string;
}): Promise<User> {
  console.log('Registering user:', userData.username);
  try {
    // Ensure we're sending the exact field names expected by the backend
    const requestData = {
      username: userData.username,
      email: userData.email,
      password: userData.password,
      password2: userData.password2
    };
    
    console.log('Sending registration data:', JSON.stringify(requestData));
    
    const csrfToken = getCsrfToken();
    const headers: Record<string, string> = { 
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };
    
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }
    
    const response = await fetch(`${API_BASE_URL}/users/register/`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(requestData),
      credentials: 'include',
    });
    
    if (!response.ok) {
      console.error('Registration failed with status:', response.status);
      let errorText = `HTTP error ${response.status}`;
      
      if (response.headers.get('content-type')?.includes('application/json')) {
        try {
          const errorData = await response.json();
          console.error('Error data:', errorData);
          errorText = JSON.stringify(errorData);
        } catch (e) {
          console.error('Failed to parse error response:', e);
        }
      } else {
        const errorText = await response.text();
        console.error('Error text:', errorText);
      }
      
      throw new Error(errorText);
    }
    
    const data = await response.json();
    console.log('Registration successful:', data);
    
    // Save the auth token
    if (data && data.token) {
      setAuthToken(data.token);
      console.log('Auth token saved after registration');
    } else {
      console.warn('No token received during registration');
    }
    
    return data;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
}

export async function logout(): Promise<void> {
  try {
    const csrfToken = getCsrfToken();
    const headers: Record<string, string> = addAuthHeaders();
    
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }
    
    const response = await fetch(`${API_BASE_URL}/users/logout/`, {
      method: 'POST',
      headers: headers,
      credentials: 'include',
    });
    
    // Clear the auth token regardless of the response
    setAuthToken(null);
    
    return handleResponse(response);
  } catch (error) {
    // Still clear the token on error
    setAuthToken(null);
    throw error;
  }
}

// User profile endpoints
export async function getProfile(): Promise<User> {
  try {
    const response = await fetch(`${API_BASE_URL}/users/profile/`, {
      headers: addAuthHeaders(),
      credentials: 'include',
    });
    
    if (!response.ok) {
      console.error('Failed to get profile:', response.status);
      throw new Error(`Failed to get profile: ${response.status}`);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error fetching profile:', error);
    throw error;
  }
}

export async function updateProfile(userData: any): Promise<User> {
  try {
    console.log('Updating profile with data:', userData);
    const response = await fetch(`${API_BASE_URL}/users/profile_update/`, {
      method: 'PATCH',
      headers: addAuthHeaders({ 'Content-Type': 'application/json' }),
      credentials: 'include',
      body: JSON.stringify(userData),
    });
    
    if (!response.ok) {
      console.error('Failed to update profile:', response.status);
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        // Ignore JSON parsing error
      }
      
      throw new Error(
        errorData && errorData.error 
          ? errorData.error 
          : `Failed to update profile: ${response.status}`
      );
    }
    
    const data = await response.json();
    console.log('Profile updated successfully:', data);
    return data;
  } catch (error) {
    console.error('Error updating profile:', error);
    throw error;
  }
}

export async function changePassword(currentPassword: string, newPassword: string): Promise<void> {
  try {
    console.log('Changing password');
    const response = await fetch(`${API_BASE_URL}/users/change_password/`, {
      method: 'POST',
      headers: addAuthHeaders({ 'Content-Type': 'application/json' }),
      credentials: 'include',
      body: JSON.stringify({ 
        current_password: currentPassword, 
        new_password: newPassword 
      }),
    });
    
    if (!response.ok) {
      console.error('Failed to change password:', response.status);
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        // Ignore JSON parsing error
      }
      
      throw new Error(
        errorData && errorData.error 
          ? errorData.error 
          : `Failed to change password: ${response.status}`
      );
    }
    
    const data = await response.json();
    console.log('Password changed successfully');
    
    // Update token if provided in response
    if (data && data.token) {
      setAuthToken(data.token);
      console.log('Updated auth token after password change');
    }
    
    return data;
  } catch (error) {
    console.error('Error changing password:', error);
    throw error;
  }
}

// Resume endpoints
export async function uploadResume(file: File): Promise<Resume> {
  try {
    const formData = new FormData();
    formData.append('file', file);

    console.log('Uploading resume with auth token');
    
    const csrfToken = getCsrfToken();
    const headers: Record<string, string> = addAuthHeaders();
    
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }
    
    const response = await fetch(`${API_BASE_URL}/resumes/`, {
      method: 'POST',
      headers: headers,
      credentials: 'include',
      body: formData,
    });
    
    if (!response.ok) {
      console.error('Resume upload failed with status:', response.status);
      let errorText = `HTTP error ${response.status}`;
      
      try {
        const errorData = await response.json();
        console.error('Error data:', errorData);
        errorText = JSON.stringify(errorData);
      } catch (e) {
        console.error('Failed to parse error response:', e);
      }
      
      throw new Error(errorText);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error uploading resume:', error);
    throw error;
  }
}

export async function getResumes(): Promise<Resume[]> {
  const response = await fetch(`${API_BASE_URL}/resumes/`, {
    headers: addAuthHeaders(),
    credentials: 'include',
  });
  return handleResponse(response);
}

export async function deleteResume(resumeId: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}/`, {
    method: 'DELETE',
    headers: addAuthHeaders(),
    credentials: 'include',
  });
  return handleResponse(response);
}

// Job endpoints
export async function getJobs(query?: string): Promise<Job[]> {
  const url = new URL(`${API_BASE_URL}/jobs/`);
  if (query) {
    url.searchParams.append('q', query);
  }
  
  const response = await fetch(url.toString(), {
    headers: addAuthHeaders(),
    credentials: 'include',
  });
  return handleResponse(response);
}

export async function getJobMatches(resumeId: number): Promise<JobMatch[]> {
  try {
    console.log(`Getting job matches for resume ${resumeId}`);
    const response = await fetch(`${API_BASE_URL}/jobs/matches/?resume_id=${resumeId}`, {
      headers: addAuthHeaders(),
      credentials: 'include',
    });
    
    if (!response.ok) {
      console.error('Job matches request failed with status:', response.status);
      let errorText = `HTTP error ${response.status}`;
      
      try {
        const errorData = await response.json();
        console.error('Error data:', errorData);
        errorText = JSON.stringify(errorData);
      } catch (e) {
        console.error('Failed to parse error response:', e);
      }
      
      throw new Error(errorText);
    }
    
    const matches = await response.json();
    console.log(`Found ${matches.length} job matches`);
    return matches;
  } catch (error) {
    console.error('Error getting job matches:', error);
    return [];  // Return empty array on error instead of throwing
  }
}

// Bookmark endpoints
export async function getBookmarks(): Promise<Bookmark[]> {
  const response = await fetch(`${API_BASE_URL}/bookmarks/`, {
    headers: addAuthHeaders(),
    credentials: 'include',
  });
  return handleResponse(response);
}

export async function addBookmark(jobId: number): Promise<Bookmark> {
  const response = await fetch(`${API_BASE_URL}/bookmarks/`, {
    method: 'POST',
    headers: addAuthHeaders({ 'Content-Type': 'application/json' }),
    credentials: 'include',
    body: JSON.stringify({ job_id: jobId }),
  });
  return handleResponse(response);
}

export async function removeBookmark(jobId: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/bookmarks/${jobId}/`, {
    method: 'DELETE',
    headers: addAuthHeaders(),
    credentials: 'include',
  });
  return handleResponse(response);
}

// Application endpoints
export async function getApplications(): Promise<Application[]> {
  const response = await fetch(`${API_BASE_URL}/applications/`, {
    headers: addAuthHeaders(),
    credentials: 'include',
  });
  return handleResponse(response);
}

export async function createApplication(data: {
  jobId: number;
  resumeId: number;
}): Promise<Application> {
  const response = await fetch(`${API_BASE_URL}/applications/`, {
    method: 'POST',
    headers: addAuthHeaders({ 'Content-Type': 'application/json' }),
    credentials: 'include',
    body: JSON.stringify(data),
  });
  return handleResponse(response);
}

export async function updateApplication(
  applicationId: number,
  data: Partial<Application>
): Promise<Application> {
  const response = await fetch(`${API_BASE_URL}/applications/${applicationId}/`, {
    method: 'PATCH',
    headers: addAuthHeaders({ 'Content-Type': 'application/json' }),
    credentials: 'include',
    body: JSON.stringify(data),
  });
  return handleResponse(response);
}

export async function deleteApplication(applicationId: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/applications/${applicationId}/`, {
    method: 'DELETE',
    headers: addAuthHeaders(),
    credentials: 'include',
  });
  return handleResponse(response);
}

// Error handling wrapper
export function withErrorHandling<T>(promise: Promise<T>): Promise<T> {
  return promise.catch((error) => {
    console.error('API Error:', error);
    throw error;
  });
} 