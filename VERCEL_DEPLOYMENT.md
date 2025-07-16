# Deploying SmartCVMatch to Vercel

This guide provides instructions for deploying both the frontend and backend of SmartCVMatch to Vercel, ensuring no sleep time and optimal performance.

## Prerequisites

- [Vercel Account](https://vercel.com/signup) (free tier is sufficient)
- [GitHub Account](https://github.com/) with your repository pushed
- [PostgreSQL Database](https://www.postgresql.org/) (you can use Vercel Postgres, Supabase, or any other PostgreSQL provider)

## Step 1: Deploy the Backend

1. **Log in to Vercel**
   - Go to [Vercel](https://vercel.com/) and log in
   - Connect your GitHub account if you haven't already

2. **Create a new project**
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Select the repository containing your SmartCVMatch project

3. **Configure the backend deployment**
   - Set the root directory to `backend` (or leave blank if your repository only contains the backend)
   - Framework preset: Other
   - Build command: Leave blank (Vercel will use the vercel.json configuration)
   - Output directory: Leave blank

4. **Configure environment variables**
   - Click on "Environment Variables"
   - Add the following variables:
     ```
     SECRET_KEY=your-secure-secret-key
     DEBUG=False
     ALLOWED_HOSTS=.vercel.app
     CORS_ALLOWED_ORIGINS=https://smartcvmatch-frontend.vercel.app
     CSRF_TRUSTED_ORIGINS=https://smartcvmatch-frontend.vercel.app
     ```

5. **Configure database environment variables**
   - Add your PostgreSQL database credentials:
     ```
     POSTGRES_NAME=your_db_name
     POSTGRES_USER=your_db_user
     POSTGRES_PASSWORD=your_db_password
     POSTGRES_HOST=your_db_host
     POSTGRES_PORT=5432
     ```
   - Alternatively, if using a connection string:
     ```
     DATABASE_URL=postgresql://user:password@host:port/dbname
     ```

6. **Deploy**
   - Click "Deploy"
   - Wait for the deployment to complete

7. **Run migrations using Vercel CLI**
   - Install Vercel CLI: `npm i -g vercel`
   - Log in: `vercel login`
   - Run migrations: `vercel run python manage.py migrate`
   - Create superuser: `vercel run python manage.py createsuperuser`
   - Download NLTK data: `vercel run python nltk_download.py`

## Step 2: Deploy the Frontend

1. **Create a new project in Vercel**
   - Click "Add New" → "Project"
   - Import your GitHub repository again
   - This time, set the root directory to `frontend` (if your repository contains both frontend and backend)

2. **Configure the frontend deployment**
   - Framework preset: Vite
   - Build command: `npm run build`
   - Output directory: `dist`

3. **Configure environment variables**
   - Click on "Environment Variables"
   - Add the following variable:
     ```
     VITE_API_URL=https://your-backend-url.vercel.app/api
     ```
   - Replace `your-backend-url` with your actual backend deployment URL

4. **Deploy**
   - Click "Deploy"
   - Wait for the deployment to complete

## Step 3: Verify Deployment

1. **Test the frontend**
   - Visit your frontend URL (e.g., `https://smartcvmatch-frontend.vercel.app`)
   - Ensure the UI loads correctly

2. **Test the backend API**
   - Visit your backend API URL (e.g., `https://smartcvmatch-backend.vercel.app/api`)
   - Verify that the API responds correctly

3. **Test user authentication**
   - Try to register a new user
   - Try to log in with existing credentials

## Troubleshooting

### CORS Issues
- Double-check that the `CORS_ALLOWED_ORIGINS` environment variable includes your frontend URL
- Ensure your frontend is using the correct backend URL

### Database Connection Issues
- Verify your database credentials
- Check if your database provider allows connections from Vercel's IP addresses
- Consider using a connection pooler like PgBouncer for better performance

### Static Files Issues
- Vercel handles static files differently than traditional hosting
- Make sure your frontend build is correctly generating all required assets

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Django on Vercel](https://vercel.com/guides/deploying-django-to-vercel)
- [Vite on Vercel](https://vercel.com/guides/deploying-vite-with-vercel)

## Notes on Serverless Limitations

When deploying Django to Vercel's serverless environment, be aware of these limitations:

1. **Cold starts**: First request after inactivity might be slower
2. **Execution time**: Functions have a 10-second timeout on the free plan
3. **Statelessness**: Each function invocation is stateless, so don't rely on in-memory caching
4. **File system**: The filesystem is read-only except for `/tmp`

For a production application with heavy usage, consider upgrading to a paid plan or using a different hosting solution. 