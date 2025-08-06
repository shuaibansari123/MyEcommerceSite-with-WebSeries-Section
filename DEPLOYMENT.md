# 🚀 ShopEase E-commerce Platform - Production Deployment Guide

This guide covers the production deployment of ShopEase using Docker and Docker Compose with enterprise-level best practices.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Production Deployment](#production-deployment)
- [Environment Configuration](#environment-configuration)
- [SSL Certificate Setup](#ssl-certificate-setup)
- [Monitoring & Logging](#monitoring--logging)
- [Backup & Recovery](#backup--recovery)
- [Scaling](#scaling)
- [Security Hardening](#security-hardening)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04 LTS or higher (recommended)
- **RAM**: Minimum 4GB, Recommended 8GB+
- **CPU**: Minimum 2 cores, Recommended 4+ cores
- **Storage**: Minimum 20GB free space
- **Network**: Static IP address (for production)

### Software Requirements
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- OpenSSL (for SSL certificates)

### Installation Commands
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/shuaibansari123/MyEcommerceSite-with-WebSeries-Section.git
cd MyEcommerceSite-with-WebSeries-Section
```

### 2. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit environment variables
nano .env
```

### 3. Generate SSL Certificates (Self-signed for testing)
```bash
mkdir -p docker/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout docker/ssl/key.pem \
    -out docker/ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=ShopEase/CN=localhost"
```

### 4. Deploy Application
```bash
# Build and start services
docker compose up -d

# Check service status
docker compose ps

# View logs
docker compose logs -f
```

### 5. Access Application
- **Main Site**: https://localhost
- **Admin Panel**: https://localhost/admin
- **Flower (Celery Monitor)**: http://localhost:5555 (with monitoring profile)

## 🏭 Production Deployment

### 1. Server Setup
```bash
# Create application directory
sudo mkdir -p /opt/shopease
sudo chown $USER:$USER /opt/shopease
cd /opt/shopease

# Clone repository
git clone https://github.com/shuaibansari123/MyEcommerceSite-with-WebSeries-Section.git .
```

### 2. Environment Configuration
```bash
# Create production environment file
cp env.example .env

# Edit with production values
sudo nano .env
```

**Critical Environment Variables for Production:**
```env
DEBUG=False
SECRET_KEY=your-super-secure-secret-key-min-50-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_PASSWORD=your-secure-database-password
REDIS_PASSWORD=your-secure-redis-password
DJANGO_SUPERUSER_PASSWORD=your-secure-admin-password
```

### 3. SSL Certificate Setup (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot

# Generate SSL certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates to Docker volume
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem docker/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem docker/ssl/key.pem
sudo chown $USER:$USER docker/ssl/*.pem
```

### 4. Production Deployment
```bash
# Deploy with production profile
docker compose -f docker-compose.yml up -d

# Enable monitoring (optional)
docker compose --profile monitoring up -d

# Verify deployment
docker compose ps
docker compose logs web
```

## 🔐 Environment Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Django debug mode | `False` |
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `ALLOWED_HOSTS` | Allowed host names | `yourdomain.com,www.yourdomain.com` |
| `DB_NAME` | Database name | `shopease` |
| `DB_USER` | Database user | `shopease` |
| `DB_PASSWORD` | Database password | `secure-password` |
| `REDIS_PASSWORD` | Redis password | `secure-redis-password` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOAD_SAMPLE_DATA` | Load sample products | `false` |
| `EMAIL_HOST` | SMTP host | `smtp.gmail.com` |
| `SENTRY_DSN` | Error monitoring | `""` |
| `FLOWER_PASSWORD` | Flower monitoring password | `flower123` |

## 🔒 SSL Certificate Setup

### Option 1: Let's Encrypt (Recommended for Production)
```bash
# Install Certbot
sudo apt install certbot

# Stop nginx temporarily
docker compose stop nginx

# Generate certificate
sudo certbot certonly --standalone \
    -d yourdomain.com \
    -d www.yourdomain.com \
    --email admin@yourdomain.com \
    --agree-tos

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem docker/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem docker/ssl/key.pem
sudo chown $USER:$USER docker/ssl/*.pem

# Restart nginx
docker compose start nginx
```

### Option 2: Self-Signed Certificate (Development/Testing)
```bash
mkdir -p docker/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout docker/ssl/key.pem \
    -out docker/ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=ShopEase/CN=yourdomain.com"
```

### Certificate Auto-Renewal
```bash
# Add to crontab for auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet && docker compose restart nginx" | sudo crontab -
```

## 📊 Monitoring & Logging

### Enable Monitoring Stack
```bash
# Start with monitoring profile
docker compose --profile monitoring up -d

# Access monitoring tools
# Flower: http://localhost:5555
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
```

### Log Management
```bash
# View application logs
docker compose logs -f web

# View nginx logs
docker compose logs -f nginx

# View database logs
docker compose logs -f db

# View all logs
docker compose logs -f
```

### Log Rotation Setup
```bash
# Create logrotate configuration
sudo nano /etc/logrotate.d/docker-shopease

# Add content:
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size 10M
    missingok
    delaycompress
    copytruncate
}
```

## 💾 Backup & Recovery

### Database Backup
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/shopease/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
docker compose exec -T db pg_dump -U shopease shopease > $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz media/

# Keep only last 7 backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

chmod +x backup.sh

# Add to crontab for daily backups
echo "0 2 * * * /opt/shopease/backup.sh" | crontab -
```

### Database Restore
```bash
# Stop application
docker compose stop web worker beat

# Restore database
cat backups/db_backup_YYYYMMDD_HHMMSS.sql | docker compose exec -T db psql -U shopease shopease

# Restore media files
tar -xzf backups/media_backup_YYYYMMDD_HHMMSS.tar.gz

# Start application
docker compose start web worker beat
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale web containers
docker compose up -d --scale web=3

# Scale worker containers
docker compose up -d --scale worker=2
```

### Load Balancer Configuration
Update `docker/nginx/nginx.conf`:
```nginx
upstream shopease_backend {
    least_conn;
    server shopease-web-1:8000 max_fails=3 fail_timeout=30s;
    server shopease-web-2:8000 max_fails=3 fail_timeout=30s;
    server shopease-web-3:8000 max_fails=3 fail_timeout=30s;
    keepalive 32;
}
```

### Database Scaling (PostgreSQL)
For high-traffic scenarios, consider:
- Read replicas
- Connection pooling (PgBouncer)
- Database partitioning

## 🔐 Security Hardening

### 1. Firewall Configuration
```bash
# Install UFW
sudo apt install ufw

# Configure firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Security Headers
Already configured in nginx:
- HSTS
- CSP (Content Security Policy)
- X-Frame-Options
- X-Content-Type-Options

### 3. Regular Updates
```bash
# Create update script
cat > update.sh << 'EOF'
#!/bin/bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker compose build --no-cache

# Deploy with zero downtime
docker compose up -d

# Clean up old images
docker image prune -f
EOF

chmod +x update.sh
```

### 4. Security Monitoring
- Enable fail2ban for SSH protection
- Monitor logs for suspicious activity
- Set up Sentry for error tracking
- Use strong passwords and 2FA

## 🔧 Troubleshooting

### Common Issues

#### 1. Container Won't Start
```bash
# Check logs
docker compose logs [service-name]

# Check resource usage
docker stats

# Restart specific service
docker compose restart [service-name]
```

#### 2. Database Connection Issues
```bash
# Check database status
docker compose exec db pg_isready -U shopease

# Reset database password
docker compose exec db psql -U shopease -c "ALTER USER shopease PASSWORD 'newpassword';"
```

#### 3. SSL Certificate Issues
```bash
# Test SSL certificate
openssl x509 -in docker/ssl/cert.pem -text -noout

# Check certificate expiration
openssl x509 -in docker/ssl/cert.pem -noout -dates
```

#### 4. Performance Issues
```bash
# Monitor resource usage
docker stats

# Check application metrics
curl http://localhost:5555/api/workers  # Flower API

# Database performance
docker compose exec db psql -U shopease -c "SELECT * FROM pg_stat_activity;"
```

### Health Checks
```bash
# Application health
curl -f http://localhost/health/

# Database health
docker compose exec db pg_isready -U shopease

# Redis health
docker compose exec redis redis-cli ping
```

### Emergency Procedures

#### 1. Complete System Recovery
```bash
# Stop all services
docker compose down

# Remove all containers and volumes (DESTRUCTIVE!)
docker compose down -v

# Restore from backup
./restore.sh

# Restart services
docker compose up -d
```

#### 2. Database Emergency Recovery
```bash
# Stop application
docker compose stop web worker beat

# Create emergency backup
docker compose exec db pg_dump -U shopease shopease > emergency_backup.sql

# Restore from last known good backup
cat backups/last_good_backup.sql | docker compose exec -T db psql -U shopease shopease

# Start application
docker compose start web worker beat
```

## 📞 Support & Maintenance

### Regular Maintenance Tasks
- [ ] Weekly security updates
- [ ] Daily backup verification
- [ ] Monthly SSL certificate check
- [ ] Quarterly performance review
- [ ] Log rotation and cleanup

### Monitoring Checklist
- [ ] Application uptime
- [ ] Database performance
- [ ] SSL certificate validity
- [ ] Disk space usage
- [ ] Memory and CPU usage
- [ ] Error rates and logs

### Contact Information
- **Repository**: https://github.com/shuaibansari123/MyEcommerceSite-with-WebSeries-Section
- **Issues**: Create an issue on GitHub
- **Email**: admin@shopease.com

---

**⚠️ Important**: Always test deployments in a staging environment before applying to production. Keep regular backups and have a rollback plan ready. 