# English Assistant Deployment Guide

This directory contains configuration files and scripts for deploying English Assistant in production environments.

## Deployment Options

### 1. Traditional Linux Server Deployment

#### Prerequisites
- Ubuntu 20.04+ or similar Linux distribution
- Root access (sudo)
- PostgreSQL 12+
- Nginx
- Python 3.8+

#### Quick Deployment
```bash
# Clone the repository
git clone <repository-url>
cd english-assistant

# Run deployment script (as root)
sudo ./deployment/deploy.sh
```

#### Manual Deployment Steps

1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install nginx postgresql python3 python3-pip python3-venv
   ```

2. **Create Application User**
   ```bash
   sudo useradd --system --shell /bin/bash --home-dir /opt/english-assistant --create-home english-assistant
   ```

3. **Deploy Application Files**
   ```bash
   sudo mkdir -p /opt/english-assistant
   sudo cp -r backend frontend /opt/english-assistant/
   sudo chown -R english-assistant:english-assistant /opt/english-assistant
   ```

4. **Setup Python Environment**
   ```bash
   sudo -u english-assistant python3 -m venv /opt/english-assistant/backend/venv
   sudo -u english-assistant /opt/english-assistant/backend/venv/bin/pip install -r /opt/english-assistant/backend/requirements.txt
   ```

5. **Configure Database**
   ```bash
   sudo -u postgres createdb english_assistant
   sudo -u postgres createuser english_assistant_user
   sudo -u postgres psql -c "ALTER USER english_assistant_user WITH PASSWORD 'your_password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE english_assistant TO english_assistant_user;"
   ```

6. **Configure Environment**
   ```bash
   sudo cp deployment/production.env /opt/english-assistant/.env
   # Edit /opt/english-assistant/.env with your settings
   ```

7. **Setup Systemd Service**
   ```bash
   sudo cp deployment/english-assistant.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable english-assistant
   sudo systemctl start english-assistant
   ```

8. **Configure Nginx**
   ```bash
   sudo cp deployment/nginx.conf /etc/nginx/sites-available/english-assistant
   sudo ln -s /etc/nginx/sites-available/english-assistant /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### 2. Docker Deployment

#### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

#### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd english-assistant/deployment

# Create environment file
cp production.env .env
# Edit .env with your settings

# Start services
docker-compose up -d
```

#### Docker Commands
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose build --no-cache
docker-compose up -d

# Scale backend (if needed)
docker-compose up -d --scale backend=3
```

## Configuration Files

### Nginx Configuration (`nginx.conf`)
- Serves frontend static files
- Proxies API requests to backend
- Includes security headers and caching
- SSL/TLS configuration (commented out)

### Systemd Service (`english-assistant.service`)
- Manages backend API process
- Auto-restart on failure
- Security restrictions
- Resource limits

### Docker Configuration
- `Dockerfile.backend`: Backend API container
- `Dockerfile.frontend`: Frontend + Nginx container
- `docker-compose.yml`: Complete stack orchestration

## Security Considerations

### Environment Variables
Always change these in production:
- `SECRET_KEY`: Use a strong, random secret key
- `DB_PASSWORD`: Use a secure database password
- `CORS_ORIGINS`: Restrict to your domain only

### SSL/TLS Setup
For HTTPS, use Let's Encrypt with Certbot:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

## Monitoring and Maintenance

### Service Status
```bash
# Check service status
sudo systemctl status english-assistant
sudo systemctl status nginx
sudo systemctl status postgresql

# View logs
sudo journalctl -u english-assistant -f
sudo tail -f /var/log/nginx/english-assistant-access.log
```

### Health Checks
- Backend: `http://your-domain/health`
- Frontend: `http://your-domain/`
- API Docs: `http://your-domain/docs`

### Backup
```bash
# Database backup
sudo -u postgres pg_dump english_assistant > backup.sql

# Application backup
sudo tar -czf english-assistant-backup.tar.gz /opt/english-assistant
```

### Updates
```bash
# Stop services
sudo systemctl stop english-assistant

# Update code
cd /opt/english-assistant
sudo git pull origin main

# Update dependencies
sudo -u english-assistant /opt/english-assistant/backend/venv/bin/pip install -r backend/requirements.txt

# Restart services
sudo systemctl start english-assistant
sudo systemctl reload nginx
```

## Troubleshooting

### Common Issues

1. **Service won't start**
   ```bash
   sudo journalctl -u english-assistant -n 50
   ```

2. **Database connection errors**
   - Check PostgreSQL is running: `sudo systemctl status postgresql`
   - Verify credentials in `.env` file
   - Test connection: `psql -h localhost -U english_assistant_user -d english_assistant`

3. **Nginx errors**
   ```bash
   sudo nginx -t  # Test configuration
   sudo tail -f /var/log/nginx/error.log
   ```

4. **Permission issues**
   ```bash
   sudo chown -R english-assistant:english-assistant /opt/english-assistant
   ```

### Performance Tuning

1. **Backend Scaling**
   - Increase workers in systemd service
   - Use load balancer for multiple instances

2. **Database Optimization**
   - Configure PostgreSQL for your hardware
   - Set up connection pooling

3. **Caching**
   - Enable Redis for session storage
   - Configure Nginx caching for static assets

## Support

For deployment issues:
1. Check the logs first
2. Verify all configuration files
3. Test individual components
4. Check firewall and network settings