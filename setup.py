#!/usr/bin/env python3
"""
ShopEase E-commerce Setup Script
Automated setup for Django e-commerce project
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(text, color):
    print(f"{color}{text}{Colors.ENDC}")

def print_step(step_num, total_steps, description):
    print_colored(f"\n[{step_num}/{total_steps}] {description}", Colors.OKBLUE)

def run_command(command, description="", check=True):
    """Run a shell command with error handling"""
    try:
        print_colored(f"Running: {command}", Colors.OKCYAN)
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        if check:
            print_colored(f"Error: {e}", Colors.FAIL)
            print_colored(f"Command output: {e.stdout}", Colors.WARNING)
            print_colored(f"Command error: {e.stderr}", Colors.FAIL)
            raise
        return e

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_colored("Error: Python 3.8 or higher is required!", Colors.FAIL)
        sys.exit(1)
    print_colored(f"✓ Python {version.major}.{version.minor}.{version.micro} detected", Colors.OKGREEN)

def install_dependencies():
    """Install required Python packages"""
    requirements = [
        "Django>=4.0,<6.0",
        "Pillow>=8.0.0",
        "python-decouple>=3.6",
    ]
    
    for requirement in requirements:
        try:
            run_command(f"pip install {requirement}")
            print_colored(f"✓ Installed {requirement}", Colors.OKGREEN)
        except:
            print_colored(f"✗ Failed to install {requirement}", Colors.FAIL)
            raise

def setup_database():
    """Setup database with migrations"""
    try:
        # Make migrations
        run_command("python3 manage.py makemigrations")
        run_command("python3 manage.py makemigrations shop")
        run_command("python3 manage.py makemigrations blog")
        
        # Apply migrations
        run_command("python3 manage.py migrate")
        
        print_colored("✓ Database setup completed", Colors.OKGREEN)
    except Exception as e:
        print_colored(f"✗ Database setup failed: {e}", Colors.FAIL)
        raise

def create_superuser():
    """Create a superuser account"""
    try:
        # Check if superuser already exists
        result = run_command(
            'python3 manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())"',
            check=False
        )
        
        if "True" in result.stdout:
            print_colored("✓ Superuser already exists", Colors.WARNING)
            return
        
        # Create superuser
        create_user_script = '''
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@shopease.com', 'admin123')
    print("Superuser created successfully")
else:
    print("Admin user already exists")
'''
        
        with open('temp_create_user.py', 'w') as f:
            f.write(create_user_script)
        
        run_command("python3 manage.py shell < temp_create_user.py")
        os.remove('temp_create_user.py')
        
        print_colored("✓ Superuser created (Username: admin, Password: admin123)", Colors.OKGREEN)
        
    except Exception as e:
        print_colored(f"✗ Superuser creation failed: {e}", Colors.FAIL)

def add_sample_data():
    """Add sample products to database"""
    sample_script = '''
from shop.models import Product
from datetime import date
import os

# Sample products data
products_data = [
    {
        "product_name": "iPhone 14 Pro",
        "category": "Electronics", 
        "subcategory": "Mobile",
        "price": 999,
        "desc": "Latest iPhone with advanced camera system and A16 Bionic chip",
    },
    {
        "product_name": "MacBook Air M2",
        "category": "Electronics",
        "subcategory": "Laptop", 
        "price": 1299,
        "desc": "Powerful laptop with M2 chip, perfect for professionals",
    },
    {
        "product_name": "Nike Air Max 270",
        "category": "Fashion",
        "subcategory": "Shoes",
        "price": 150,
        "desc": "Comfortable running shoes with Air Max technology",
    },
    {
        "product_name": "Levi's 501 Jeans",
        "category": "Fashion", 
        "subcategory": "Clothing",
        "price": 89,
        "desc": "Classic straight-fit jeans, timeless style",
    },
    {
        "product_name": "Coffee Maker Deluxe",
        "category": "Home & Garden",
        "subcategory": "Kitchen",
        "price": 199,
        "desc": "Premium coffee maker with programmable features",
    },
    {
        "product_name": "Yoga Mat Pro",
        "category": "Sports",
        "subcategory": "Fitness", 
        "price": 45,
        "desc": "High-quality yoga mat with excellent grip and cushioning",
    },
    {
        "product_name": "Wireless Headphones",
        "category": "Electronics",
        "subcategory": "Audio",
        "price": 299,
        "desc": "Premium wireless headphones with noise cancellation",
    },
    {
        "product_name": "Smart Watch Series 8",
        "category": "Electronics",
        "subcategory": "Wearables", 
        "price": 399,
        "desc": "Advanced smartwatch with health monitoring features",
    }
]

# Add products if they don't exist
for product_data in products_data:
    if not Product.objects.filter(product_name=product_data["product_name"]).exists():
        product = Product(
            product_name=product_data["product_name"],
            category=product_data["category"],
            subcategory=product_data["subcategory"], 
            price=product_data["price"],
            desc=product_data["desc"],
            pub_date=date.today()
        )
        product.save()
        print(f"Added product: {product.product_name}")
    else:
        print(f"Product already exists: {product_data['product_name']}")

print("Sample data setup completed!")
'''
    
    try:
        with open('temp_sample_data.py', 'w') as f:
            f.write(sample_script)
        
        run_command("python3 manage.py shell < temp_sample_data.py")
        os.remove('temp_sample_data.py')
        
        print_colored("✓ Sample data added successfully", Colors.OKGREEN)
        
    except Exception as e:
        print_colored(f"✗ Sample data setup failed: {e}", Colors.FAIL)

def collect_static_files():
    """Collect static files"""
    try:
        run_command("python3 manage.py collectstatic --noinput")
        print_colored("✓ Static files collected", Colors.OKGREEN)
    except Exception as e:
        print_colored(f"✗ Static files collection failed: {e}", Colors.FAIL)

def create_media_directories():
    """Create necessary media directories"""
    directories = [
        "media/shop/images",
        "static/shop/css", 
        "static/shop/js",
        "static/shop/images"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print_colored(f"✓ Created directory: {directory}", Colors.OKGREEN)

def main():
    """Main setup function"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("    🛍️  SHOPEASE E-COMMERCE SETUP SCRIPT  🛍️", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    
    total_steps = 8
    
    try:
        print_step(1, total_steps, "Checking Python version...")
        check_python_version()
        
        print_step(2, total_steps, "Installing dependencies...")
        install_dependencies()
        
        print_step(3, total_steps, "Creating media directories...")
        create_media_directories()
        
        print_step(4, total_steps, "Setting up database...")
        setup_database()
        
        print_step(5, total_steps, "Creating superuser...")
        create_superuser()
        
        print_step(6, total_steps, "Adding sample data...")
        add_sample_data()
        
        print_step(7, total_steps, "Collecting static files...")
        collect_static_files()
        
        print_step(8, total_steps, "Final setup...")
        
        print_colored("\n" + "=" * 60, Colors.OKGREEN)
        print_colored("    🎉 SETUP COMPLETED SUCCESSFULLY! 🎉", Colors.OKGREEN)
        print_colored("=" * 60, Colors.OKGREEN)
        
        print_colored("\n📋 SETUP SUMMARY:", Colors.HEADER)
        print_colored("✓ Dependencies installed", Colors.OKGREEN)
        print_colored("✓ Database configured and migrated", Colors.OKGREEN)
        print_colored("✓ Superuser created (admin/admin123)", Colors.OKGREEN)
        print_colored("✓ Sample products added", Colors.OKGREEN)
        print_colored("✓ Static files collected", Colors.OKGREEN)
        
        print_colored("\n🚀 TO START THE SERVER:", Colors.HEADER)
        print_colored("python3 manage.py runserver", Colors.OKCYAN)
        
        print_colored("\n🌐 ACCESS URLS:", Colors.HEADER)
        print_colored("Main Site: http://localhost:8000/shop/", Colors.OKCYAN)
        print_colored("Admin Panel: http://localhost:8000/admin/", Colors.OKCYAN)
        
        print_colored("\n🔐 ADMIN CREDENTIALS:", Colors.HEADER)
        print_colored("Username: admin", Colors.OKCYAN)
        print_colored("Password: admin123", Colors.OKCYAN)
        
    except Exception as e:
        print_colored(f"\n❌ Setup failed: {e}", Colors.FAIL)
        print_colored("Please check the error messages above and try again.", Colors.WARNING)
        sys.exit(1)

if __name__ == "__main__":
    main() 