#!/bin/bash

# SignSync Meet Deployment Script
# This script automates the deployment process for both frontend and backend

set -e

echo "🚀 Starting SignSync Meet Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js v16 or higher."
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm."
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed. Please install pip3."
        exit 1
    fi
    
    print_success "All requirements are met!"
}

# Deploy frontend
deploy_frontend() {
    print_status "Deploying frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing frontend dependencies..."
    npm install
    
    # Build production version
    print_status "Building production version..."
    npm run build
    
    # Check if Firebase CLI is installed
    if ! command -v firebase &> /dev/null; then
        print_warning "Firebase CLI not found. Installing..."
        npm install -g firebase-tools
    fi
    
    # Deploy to Firebase
    print_status "Deploying to Firebase..."
    firebase deploy --only hosting
    
    cd ..
    print_success "Frontend deployed successfully!"
}

# Deploy backend
deploy_backend() {
    print_status "Deploying backend..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing backend dependencies..."
    pip install -r requirements.txt
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Please create one from env.example"
        print_status "You can copy env.example to .env and update the values"
    fi
    
    print_success "Backend setup completed!"
    print_status "To start the backend server, run:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  python app.py"
    
    cd ..
}

# Setup AI model
setup_ai_model() {
    print_status "Setting up AI model..."
    
    cd ai-model
    
    # Create models directory if it doesn't exist
    mkdir -p models
    
    # Check if training data exists
    if [ ! -d "data" ]; then
        print_warning "Training data directory not found."
        print_status "To train the model, create a 'data' directory with ASL images organized by letter"
        print_status "Then run: python train_model.py"
    else
        print_status "Training data found. You can train the model with: python train_model.py"
    fi
    
    print_success "AI model setup completed!"
    
    cd ..
}

# Main deployment function
main() {
    print_status "Starting SignSync Meet deployment..."
    
    # Check requirements
    check_requirements
    
    # Deploy frontend
    deploy_frontend
    
    # Deploy backend
    deploy_backend
    
    # Setup AI model
    setup_ai_model
    
    print_success "🎉 Deployment completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Configure Firebase in frontend/src/firebase.js"
    echo "2. Set up environment variables in backend/.env"
    echo "3. Train the AI model with your data"
    echo "4. Start the backend server"
    echo ""
    echo "For more information, see README.md"
}

# Run main function
main "$@"
