# SmartCVMatch Deployment Guide

This guide provides instructions for deploying the SmartCVMatch application to Heroku.

## Prerequisites

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- [Git](https://git-scm.com/) installed
- A [Heroku](https://www.heroku.com/) account

## Backend Deployment

1. **Login to Heroku CLI**

```bash
heroku login
```

2. **Create a new Heroku app for the backend**

```bash
cd backend
heroku create smartcvmatch-backend
```

3. **Add PostgreSQL add-on**

```bash
heroku addons:create heroku-postgresql:mini -a smartcvmatch-backend
```

4. **Configure environment variables**

```bash
heroku config:set SECRET_KEY="your-secure-secret-key" -a smartcvmatch-backend
heroku config:set DEBUG=False -a smartcvmatch-backend
heroku config:set ALLOWED_HOSTS=smartcvmatch-backend.herokuapp.com -a smartcvmatch-backend
heroku config:set CORS_ALLOWED_ORIGINS=https://smartcvmatch-frontend.herokuapp.com -a smartcvmatch-backend
heroku config:set CSRF_TRUSTED_ORIGINS=https://smartcvmatch-frontend.herokuapp.com -a smartcvmatch-backend
```

5. **Deploy the backend**

```bash
git subtree push --prefix backend heroku main
```

6. **Run migrations and create a superuser**

```bash
heroku run python manage.py migrate -a smartcvmatch-backend
heroku run python manage.py createsuperuser -a smartcvmatch-backend
heroku run python nltk_download.py -a smartcvmatch-backend
```

## Frontend Deployment

1. **Create a new Heroku app for the frontend**

```bash
cd ../frontend
heroku create smartcvmatch-frontend
```

2. **Add the Heroku buildpack for static sites**

```bash
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-static.git -a smartcvmatch-frontend
```

3. **Configure environment variables**

Create a `.env.production` file in the frontend directory with:

```
VITE_API_URL=https://smartcvmatch-backend.herokuapp.com/api
```

4. **Build the frontend**

```bash
npm install
npm run build
```

5. **Deploy the frontend**

```bash
git subtree push --prefix frontend heroku main
```

## Alternative Deployment Options

### Option 2: Deploy to Render

#### Backend

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure as:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && gunicorn core.wsgi --log-file -`
4. Add environment variables similar to Heroku setup

#### Frontend

1. Create a new Static Site on Render
2. Connect your GitHub repository
3. Configure as:
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`
4. Add environment variables similar to Heroku setup

### Option 3: Deploy to Netlify and Railway

#### Backend (Railway)

1. Create a new project on Railway
2. Connect your GitHub repository
3. Set the root directory to `/backend`
4. Add PostgreSQL plugin
5. Configure environment variables

#### Frontend (Netlify)

1. Connect your GitHub repository to Netlify
2. Set build settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`
3. Configure environment variables

## Troubleshooting

### Common Issues

1. **CORS errors**: Ensure CORS_ALLOWED_ORIGINS includes your frontend URL
2. **Database connection issues**: Check DATABASE_URL is correctly set
3. **Static files not loading**: Verify STATIC_ROOT and STATICFILES_STORAGE settings

### Logs

To view logs:

```bash
# Backend logs
heroku logs --tail -a smartcvmatch-backend

# Frontend logs
heroku logs --tail -a smartcvmatch-frontend
``` 