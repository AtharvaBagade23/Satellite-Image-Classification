#!/usr/bin/env python3
"""
Deployment helper script for Satellite Image Processor
This script helps you prepare your Django app for deployment.
"""

import os
import secrets
import string
from pathlib import Path

def generate_secret_key():
    """Generate a secure Django secret key"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50))

def create_env_file():
    """Create a .env file with deployment settings"""
    env_content = f"""# Django Settings
SECRET_KEY={generate_secret_key()}
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - will use SQLite if not set)
# DATABASE_URL=postgresql://user:password@host:port/database

# Additional settings
# STATIC_URL=/static/
# MEDIA_URL=/media/
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with deployment settings")
    print("⚠️  Remember to add .env to your .gitignore file!")

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'build.sh',
        'manage.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required deployment files found")
        return True

def check_settings():
    """Check if settings.py is properly configured for production"""
    settings_path = Path('Processor/settings.py')
    if not settings_path.exists():
        print("❌ settings.py not found")
        return False
    
    with open(settings_path, 'r') as f:
        content = f.read()
    
    checks = [
        ('SECRET_KEY', 'os.environ.get' in content),
        ('DEBUG', 'os.environ.get' in content),
        ('ALLOWED_HOSTS', 'os.environ.get' in content),
        ('WhiteNoise', 'whitenoise' in content),
        ('dj_database_url', 'dj_database_url' in content),
    ]
    
    all_good = True
    for check_name, passed in checks:
        if passed:
            print(f"✅ {check_name} configured for production")
        else:
            print(f"❌ {check_name} needs production configuration")
            all_good = False
    
    return all_good

def main():
    print("🚀 Satellite Image Processor - Deployment Setup")
    print("=" * 50)
    
    # Check current directory
    if not Path('manage.py').exists():
        print("❌ Please run this script from the Django project root directory")
        return
    
    print("\n1. Checking deployment files...")
    if not check_requirements():
        print("\n❌ Please ensure all required files are present before deploying")
        return
    
    print("\n2. Checking production settings...")
    if not check_settings():
        print("\n❌ Please update settings.py for production deployment")
        return
    
    print("\n3. Creating environment file...")
    create_env_file()
    
    print("\n🎉 Deployment setup complete!")
    print("\nNext steps:")
    print("1. Push your code to GitHub")
    print("2. Choose a deployment platform (Railway, Render, Heroku, etc.)")
    print("3. Follow the instructions in DEPLOYMENT_GUIDE.md")
    print("4. Set the environment variables in your deployment platform")
    print("5. Deploy!")
    
    print("\n💡 Recommended platforms:")
    print("   - Railway (easiest, good free tier)")
    print("   - Render (good free tier)")
    print("   - Heroku (classic choice)")
    print("   - DigitalOcean App Platform")

if __name__ == "__main__":
    main() 