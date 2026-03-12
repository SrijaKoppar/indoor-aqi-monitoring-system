#!/bin/bash

# Air Quality Monitor - Development Startup Script
# This script starts both the React frontend and FastAPI backend

set -e

echo "🚀 Air Quality Monitor - Development Startup"
echo "=============================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "   Please install Node.js from https://nodejs.org"
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed"
    echo "   Please install Python from https://www.python.org"
    exit 1
fi

echo "✓ Node.js version: $(node --version)"
echo "✓ Python version: $(python --version)"
echo ""

# Step 1: Setup Frontend
echo "📦 Setting up frontend..."
if [ ! -d "node_modules" ]; then
    pnpm install
else
    echo "   ✓ Dependencies already installed"
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "   📝 Creating .env.local..."
    cp .env.local.example .env.local
    echo "   ✓ .env.local created"
fi

echo "✓ Frontend setup complete"
echo ""

# Step 2: Setup Backend
echo "📦 Setting up backend..."
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "   🐍 Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
fi

# Install dependencies
if ! pip show fastapi &> /dev/null; then
    echo "   📥 Installing Python dependencies..."
    pip install -r requirements.txt
else
    echo "   ✓ Dependencies already installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "   📝 Creating .env..."
    cp .env.example .env
    echo "   ✓ .env created"
fi

echo "✓ Backend setup complete"
echo ""

cd ..

# Step 3: Display instructions
echo "════════════════════════════════════════════"
echo "✅ Setup complete!"
echo "════════════════════════════════════════════"
echo ""
echo "To start development, open TWO terminals:"
echo ""
echo "Terminal 1 - Frontend:"
echo "  $ pnpm dev"
echo "  → http://localhost:3000"
echo ""
echo "Terminal 2 - Backend:"
echo "  $ cd backend"
echo "  $ source venv/bin/activate"
echo "  $ uvicorn main:app --reload"
echo "  → http://localhost:8000"
echo "  → API Docs: http://localhost:8000/docs"
echo ""
echo "Or if you have 'concurrently' installed, run:"
echo "  $ pnpm dev:all"
echo ""
echo "════════════════════════════════════════════"
