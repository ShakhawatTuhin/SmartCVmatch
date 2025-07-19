# Setting Up PostgreSQL on Vercel

This guide will walk you through setting up a PostgreSQL database for your SmartCVMatch application using Vercel Postgres.

## Step 1: Create a Vercel Postgres Database

1. Log in to your [Vercel dashboard](https://vercel.com/dashboard)
2. Click on the "Storage" tab in the left sidebar
3. Select "Postgres" and click "Create Database"
4. Choose a name for your database (e.g., "smartcvmatch-db")
5. Select the region closest to your users
6. Click "Create"

## Step 2: Get Database Connection Details

1. After your database is created, click on it to view its details
2. Click on the ".env.local" tab to see the connection details
3. You'll see environment variables like:
   ```
   POSTGRES_URL=...
   POSTGRES_PRISMA_URL=...
   POSTGRES_URL_NON_POOLING=...
   POSTGRES_USER=...
   POSTGRES_HOST=...
   POSTGRES_PASSWORD=...
   POSTGRES_DATABASE=...
   ```

## Step 3: Configure Your Backend Project

1. Go to your backend project settings in Vercel
2. Add the following environment variables using the values from Step 2:
   ```
   POSTGRES_NAME=your_database_name
   POSTGRES_USER=your_database_user
   POSTGRES_PASSWORD=your_database_password
   POSTGRES_HOST=your_database_host
   POSTGRES_PORT=5432
   ```
   
   Alternatively, you can use the `DATABASE_URL` format:
   ```
   DATABASE_URL=postgres://user:password@host:port/database
   ```

## Step 4: Initialize Your Database

After deploying your backend, you need to run migrations to set up your database schema:

1. Install the Vercel CLI: `npm i -g vercel`
2. Log in: `vercel login`
3. Run migrations: `vercel --cwd backend run python manage.py migrate`

## Step 5: Verify Database Connection

1. Visit your deployed backend URL to verify it's connecting to the database
2. Check the logs in your Vercel dashboard for any database connection errors

## Database Management

### Viewing Your Data

1. Go to the "Storage" tab in your Vercel dashboard
2. Click on your database
3. Use the "Data" tab to browse and query your tables

### Running SQL Commands

1. Go to the "Storage" tab in your Vercel dashboard
2. Click on your database
3. Use the "Query" tab to run SQL commands

### Connecting with External Tools

You can also connect to your Vercel Postgres database using tools like pgAdmin or DBeaver:

1. Go to the "Storage" tab in your Vercel dashboard
2. Click on your database
3. Click on "Connect" to get connection details
4. Use these details to connect with your preferred database tool

## Important Notes

1. **Connection Limits**: Vercel Postgres has connection limits based on your plan. Be mindful of these limits.
2. **SSL Required**: Vercel Postgres requires SSL connections. Make sure your connection string includes `sslmode=require`.
3. **Backup Regularly**: Set up regular backups of your database to prevent data loss.
4. **Database Size**: Monitor your database size to stay within your plan limits.

## Troubleshooting

### Connection Issues

If you're having trouble connecting to your database:

1. Verify your connection credentials
2. Check if your IP is allowed (Vercel Postgres restricts access by IP)
3. Ensure you're using SSL for the connection
4. Check the Vercel status page for any ongoing issues

### Migration Errors

If you encounter errors when running migrations:

1. Check your database schema for compatibility issues
2. Ensure your migrations are in the correct order
3. Try running migrations one by one to identify the problematic migration 