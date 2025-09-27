#!/usr/bin/env python3
"""
Advanced API Development - Universal Launcher
This script provides a cross-platform way to start the server and test the API.
"""

import os
import sys
import platform
import subprocess
import webbrowser
import time
import threading

def print_banner():
    """Print launcher banner"""
    print("🚀 Advanced API Development - Universal Launcher")
    print("=" * 55)

def check_venv():
    """Check if virtual environment exists and is activated"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
        return True
    else:
        print("⚠️  Virtual environment not detected")
        print("   Make sure to activate your virtual environment first:")
        if platform.system().lower() == "windows":
            print("   venv\\Scripts\\activate.bat")
        else:
            print("   source venv/bin/activate")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import django
        import rest_framework
        print("✅ Django and DRF are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_database():
    """Check if database is set up"""
    try:
        from django.core.management import execute_from_command_line
        from django.conf import settings
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
        import django
        django.setup()
        
        from api.models import Author, Book
        author_count = Author.objects.count()
        book_count = Book.objects.count()
        
        print(f"✅ Database is set up (Authors: {author_count}, Books: {book_count})")
        return True
    except Exception as e:
        print(f"❌ Database issue: {e}")
        print("   Run: python manage.py migrate")
        return False

def start_server():
    """Start the Django development server"""
    print("\n🌐 Starting Django development server...")
    print("   Server will be available at: http://127.0.0.1:8000")
    print("   Press Ctrl+C to stop the server")
    print("")
    
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", "127.0.0.1:8000"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def test_api():
    """Test the API endpoints"""
    print("\n🧪 Testing API endpoints...")
    
    import requests
    import json
    
    base_url = "http://127.0.0.1:8000/api"
    
    endpoints = [
        ("/", "API Root"),
        ("/authors/", "Authors List"),
        ("/books/", "Books List"),
        ("/statistics/", "Statistics"),
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: OK")
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {name}: Connection failed - {e}")

def open_browser():
    """Open browser to the API root"""
    time.sleep(2)  # Wait for server to start
    try:
        webbrowser.open("http://127.0.0.1:8000/api/")
        print("🌐 Opening browser to API root...")
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")

def show_menu():
    """Show the main menu"""
    print("\n📋 Available Options:")
    print("1. Start server")
    print("2. Test API (requires server running)")
    print("3. Start server and open browser")
    print("4. Run tests")
    print("5. Create sample data")
    print("6. Exit")
    print("")

def run_tests():
    """Run Django tests"""
    print("\n🧪 Running Django tests...")
    try:
        subprocess.run([sys.executable, "manage.py", "test", "api"])
    except Exception as e:
        print(f"❌ Error running tests: {e}")

def create_sample_data():
    """Create sample data"""
    print("\n📚 Creating sample data...")
    try:
        subprocess.run([sys.executable, "create_sample_data.py"])
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")

def main():
    """Main launcher function"""
    print_banner()
    
    # Check prerequisites
    if not check_venv():
        return
    
    if not check_dependencies():
        return
    
    if not check_database():
        return
    
    print("\n✅ All checks passed! Ready to launch.")
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                start_server()
            elif choice == "2":
                test_api()
            elif choice == "3":
                # Start server in background and open browser
                server_thread = threading.Thread(target=start_server)
                server_thread.daemon = True
                server_thread.start()
                open_browser()
                server_thread.join()
            elif choice == "4":
                run_tests()
            elif choice == "5":
                create_sample_data()
            elif choice == "6":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)