# Quick Deploy to Railway 🚀

This is the fastest way to get your satellite image processor app online!

## Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

## Step 2: Deploy to Railway

1. **Go to [railway.app](https://railway.app)** and sign up/login
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Connect your GitHub account** (if not already connected)
5. **Select your repository**
6. **Railway will automatically detect Django and deploy!**

## Step 3: Configure Environment Variables

1. In your Railway project dashboard, go to **Variables** tab
2. Add these environment variables:
   ```
   SECRET_KEY=your-secret-key-from-.env-file
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   ```

## Step 4: Your App is Live! 🎉

- Railway will give you a URL like: `https://your-app-name.railway.app`
- Your app is now accessible to anyone on the internet!

## Optional: Add Database

1. In Railway dashboard, click **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway will automatically set the `DATABASE_URL` environment variable
3. Your app will automatically use PostgreSQL instead of SQLite

## Troubleshooting

- **Build fails?** Check the logs in Railway dashboard
- **App not loading?** Make sure `ALLOWED_HOSTS` includes your Railway domain
- **Database errors?** Run `python manage.py migrate` in Railway console

## Next Steps

- Test uploading a TIFF file
- Check that NDVI and water analysis works
- Monitor your app's performance
- Consider upgrading to a paid plan if needed

That's it! Your satellite image processor is now live on the internet! 🌍 