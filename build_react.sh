#!/bin/bash

# Build script for React components

echo "🚀 Building React components..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build for production
echo "🔨 Building React components..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ React components built successfully!"
    echo "📁 Built files are in static/dist/"
else
    echo "❌ Build failed!"
    exit 1
fi

echo "🎉 React setup complete!"
echo ""
echo "Next steps:"
echo "1. Start your Django server: python manage.py runserver"
echo "2. The React calendar should load automatically"
echo "3. For development, run: npm run dev (for watch mode)"