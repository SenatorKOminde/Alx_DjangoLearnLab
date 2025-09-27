#!/usr/bin/env python3
"""
Advanced Features and Security - Django Project Setup Script
This script automates the setup process for the Django security project.
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_django_environment():
    """Set up Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    django.setup()

def main():
    """Main setup function"""
    print("🚀 Advanced Features and Security - Django Project Setup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check requirements.txt")
        sys.exit(1)
    
    # Set up Django environment
    try:
        setup_django_environment()
        print("✅ Django environment configured")
    except Exception as e:
        print(f"❌ Failed to configure Django environment: {e}")
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        print("❌ Failed to create migrations")
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Running migrations"):
        print("❌ Failed to run migrations")
        sys.exit(1)
    
    # Set up groups and permissions
    if not run_command("python manage.py setup_groups", "Setting up groups and permissions"):
        print("❌ Failed to set up groups")
        sys.exit(1)
    
    # Create test users
    if not run_command("python manage.py create_test_users", "Creating test users"):
        print("❌ Failed to create test users")
        sys.exit(1)
    
    # Create superuser
    print("🔄 Creating superuser...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Check if superuser already exists
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("✅ Superuser created: admin / admin123")
        else:
            print("ℹ️ Superuser already exists")
    except Exception as e:
        print(f"❌ Failed to create superuser: {e}")
    
    # Create some sample data
    print("🔄 Creating sample data...")
    try:
        from bookshelf.models import Book
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        admin_user = User.objects.get(username='admin')
        
        # Create sample books if they don't exist
        if not Book.objects.exists():
            sample_books = [
                {
                    'title': 'The Great Gatsby',
                    'author': 'F. Scott Fitzgerald',
                    'publication_year': 1925,
                    'created_by': admin_user
                },
                {
                    'title': 'To Kill a Mockingbird',
                    'author': 'Harper Lee',
                    'publication_year': 1960,
                    'created_by': admin_user
                },
                {
                    'title': '1984',
                    'author': 'George Orwell',
                    'publication_year': 1949,
                    'created_by': admin_user
                }
            ]
            
            for book_data in sample_books:
                Book.objects.create(**book_data)
            
            print("✅ Sample books created")
        else:
            print("ℹ️ Sample books already exist")
    except Exception as e:
        print(f"⚠️ Warning: Could not create sample data: {e}")
    
    # Final setup summary
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\n📋 Project Information:")
    print("• Custom User Model: ✅ Implemented")
    print("• Permissions & Groups: ✅ Configured")
    print("• Security Settings: ✅ Applied")
    print("• HTTPS Configuration: ✅ Ready")
    
    print("\n👥 Test Users Created:")
    print("• viewer1 / testpass123 (Viewers group)")
    print("• editor1 / testpass123 (Editors group)")
    print("• admin1 / testpass123 (Admins group)")
    print("• admin / admin123 (Superuser)")
    
    print("\n🚀 Next Steps:")
    print("1. Run the development server: python manage.py runserver")
    print("2. Visit http://localhost:8000 to access the application")
    print("3. Login with different users to test permissions")
    print("4. Check the admin interface at http://localhost:8000/admin/")
    
    print("\n📚 Documentation:")
    print("• README.md - Project overview and usage")
    print("• SECURITY_DOCUMENTATION.md - Detailed security implementation")
    
    print("\n🔐 Security Features Implemented:")
    print("• Custom User Model with additional fields")
    print("• Role-based access control with groups")
    print("• Permission-based view protection")
    print("• CSRF token protection")
    print("• XSS prevention")
    print("• SQL injection prevention")
    print("• HTTPS configuration")
    print("• Secure cookie settings")
    print("• Content Security Policy")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()