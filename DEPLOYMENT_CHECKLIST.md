# SmartCVMatch Deployment Checklist

Use this checklist to ensure a successful deployment of your SmartCVMatch application to Vercel.

## Pre-Deployment Preparation

### Backend Preparation
- [ ] Ensure `requirements.txt` is up to date with all dependencies
- [ ] Verify `vercel.json` is properly configured
- [ ] Check `settings.py` for proper production settings
- [ ] Make sure `DEBUG = False` in production
- [ ] Ensure database settings are configured to use environment variables
- [ ] Verify CORS settings allow your frontend domain
- [ ] Test locally with production settings

### Frontend Preparation
- [ ] Run `npm run build` locally to ensure it builds successfully
- [ ] Verify API URL configuration in `src/services/api.ts`
- [ ] Check `vercel.json` is properly configured
- [ ] Ensure all dependencies are in `package.json`
- [ ] Test locally with production API URL

## Database Setup
- [ ] Create PostgreSQL database on Vercel or external provider
- [ ] Note down connection details (host, username, password, database name)
- [ ] Test connection to database

## Deployment Process

### Backend Deployment
- [ ] Create new project on Vercel
- [ ] Connect to your Git repository
- [ ] Set root directory to `backend`
- [ ] Set environment variables:
  - [ ] `SECRET_KEY`
  - [ ] `DEBUG=False`
  - [ ] `ALLOWED_HOSTS`
  - [ ] `POSTGRES_NAME`
  - [ ] `POSTGRES_USER`
  - [ ] `POSTGRES_PASSWORD`
  - [ ] `POSTGRES_HOST`
  - [ ] `POSTGRES_PORT`
  - [ ] `CORS_ALLOWED_ORIGINS`
  - [ ] `CSRF_TRUSTED_ORIGINS`
  - [ ] `SECURE_SSL_REDIRECT=True`
- [ ] Deploy backend
- [ ] Note the deployed URL
- [ ] Run migrations using Vercel CLI

### Frontend Deployment
- [ ] Create new project on Vercel
- [ ] Connect to your Git repository
- [ ] Set root directory to `frontend`
- [ ] Set environment variables:
  - [ ] `VITE_API_URL=https://your-backend-app-name.vercel.app/api`
- [ ] Deploy frontend
- [ ] Note the deployed URL

## Post-Deployment Verification

### Backend Verification
- [ ] Visit backend URL to ensure it's running
- [ ] Check Vercel logs for any errors
- [ ] Verify database connection is working
- [ ] Test API endpoints using a tool like Postman

### Frontend Verification
- [ ] Visit frontend URL to ensure it loads
- [ ] Test user registration and login
- [ ] Test resume upload functionality
- [ ] Test job matching functionality
- [ ] Check browser console for any errors

### Integration Verification
- [ ] Ensure frontend can communicate with backend
- [ ] Test end-to-end user flow
- [ ] Verify CORS is properly configured
- [ ] Check authentication is working

## Final Steps
- [ ] Update backend CORS settings to include actual frontend URL
- [ ] Create admin user if needed
- [ ] Set up monitoring (optional)
- [ ] Configure custom domain (optional)
- [ ] Set up SSL certificate (automatic with Vercel)

## Troubleshooting Common Issues
- [ ] Check Vercel deployment logs for errors
- [ ] Verify environment variables are set correctly
- [ ] Ensure database migrations have run successfully
- [ ] Check CORS configuration if API requests fail
- [ ] Verify API URL in frontend is correct
- [ ] Check browser console for JavaScript errors

## Maintenance Plan
- [ ] Set up regular database backups
- [ ] Monitor database size and performance
- [ ] Plan for future updates and feature additions
- [ ] Document deployment process for team members 