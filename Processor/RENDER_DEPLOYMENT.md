# Deploy to Render 🚀

Render is an excellent platform for Django applications with great free tier support and easy deployment.

## Prerequisites

1. **GitHub Repository**: Your code must be on GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)

## Step 1: Prepare Your Repository

Make sure your code is pushed to GitHub:

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

## Step 2: Create a Render Web Service

1. **Go to [render.com](https://render.com)** and sign up/login
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**:
   - Click "Connect a repository"
   - Authorize Render to access your GitHub
   - Select your repository

## Step 3: Configure the Web Service

Fill in these settings:

### Basic Settings:
- **Name**: `satellite-image-processor` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`

### Build & Deploy Settings:
- **Build Command**: 
  ```
  pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
  ```
- **Start Command**: 
  ```
  gunicorn Processor.wsgi:application
  ```

### Environment Variables:
Click "Advanced" → "Add Environment Variable" and add:

```
SECRET_KEY=your-secret-key-from-.env-file
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

## Step 4: Deploy

1. **Click "Create Web Service"**
2. **Wait for deployment** (usually 5-10 minutes)
3. **Your app will be live** at `https://your-app-name.onrender.com`

## Step 5: Add Database (Optional but Recommended)

1. **In your Render dashboard**, click **"New +"** → **"PostgreSQL"**
2. **Configure the database**:
   - Name: `satellite-processor-db`
   - Database: `satellite_processor`
   - User: `satellite_user`
3. **Click "Create Database"**
4. **Connect to your web service**:
   - Go back to your web service
   - Click "Environment" tab
   - Add environment variable:
     ```
     DATABASE_URL=postgresql://satellite_user:password@host:port/satellite_processor
     ```
   - (Render will provide the actual URL)

## Step 6: Test Your App

1. **Visit your app URL**
2. **Test file upload** with a TIFF file
3. **Verify NDVI and water analysis** works
4. **Check statistics page**

## Render-Specific Features

### Auto-Deploy
- Render automatically deploys when you push to GitHub
- No manual deployment needed

### Free Tier Limits
- **512 MB RAM**
- **Shared CPU**
- **750 hours/month** (enough for 24/7 operation)
- **Sleep after 15 minutes** of inactivity (wakes up on first request)

### Custom Domains
1. **Go to your web service settings**
2. **Click "Custom Domains"**
3. **Add your domain** and configure DNS

## Environment Variables Reference

```bash
# Required
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com

# Optional (for database)
DATABASE_URL=postgresql://user:password@host:port/database

# Optional (for custom domain)
ALLOWED_HOSTS=your-domain.com,your-app-name.onrender.com
```

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version in `runtime.txt`

### App Not Loading
- Check if `ALLOWED_HOSTS` includes your Render domain
- Verify environment variables are set correctly
- Check application logs

### Database Issues
- Ensure `DATABASE_URL` is set correctly
- Run migrations: `python manage.py migrate`
- Check database connection in logs

### File Upload Issues
- Render supports file uploads
- Files are stored in the container (temporary)
- Consider using cloud storage (AWS S3) for production

### Performance Issues
- Upgrade to paid plan for better performance
- Consider using Redis for caching
- Optimize database queries

## Monitoring

### Logs
- View logs in Render dashboard
- Real-time log streaming available
- Log retention for debugging

### Metrics
- CPU and memory usage
- Request count and response times
- Error rates

## Scaling

### Free to Paid
- **Free**: 512 MB RAM, shared CPU
- **Paid**: Up to 32 GB RAM, dedicated CPU
- **Auto-scaling**: Available on paid plans

### Database Scaling
- **Free**: 1 GB storage
- **Paid**: Up to 1 TB storage
- **Read replicas**: Available on paid plans

## Security

### HTTPS
- Automatic SSL certificates
- HTTPS redirect enabled by default

### Environment Variables
- Encrypted at rest
- Not visible in logs
- Secure access control

## Best Practices

1. **Use environment variables** for sensitive data
2. **Set DEBUG=False** in production
3. **Use PostgreSQL** for production databases
4. **Monitor logs** regularly
5. **Set up alerts** for errors
6. **Backup database** regularly

## Support

- **Documentation**: [render.com/docs](https://render.com/docs)
- **Community**: [render.com/community](https://render.com/community)
- **Status**: [status.render.com](https://status.render.com)

## Next Steps

After successful deployment:

1. **Test all features** thoroughly
2. **Set up monitoring** and alerts
3. **Configure backups** for database
4. **Add custom domain** if needed
5. **Optimize performance** based on usage
6. **Scale up** when needed

Your satellite image processor will be live and accessible worldwide! 🌍 