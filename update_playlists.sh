#!/bin/bash
# Manual playlist update script for testing

echo "🚀 Starting playlist update..."

# Create scripts directory if it doesn't exist
mkdir -p scripts

# Copy the update script to scripts directory if it doesn't exist there
if [ ! -f "scripts/update_playlists.py" ]; then
    echo "📄 Setting up update script..."
    # The script is already created in the scripts directory
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install requests beautifulsoup4 lxml

# Run the update script
echo "📺 Updating playlists..."
cd scripts
python update_playlists.py

# Check if changes were made
if [ -n "$(git status --porcelain)" ]; then
    echo "✅ Changes detected!"
    echo "Changed files:"
    git status --porcelain
    
    echo "📝 Would you like to commit these changes? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        git add .
        git commit -m "🤖 Manual update: New videos added from YouTube playlists"
        echo "✅ Changes committed!"
    fi
else
    echo "✅ No changes needed - playlists are up to date"
fi

echo "🎉 Playlist update completed!"

