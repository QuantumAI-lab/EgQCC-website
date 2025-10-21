#!/usr/bin/env python3
"""
Script to download team member images from Google Drive
"""

import os
import requests
from pathlib import Path

# Create contributors directory if it doesn't exist
contributors_dir = Path("docs/assets/contributors")
contributors_dir.mkdir(parents=True, exist_ok=True)

# Google Drive direct download links (you'll need to get these from the shared folder)
# These are the file IDs from the Google Drive folder
drive_links = {
    "asmaa-saafan.PNG": "1fli0hZvrlBQdvrcu8XbRLnIhnl_308En",  # Dr Asmaa Saafan pic
    "ahmed-el-taher.png": "1djyuid3hp017CJ-JRaURIF5wzzWcDeaD",  # Ahmed El-Taher
    "mohammed-nabil.jpg": "17nlJCKNN8f-Q4_ZU1B5UnVhppsR4U6Ki",  # Mohammed Nabil
    "abdelrahman-elsayed.jpeg": "1KLYleCPT7cEcrqjDB_FGTpi2XrxgYkHy",  # Abdelrahman
    "omar-sobhy.jpeg": "1jFCBdmCqiaua4DrMnGWU3sZBERU84CIu",  # Omar Sobhy
    "muhammad-fergany.jpeg": "1IQWqVL63frgTDhyfSiYLAzRl479h9L2S",  # Muhammad Fergany
    "ziad-tarek.JPG": "11xe4G72puZN7fpHXAUbd49bz6ScMTYZn",  # Ziad Tarek
    "ahmed-saad-el-fiky.jpeg": "1rY7lbVg9Ll9T1iDIbms_jmXzr1xPCKnZ",  # Ahmed Saad El Fiky
    "moataz-mohamed.jpg": "1PUlwiU-aZM8d8bL7iuM8-LhsqgY034_q"  # Moataz Mohamed
}

def download_file(file_id, filename):
    """Download a file from Google Drive using file ID"""
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    try:
        print(f"Downloading {filename}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        file_path = contributors_dir / filename
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def main():
    print("🚀 Starting team member image downloads...")
    print(f"📁 Target directory: {contributors_dir.absolute()}")
    
    success_count = 0
    total_count = len(drive_links)
    
    for filename, file_id in drive_links.items():
        if download_file(file_id, filename):
            success_count += 1
    
    print(f"\n📊 Download Summary:")
    print(f"✅ Successfully downloaded: {success_count}/{total_count} images")
    
    if success_count == total_count:
        print("🎉 All images downloaded successfully!")
        print("🔄 The website should now display all team member photos.")
    else:
        print("⚠️  Some images failed to download. Please check the error messages above.")

if __name__ == "__main__":
    main()
