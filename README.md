# English Assistant

A local web application to help Spanish speakers improve their English skills through vocabulary explanations, writing correction, grammar concepts, and phrasal verb learning. The system uses offline HuggingFace models and LangGraph agents, with all history stored locally in PostgreSQL.

## Features

- **Vocabulary Explanations**: Bilingual word and sentence explanations
- **Writing Correction**: Grammar correction with detailed explanations
- **Grammar Concepts**: Grammar rules and word comparisons
- **Phrasal Verbs**: Interactive learning with progress tracking
- **Learning History**: Searchable history across all sections
- **Offline Operation**: No external API keys required

## Architecture

- **Frontend**: Single Page Application with TailwindCSS
- **Backend**: Python with FastAPI and LangGraph agents
- **Database**: PostgreSQL for local data storage
- **AI Models**: HuggingFace Transformers (offline mode)

## Project Structure

```
english-assistant/
├── backend/                 # Python backend
│   ├── agents/             # LangGraph agents
│   ├── api/                # FastAPI endpoints
│   ├── models/             # Database models
│   ├── utils/              # Utility functions
│   ├── config.py           # Configuration settings
│   └── requirements.txt    # Python dependencies
├── frontend/               # Frontend application
│   ├── css/                # Styles and TailwindCSS
│   ├── js/                 # JavaScript application
│   ├── index.html          # Main HTML file
│   └── package.json        # Node.js dependencies
├── database/               # Database schema and migrations
│   └── schema.sql          # PostgreSQL schema
└── .env.example            # Environment configuration template
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### Backend Setup

1. Create and activate Python virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment configuration:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Build TailwindCSS:
```bash
npm run build-css
```

### Database Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE english_assistant;
CREATE USER english_assistant_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE english_assistant TO english_assistant_user;
```

2. Run database migrations (to be implemented in Task 2)

## Development

### Quick Start

```bash
# Complete setup (first time)
make setup

# Start development environment
make dev

# Or start individual servers
make dev-backend    # Backend API only
make dev-frontend   # Frontend only
```

### Development Servers

- **Backend API**: http://localhost:8000
  - API Documentation: http://localhost:8000/docs
  - Health Check: http://localhost:8000/health
- **Frontend**: http://localhost:3000
- **TailwindCSS**: Auto-rebuilds on file changes

### Development Commands

```bash
# Setup and installation
make install        # Install all dependencies
make setup         # Complete project setup

# Development
make dev           # Start both servers
make dev-backend   # Backend API only  
make dev-frontend  # Frontend only

# Building
make build         # Build all assets
make build-css     # Build TailwindCSS

# Testing and quality
make test          # Run all tests
make lint          # Run linters
make format        # Format code
make check         # Check dependencies

# Utilities
make clean         # Clean build artifacts
make help          # Show all commands
```

### Manual Development

If you prefer to run servers manually:

```bash
# Backend (Terminal 1)
cd backend
python run_server.py

# Frontend (Terminal 2) 
cd frontend
python serve.py

# TailwindCSS Watch (Terminal 3)
cd frontend
npm run dev
```

## License

MIT License