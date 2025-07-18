# Deployment Guide for SmartCVMatch on Vercel

This guide will walk you through deploying both the frontend and backend of SmartCVMatch on Vercel.

## Prerequisites

1. A [Vercel](https://vercel.com) account
2. A [PostgreSQL database](https://vercel.com/docs/storage/vercel-postgres) (can be set up through Vercel or externally)
3. Git repository with your code

## Step 1: Prepare the Backend for Deployment

### Environment Variables for Backend

When deploying the backend to Vercel, you'll need to set the following environment variables:

```
# Django settings
SECRET_KEY=your_secure_secret_key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app,your-backend-app-name.vercel.app

# Database settings
POSTGRES_NAME=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=your_db_host
POSTGRES_PORT=5432

# CORS settings
CORS_ALLOWED_ORIGINS=https://smartcvmatch-frontend.vercel.app
CSRF_TRUSTED_ORIGINS=https://smartcvmatch-frontend.vercel.app

# Security settings
SECURE_SSL_REDIRECT=True
```

Replace placeholders with your actual values.

## Step 2: Deploy the Backend to Vercel

1. Log in to your Vercel account
2. Click "Add New" > "Project"
3. Import your Git repository
4. Configure the project:
   - Framework Preset: Other
   - Root Directory: `backend`
   - Build Command: Leave empty (Vercel will use the settings in vercel.json)
   - Output Directory: Leave empty
5. Add the environment variables listed above
6. Click "Deploy"

Once deployed, note the URL of your backend (e.g., `https://smartcvmatch-backend.vercel.app`).

## Step 3: Prepare the Frontend for Deployment

### Environment Variables for Frontend

When deploying the frontend to Vercel, you'll need to set the following environment variable:

```
VITE_API_URL=https://your-backend-app-name.vercel.app/api
```

Replace `your-backend-app-name` with the actual subdomain of your deployed backend.

## Step 4: Deploy the Frontend to Vercel

1. Log in to your Vercel account
2. Click "Add New" > "Project"
3. Import your Git repository
4. Configure the project:
   - Framework Preset: Svelte
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Add the environment variable listed above
6. Click "Deploy"

## Step 5: Connect Frontend and Backend

1. After both deployments are complete, go to your backend project settings in Vercel
2. Update the CORS settings to include your frontend URL:
   ```
   CORS_ALLOWED_ORIGINS=https://your-frontend-app-name.vercel.app
   CSRF_TRUSTED_ORIGINS=https://your-frontend-app-name.vercel.app
   ```
3. Redeploy the backend to apply these changes

## Step 6: Database Initialization

You'll need to run migrations on your deployed backend:

1. Install the Vercel CLI: `npm i -g vercel`
2. Log in: `vercel login`
3. Run: `vercel --cwd backend run python manage.py migrate`

## Step 7: Create a Superuser (Optional)

If you need admin access:

1. Run: `vercel --cwd backend run python manage.py createsuperuser`
2. Follow the prompts to create an admin user

## Step 8: Verify Deployment

1. Visit your frontend URL
2. Test user registration and login
3. Test resume uploads and job matching
4. Test bookmark functionality (once fixed)

## Troubleshooting

### CORS Issues

If you encounter CORS errors:

1. Check that your backend's `CORS_ALLOWED_ORIGINS` includes the full frontend URL
2. Ensure your frontend is using the correct backend URL
3. Verify that the backend's `vercel.json` has the correct CORS headers

### Database Connection Issues

If you encounter database connection issues:

1. Verify your PostgreSQL credentials in the environment variables
2. Check if your database allows connections from Vercel's IP addresses
3. Ensure your database is running and accessible

### Static Files Issues

If static files aren't loading:

1. Verify that `STATIC_ROOT` is set correctly in `settings.py`
2. Ensure Whitenoise is properly configured
3. Check that static files were collected during deployment

## Updating Your Deployed Application

When you push changes to your repository:

1. Vercel will automatically rebuild and redeploy your application
2. The URL will remain the same
3. Users will see the updated version when they refresh the page

This allows you to fix issues (like the bookmark functionality) later without changing the URL you've included in your CV. 