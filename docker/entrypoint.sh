#!/bin/bash

# ==============================================================================
# ShopEase E-commerce Platform - Production Entrypoint Script
# Handles application initialization, migrations, and startup
# ==============================================================================

set -euo pipefail  # Exit on error, undefined variables, and pipe failures

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to wait for database
wait_for_db() {
    log_info "Waiting for database connection..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if python manage.py check --database default > /dev/null 2>&1; then
            log_success "Database connection established"
            return 0
        else
            log_warning "Database not ready, attempt $attempt/$max_attempts"
            sleep 2
            ((attempt++))
        fi
    done
    
    log_error "Database connection failed after $max_attempts attempts"
    exit 1
}

# Function to run database migrations
run_migrations() {
    log_info "Running database migrations..."
    
    if python manage.py migrate --noinput; then
        log_success "Database migrations completed"
    else
        log_error "Database migrations failed"
        exit 1
    fi
}

# Function to collect static files
collect_static() {
    log_info "Collecting static files..."
    
    if python manage.py collectstatic --noinput --clear; then
        log_success "Static files collected"
    else
        log_error "Static file collection failed"
        exit 1
    fi
}

# Function to create superuser if it doesn't exist
create_superuser() {
    log_info "Checking for superuser..."
    
    python manage.py shell << EOF
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@shopease.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully")
else:
    print(f"Superuser '{username}' already exists")
EOF
    
    log_success "Superuser check completed"
}

# Function to load sample data
load_sample_data() {
    if [ "${LOAD_SAMPLE_DATA:-false}" = "true" ]; then
        log_info "Loading sample data..."
        
        python manage.py shell << 'EOF'
from shop.models import Product
from datetime import date

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
        "product_name": "Coffee Maker Deluxe",
        "category": "Home & Garden",
        "subcategory": "Kitchen",
        "price": 199,
        "desc": "Premium coffee maker with programmable features",
    },
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

print("Sample data loading completed!")
EOF
        
        log_success "Sample data loaded"
    fi
}

# Function to setup directories and permissions
setup_directories() {
    log_info "Setting up directories and permissions..."
    
    # Ensure directories exist
    mkdir -p /app/staticfiles /app/media /var/log/shopease /var/run/shopease
    
    # Set proper permissions (if running as root, which we shouldn't in production)
    if [ "$(id -u)" = "0" ]; then
        chown -R shopease:shopease /app/staticfiles /app/media /var/log/shopease /var/run/shopease
    fi
    
    log_success "Directories and permissions set up"
}

# Function to validate environment
validate_environment() {
    log_info "Validating environment configuration..."
    
    # Check required environment variables
    local required_vars=("DJANGO_SETTINGS_MODULE")
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var:-}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        log_error "Missing required environment variables: ${missing_vars[*]}"
        exit 1
    fi
    
    # Validate Django configuration
    if ! python manage.py check --deploy > /dev/null 2>&1; then
        log_warning "Django deployment checks failed. Check your configuration."
    fi
    
    log_success "Environment validation completed"
}

# Function to start services based on the command
start_services() {
    local cmd="$1"
    
    case "$cmd" in
        "web"|"gunicorn")
            log_info "Starting Gunicorn web server..."
            exec gunicorn mac.wsgi:application -c /app/gunicorn.conf.py
            ;;
        "worker"|"celery")
            log_info "Starting Celery worker..."
            exec celery -A mac worker -l info
            ;;
        "beat"|"celery-beat")
            log_info "Starting Celery beat scheduler..."
            exec celery -A mac beat -l info
            ;;
        "flower")
            log_info "Starting Flower monitoring..."
            exec celery -A mac flower
            ;;
        "migrate")
            log_info "Running migrations only..."
            run_migrations
            exit 0
            ;;
        "collectstatic")
            log_info "Collecting static files only..."
            collect_static
            exit 0
            ;;
        "shell")
            log_info "Starting Django shell..."
            exec python manage.py shell
            ;;
        "bash")
            log_info "Starting bash shell..."
            exec /bin/bash
            ;;
        *)
            log_info "Starting with custom command: $*"
            exec "$@"
            ;;
    esac
}

# Main execution flow
main() {
    log_info "=== ShopEase E-commerce Platform Starting ==="
    log_info "Container started at $(date)"
    
    # Setup
    setup_directories
    validate_environment
    
    # Database operations (skip for worker processes)
    if [[ "$1" != "worker" && "$1" != "celery" && "$1" != "beat" && "$1" != "celery-beat" && "$1" != "flower" ]]; then
        wait_for_db
        run_migrations
        collect_static
        create_superuser
        load_sample_data
    fi
    
    # Start the requested service
    start_services "$@"
}

# Trap signals for graceful shutdown
trap 'log_info "Received shutdown signal, exiting..."; exit 0' TERM INT

# Run main function with all arguments
main "$@" 