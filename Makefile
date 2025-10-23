# English Assistant Development Makefile

.PHONY: help dev dev-backend dev-frontend install setup test clean build

# Default target
help:
	@echo "English Assistant Development Commands"
	@echo "====================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install     - Install all dependencies"
	@echo "  make setup       - Complete project setup"
	@echo ""
	@echo "Development Commands:"
	@echo "  make dev         - Start both frontend and backend servers"
	@echo "  make dev-backend - Start only backend API server"
	@echo "  make dev-frontend- Start only frontend server"
	@echo ""
	@echo "Build Commands:"
	@echo "  make build       - Build frontend assets"
	@echo "  make build-css   - Build TailwindCSS"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test        - Run all tests"
	@echo "  make test-backend- Run backend tests"
	@echo "  make test-frontend- Run frontend tests"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make check       - Check dependencies"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code"

# Setup commands
install:
	@echo "📦 Installing dependencies..."
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Dependencies installed"

setup: install
	@echo "🔧 Setting up English Assistant..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file..."; \
		cp .env.example .env; \
	fi
	@echo "Building frontend assets..."
	cd frontend && npm run build
	@echo "✅ Setup complete!"
	@echo ""
	@echo "🚀 Ready to start development:"
	@echo "   make dev"

# Development commands
dev:
	@echo "🚀 Starting development environment..."
	python dev.py both

dev-backend:
	@echo "🚀 Starting backend server..."
	python dev.py backend

dev-frontend:
	@echo "🚀 Starting frontend server..."
	python dev.py frontend

# Build commands
build: build-css
	@echo "✅ Build complete"

build-css:
	@echo "🎨 Building TailwindCSS..."
	cd frontend && npm run build

build-dev:
	@echo "🎨 Starting TailwindCSS watch mode..."
	cd frontend && npm run dev

# Testing commands
test:
	@echo "🧪 Running all tests..."
	@if [ -d "backend/tests" ]; then \
		echo "Running backend tests..."; \
		cd backend && python -m pytest tests/ -v; \
	fi
	@if [ -f "frontend/test_frontend.py" ]; then \
		echo "Running frontend tests..."; \
		cd frontend && python test_frontend.py; \
	fi

test-backend:
	@echo "🧪 Running backend tests..."
	@if [ -d "backend/tests" ]; then \
		cd backend && python -m pytest tests/ -v; \
	else \
		echo "No backend tests found"; \
	fi

test-frontend:
	@echo "🧪 Running frontend tests..."
	@if [ -f "frontend/test_frontend.py" ]; then \
		cd frontend && python test_frontend.py; \
	else \
		echo "No frontend tests found"; \
	fi

# Utility commands
check:
	@echo "🔍 Checking dependencies..."
	python dev.py --check

clean:
	@echo "🧹 Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf backend/.coverage 2>/dev/null || true
	@rm -rf frontend/node_modules/.cache 2>/dev/null || true
	@echo "✅ Cleanup complete"

lint:
	@echo "🔍 Running linters..."
	@if command -v flake8 >/dev/null 2>&1; then \
		echo "Linting Python code..."; \
		flake8 backend/ --max-line-length=100 --ignore=E203,W503; \
	else \
		echo "flake8 not installed, skipping Python linting"; \
	fi
	@if command -v eslint >/dev/null 2>&1 && [ -f "frontend/.eslintrc.js" ]; then \
		echo "Linting JavaScript code..."; \
		cd frontend && eslint js/; \
	else \
		echo "ESLint not configured, skipping JavaScript linting"; \
	fi

format:
	@echo "🎨 Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		echo "Formatting Python code..."; \
		black backend/ --line-length=100; \
	else \
		echo "black not installed, skipping Python formatting"; \
	fi
	@if command -v prettier >/dev/null 2>&1; then \
		echo "Formatting JavaScript code..."; \
		cd frontend && prettier --write js/; \
	else \
		echo "prettier not installed, skipping JavaScript formatting"; \
	fi

# Database commands
db-setup:
	@echo "🗄️  Setting up database..."
	@echo "This would set up PostgreSQL database"
	@echo "Manual setup required - see README.md"

db-migrate:
	@echo "🗄️  Running database migrations..."
	@echo "Database migrations not implemented yet"

# Docker commands (for future use)
docker-build:
	@echo "🐳 Building Docker images..."
	@echo "Docker configuration not implemented yet"

docker-dev:
	@echo "🐳 Starting Docker development environment..."
	@echo "Docker configuration not implemented yet"