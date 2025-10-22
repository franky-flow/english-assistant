#!/bin/bash

# English Assistant Setup Script

echo "🚀 Setting up English Assistant..."

# Create logs directory
mkdir -p logs

# Backend setup
echo "📦 Setting up Python backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

cd ..

# Frontend setup
echo "🎨 Setting up frontend..."
cd frontend

# Install Node.js dependencies
if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies..."
    npm install
    
    # Build TailwindCSS
    echo "Building TailwindCSS..."
    npm run build
fi

cd ..

# Create environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating environment configuration..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your database credentials"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database credentials"
echo "2. Create PostgreSQL database"
echo "3. Run database migrations (Task 2)"
echo "4. Start the development servers"