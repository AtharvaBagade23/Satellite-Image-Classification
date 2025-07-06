# Deployment Guide for Satellite Image Processor

This guide will help you deploy your Django satellite image processing application to various cloud platforms.

## Prerequisites

1. **Git Repository**: Make sure your code is in a Git repository
2. **Python 3.11+**: The app requires Python 3.11 or higher
3. **Dependencies**: All required packages are listed in `requirements.txt`

## Option 1: Deploy to Railway (Recommended)

Railway is a modern platform with excellent free tier support.

### Steps:

1. **Sign up** at [railway.app](https://railway.app)

2. **Connect your repository**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select your repository

3. **Configure environment variables**:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   ```

4. **Deploy**: Railway will automatically detect Django and deploy your app

5. **Set up database** (optional):
   - Add PostgreSQL service in Railway
   - Railway will automatically set `DATABASE_URL`

### Railway-specific files:
- `Procfile`: Tells Railway how to run your app
- `requirements.txt`: Lists all Python dependencies
- `runtime.txt`: Specifies Python version

## Option 2: Deploy to Render

Render is another excellent platform with good free tier support.

### Steps:

1. **Sign up** at [render.com](https://render.com)

2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Choose "Python" as the environment

3. **Configure the service**:
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
   - **Start Command**: `gunicorn Processor.wsgi:application`
   - **Environment**: Python 3.11

4. **Set environment variables**:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   ```

5. **Deploy**: Click "Create Web Service"

## Option 3: Deploy to Heroku

### Steps:

1. **Install Heroku CLI** and sign up at [heroku.com](https://heroku.com)

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

5. **Add PostgreSQL** (optional):
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

6. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

7. **Run migrations**:
   ```bash
   heroku run python manage.py migrate
   ```

## Option 4: Deploy to DigitalOcean App Platform

### Steps:

1. **Sign up** at [digitalocean.com](https://digitalocean.com)

2. **Create a new app**:
   - Connect your GitHub repository
   - Choose "Python" as the environment

3. **Configure the app**:
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
   - **Run Command**: `gunicorn Processor.wsgi:application`
   - **Environment**: Python 3.11

4. **Set environment variables**:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.ondigitalocean.app
   ```

5. **Deploy**: Click "Create Resources"

## Environment Variables

Set these environment variables in your deployment platform:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url (optional, will use SQLite if not set)
```

## Generate a Secret Key

You can generate a new secret key using Python:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Important Notes

1. **File Uploads**: Your app handles TIFF file uploads. Make sure your deployment platform supports file uploads and has sufficient storage.

2. **Memory Requirements**: Image processing can be memory-intensive. Consider using a platform with at least 512MB RAM.

3. **Database**: The app will work with SQLite for small deployments, but consider PostgreSQL for production use.

4. **Static Files**: The app uses WhiteNoise to serve static files in production.

5. **Media Files**: Uploaded files are stored in the `media/` directory. For production, consider using cloud storage (AWS S3, etc.).

## Troubleshooting

### Common Issues:

1. **Build fails**: Check that all dependencies are in `requirements.txt`
2. **Static files not loading**: Ensure `python manage.py collectstatic` runs during build
3. **Database errors**: Run migrations with `python manage.py migrate`
4. **Permission errors**: Make sure `build.sh` is executable (`chmod +x build.sh`)

### Debug Mode:

For debugging, temporarily set:
```
DEBUG=True
```

## Next Steps

After deployment:

1. **Test the application**: Upload a TIFF file and verify processing works
2. **Monitor logs**: Check application logs for any errors
3. **Set up monitoring**: Consider adding error tracking (Sentry, etc.)
4. **Scale up**: If needed, upgrade to a paid plan for better performance

## Support

If you encounter issues:
1. Check the platform's documentation
2. Review application logs
3. Test locally with production settings
4. Consider the platform's community forums 