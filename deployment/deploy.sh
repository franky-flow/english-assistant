#!/bin/bash
# English Assistant Production Deployment Script

set -e  # Exit on any error

# Configuration
APP_NAME="english-assistant"
APP_USER="english-assistant"
APP_DIR="/opt/english-assistant"
NGINX_SITES_DIR="/etc/nginx/sites-available"
NGINX_ENABLED_DIR="/etc/nginx/sites-enabled"
SYSTEMD_DIR="/etc/systemd/system"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root (use sudo)"
    fi
}

check_dependencies() {
    log "Checking system dependencies..."
    
    # Check if required packages are installed
    local packages=("nginx" "postgresql" "python3" "python3-pip" "python3-venv")
    local missing=()
    
    for package in "${packages[@]}"; do
        if ! command -v "$package" &> /dev/null && ! dpkg -l | grep -q "^ii  $package "; then
            missing+=("$package")
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        warn "Missing packages: ${missing[*]}"
        log "Installing missing packages..."
        apt-get update
        apt-get install -y "${missing[@]}"
    fi
    
    success "Dependencies check completed"
}

create_user() {
    log "Creating application user..."
    
    if ! id "$APP_USER" &>/dev/null; then
        useradd --system --shell /bin/bash --home-dir "$APP_DIR" --create-home "$APP_USER"
        success "Created user: $APP_USER"
    else
        log "User $APP_USER already exists"
    fi
}

setup_directories() {
    log "Setting up application directories..."
    
    # Create main directories
    mkdir -p "$APP_DIR"/{backend,frontend,logs,models_cache}
    mkdir -p /var/log/nginx
    
    # Set ownership
    chown -R "$APP_USER:$APP_USER" "$APP_DIR"
    chmod 755 "$APP_DIR"
    chmod 755 "$APP_DIR/logs"
    chmod 755 "$APP_DIR/models_cache"
    
    success "Directories created and configured"
}

deploy_application() {
    log "Deploying application files..."
    
    # Copy backend files
    cp -r backend/* "$APP_DIR/backend/"
    
    # Copy frontend files
    cp -r frontend/* "$APP_DIR/frontend/"
    
    # Copy configuration files
    if [ -f ".env.example" ]; then
        cp .env.example "$APP_DIR/.env"
        log "Copied .env.example to .env - please configure it"
    fi
    
    # Set ownership
    chown -R "$APP_USER:$APP_USER" "$APP_DIR"
    
    success "Application files deployed"
}

setup_python_environment() {
    log "Setting up Python virtual environment..."
    
    # Create virtual environment
    sudo -u "$APP_USER" python3 -m venv "$APP_DIR/backend/venv"
    
    # Install Python dependencies
    sudo -u "$APP_USER" "$APP_DIR/backend/venv/bin/pip" install --upgrade pip
    sudo -u "$APP_USER" "$APP_DIR/backend/venv/bin/pip" install -r "$APP_DIR/backend/requirements.txt"
    
    success "Python environment configured"
}

setup_database() {
    log "Setting up PostgreSQL database..."
    
    # Start PostgreSQL service
    systemctl start postgresql
    systemctl enable postgresql
    
    # Create database and user (if they don't exist)
    sudo -u postgres psql -c "CREATE DATABASE english_assistant;" 2>/dev/null || log "Database already exists"
    sudo -u postgres psql -c "CREATE USER english_assistant_user WITH PASSWORD 'change_this_password';" 2>/dev/null || log "User already exists"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE english_assistant TO english_assistant_user;" 2>/dev/null
    
    warn "Please update the database password in $APP_DIR/.env"
    success "Database setup completed"
}

configure_nginx() {
    log "Configuring Nginx..."
    
    # Copy Nginx configuration
    cp deployment/nginx.conf "$NGINX_SITES_DIR/$APP_NAME"
    
    # Enable site
    ln -sf "$NGINX_SITES_DIR/$APP_NAME" "$NGINX_ENABLED_DIR/$APP_NAME"
    
    # Remove default site if it exists
    rm -f "$NGINX_ENABLED_DIR/default"
    
    # Test Nginx configuration
    nginx -t
    
    # Reload Nginx
    systemctl reload nginx
    systemctl enable nginx
    
    success "Nginx configured and reloaded"
}

configure_systemd() {
    log "Configuring systemd service..."
    
    # Copy service file
    cp deployment/english-assistant.service "$SYSTEMD_DIR/"
    
    # Reload systemd
    systemctl daemon-reload
    
    # Enable and start service
    systemctl enable english-assistant
    systemctl start english-assistant
    
    success "Systemd service configured and started"
}

setup_ssl() {
    log "SSL setup (optional)..."
    
    if command -v certbot &> /dev/null; then
        log "Certbot is available for SSL setup"
        log "Run: certbot --nginx -d your-domain.com"
    else
        log "Install certbot for automatic SSL setup:"
        log "  apt-get install certbot python3-certbot-nginx"
    fi
}

show_status() {
    log "Checking service status..."
    
    echo "=== Service Status ==="
    systemctl status english-assistant --no-pager -l
    
    echo ""
    echo "=== Nginx Status ==="
    systemctl status nginx --no-pager -l
    
    echo ""
    echo "=== Application URLs ==="
    echo "Frontend: http://localhost/"
    echo "API: http://localhost/api/"
    echo "Health: http://localhost/health"
    echo "Docs: http://localhost/docs"
}

main() {
    log "Starting English Assistant deployment..."
    
    check_root
    check_dependencies
    create_user
    setup_directories
    deploy_application
    setup_python_environment
    setup_database
    configure_nginx
    configure_systemd
    setup_ssl
    
    success "Deployment completed successfully!"
    
    show_status
    
    echo ""
    warn "Important next steps:"
    echo "1. Configure $APP_DIR/.env with your settings"
    echo "2. Update database password in .env file"
    echo "3. Configure SSL certificate if needed"
    echo "4. Test the application: http://localhost/"
}

# Run main function
main "$@"