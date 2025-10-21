#!/usr/bin/env python3
"""
Automated playlist updater for Quantum AI website.
Fetches videos from YouTube playlists and creates/updates episode pages.
"""

import requests
import re
import json
import os
import sys
from urllib.parse import parse_qs, urlparse
from datetime import datetime, timezone
import hashlib
import time

# Configuration
PLAYLISTS = {
    'monthly-series': {
        'playlist_id': 'PLbzgihkqSogoFQ4BNssbgdEJWQyU4C4Yo',
        'directory': '../docs/monthly-series',
        'nav_section': 'Monthly Series',
        'series_name': 'Monthly Series'
    },
    'quantum-ai-lab': {
        'playlist_id': 'PLbzgihkqSogor2r6XvsjvdgFIO770L4BG',
        'directory': '../docs/quantum-ai-lab',
        'nav_section': 'Quantum AI Lab',
        'series_name': 'Quantum AI Lab'
    },
    '2025/summer-school': {
        'playlist_id': 'PLbzgihkqSogq5WG5keipbrX25hYnIslnN',
        'directory': '../docs/2025/summer-school',
        'nav_section': 'Quantum Summer School',
        'series_name': 'Quantum Summer School August 2025'
    },
    '2025/hackathon': {
        'playlist_id': 'PLbzgihkqSogowGABsPzdjH84vnEEPtGty',
        'directory': '../docs/2025/hackathon',
        'nav_section': 'Alexandria Quantum Hackathon',
        'series_name': 'Alexandria Quantum Hackathon 2025'
    },
    '2025/dry-run-hackathon': {
        'playlist_id': 'PLbzgihkqSogoE3uMg5Md9J6NN6SRr9YGO',
        'directory': '../docs/2025/dry-run-hackathon',
        'nav_section': 'Quantum Hackathon Dry-Run',
        'series_name': 'Quantum Hackathon July 2025 - Virtual Dry-Run'
    }
}

def extract_playlist_id(url):
    """Extract playlist ID from YouTube URL."""
    parsed_url = urlparse(url)
    if 'list' in parse_qs(parsed_url.query):
        return parse_qs(parsed_url.query)['list'][0]
    return None

def get_playlist_info(playlist_id):
    """
    Fetch playlist information using web scraping approach.
    """
    try:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        content = response.text
        
        # Look for ytInitialData which contains playlist information
        pattern = r'var ytInitialData = ({.*?});'
        match = re.search(pattern, content)
        
        if match:
            try:
                data = json.loads(match.group(1))
                return extract_videos_from_data(data)
            except json.JSONDecodeError:
                print("Could not parse YouTube data")
                return []
        
        return []
        
    except Exception as e:
        print(f"Error fetching playlist {playlist_id}: {e}")
        return []

def extract_videos_from_data(data):
    """Extract video information from YouTube data structure."""
    videos = []
    
    try:
        # Navigate through the complex YouTube data structure
        contents = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
        
        for tab in contents:
            if 'tabRenderer' in tab:
                tab_content = tab['tabRenderer'].get('content', {})
                if 'sectionListRenderer' in tab_content:
                    sections = tab_content['sectionListRenderer'].get('contents', [])
                    
                    for section in sections:
                        if 'itemSectionRenderer' in section:
                            items = section['itemSectionRenderer'].get('contents', [])
                            
                            for item in items:
                                if 'playlistVideoListRenderer' in item:
                                    video_list = item['playlistVideoListRenderer'].get('contents', [])
                                    
                                    for video_item in video_list:
                                        if 'playlistVideoRenderer' in video_item:
                                            video = video_item['playlistVideoRenderer']
                                            video_info = extract_video_info(video)
                                            if video_info:
                                                videos.append(video_info)
        
        return videos
        
    except Exception as e:
        print(f"Error extracting videos: {e}")
        return []

def get_video_upload_date(video_id):
    """
    Fetch individual video upload date by scraping the video page.
    """
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        content = response.text
        
        # Look for upload date in various formats
        patterns = [
            r'"uploadDate":"([^"]+)"',
            r'"publishDate":"([^"]+)"',
            r'dateText":\{"simpleText":"([^"]+)"',
            r'uploaded":"([^"]+)"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                date_str = match.group(1)
                try:
                    # Try to parse ISO format first
                    if 'T' in date_str:
                        upload_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:
                        # Try to parse other formats
                        upload_date = datetime.strptime(date_str, "%b %d, %Y")
                    
                    return upload_date
                except ValueError:
                    continue
        
        # If no date found, return a default date (very old)
        return datetime(2020, 1, 1)
        
    except Exception as e:
        print(f"Error fetching upload date for {video_id}: {e}")
        return datetime(2020, 1, 1)  # Default to old date if error

def get_sort_key(video):
    """
    Generate intelligent sort key that prioritizes episode numbers over dates.
    """
    title = video.get('title', '').lower()
    upload_date = video.get('upload_date', datetime(2020, 1, 1))
    
    # Extract various episode/series numbers
    episode_num = None
    series_num = None
    lab_num = None
    
    # Look for episode numbers: "Episode 1", "#1", "Lab #1", etc.
    episode_patterns = [
        r'episode\s*#?(\d+)',
        r'lab\s*#?(\d+)',
        r'#(\d+)',
        r'ep\s*(\d+)',
        r'part\s*(\d+)'
    ]
    
    for pattern in episode_patterns:
        match = re.search(pattern, title)
        if match:
            episode_num = int(match.group(1))
            break
    
    # Look for series numbers: "S1", "S3", "S4", etc.
    series_match = re.search(r's(\d+)', title)
    if series_match:
        series_num = int(series_match.group(1))
    
    # Look for lab numbers in different formats
    lab_patterns = [
        r'quantum\s*ai\s*lab\s*#?(\d+)',
        r'lab\s*#?(\d+)',
        r'الكم.*?(\d+)'  # Arabic patterns
    ]
    
    for pattern in lab_patterns:
        match = re.search(pattern, title)
        if match:
            lab_num = int(match.group(1))
            break
    
    # Create sort key with priorities:
    # 1. Episode number (if found)
    # 2. Series number (if found) 
    # 3. Lab number (if found)
    # 4. Upload date as tiebreaker
    
    # Use a large number (9999) for missing numbers so they sort last
    sort_episode = episode_num if episode_num is not None else 9999
    sort_series = series_num if series_num is not None else 9999
    sort_lab = lab_num if lab_num is not None else 9999
    
    # Special handling for different video types
    if 'bibliotheca' in title and 'edition' in title:
        # Special editions get priority 0 (first)
        return (0, 0, 0, upload_date)
    elif episode_num is not None:
        # Regular episodes: sort by episode number
        return (1, sort_episode, 0, upload_date)
    elif series_num is not None:
        # Series: sort by series number
        return (2, sort_series, 0, upload_date)
    elif lab_num is not None:
        # Lab episodes: sort by lab number
        return (3, sort_lab, 0, upload_date)
    else:
        # Everything else: sort by date
        return (4, 0, 0, upload_date)

def extract_video_info(video_data):
    """Extract individual video information."""
    try:
        video_id = video_data.get('videoId', '')
        title = video_data.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown Title')
        
        # Extract duration if available
        duration = 'Unknown'
        if 'lengthText' in video_data:
            duration = video_data['lengthText'].get('simpleText', 'Unknown')
        
        # Extract description if available
        description = ''
        if 'descriptionSnippet' in video_data:
            desc_runs = video_data['descriptionSnippet'].get('runs', [])
            description = ' '.join([run.get('text', '') for run in desc_runs])
        
        # Extract publication date if available
        published_date = 'Unknown'
        if 'publishedTimeText' in video_data:
            published_date = video_data['publishedTimeText'].get('simpleText', 'Unknown')
        
        # Try to get index in playlist for ordering
        playlist_index = video_data.get('index', {}).get('simpleText', '0')
        if playlist_index.isdigit():
            playlist_index = int(playlist_index)
        else:
            playlist_index = 0
        
        return {
            'video_id': video_id,
            'title': title,
            'duration': duration,
            'description': description,
            'published_date': published_date,
            'playlist_index': playlist_index,
            'url': f'https://www.youtube.com/watch?v={video_id}'
        }
        
    except Exception as e:
        print(f"Error extracting video info: {e}")
        return None

def sanitize_filename(title):
    """Convert video title to a safe filename."""
    filename = re.sub(r'[^\w\s-]', '', title)
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.lower().strip('-')[:50]

def create_video_page(video, episode_num, series_name):
    """Create a markdown page for a single video."""
    
    # Extract episode number from title if possible
    title_match = re.search(r'#(\d+)', video['title'])
    if title_match:
        episode_display = f"Episode {title_match.group(1)}"
    else:
        episode_display = f"Episode {episode_num}"
    
    # Clean title for display
    clean_title = video['title'].replace('Quantum AI', '').strip()
    if clean_title.startswith('#'):
        clean_title = clean_title[clean_title.find(':')+1:].strip() if ':' in clean_title else clean_title[clean_title.find('|')+1:].strip() if '|' in clean_title else clean_title
    
    # Generate content based on title
    topics = generate_topics_from_title(video['title'])
    summary = generate_summary_from_title(video['title'])
    
    content = f'''---
description: "{episode_display}: {clean_title} - Comprehensive exploration of quantum computing topics with expert insights and practical applications."
---

# {episode_display}: {clean_title}

**Duration:** {video['duration']}  
**Published:** {video.get('upload_date_str', 'Unknown Date')}

## Video

<iframe width="100%" height="400" src="https://www.youtube.com/embed/{video['video_id']}" title="{video['title']}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

*[Watch on YouTube]({video['url']})*

## Episode Summary

{summary}

### Key Topics Covered
{topics}

## Detailed Description

This comprehensive session explores cutting-edge developments in quantum computing and artificial intelligence. The discussion covers both theoretical foundations and practical applications, making it valuable for researchers, students, and industry professionals.

### Session Highlights

- **Expert Presentations**: Leading researchers and practitioners share their insights
- **Interactive Discussions**: Q&A sessions with the community
- **Practical Applications**: Real-world use cases and implementations
- **Future Directions**: Emerging trends and research opportunities

## Topics Deep Dive

{generate_detailed_topics(video['title'])}

## Community Discussion

### Discussion Points
- What aspects of this session resonated most with you?
- How can these concepts be applied in your current work or research?
- What questions do you have about the topics covered?

### Related Episodes
- Browse other episodes in the [{series_name}](index.md)
- Explore related content in other series

## Additional Resources

### Recommended Reading
- Research papers mentioned in the session
- Documentation for tools and frameworks discussed
- Community-contributed resources and implementations

### Code Examples
- Implementation examples from the session
- Practice exercises and challenges
- Community-shared projects and solutions

## Next Steps

### For Beginners
1. Review fundamental concepts covered in earlier episodes
2. Practice with recommended quantum computing simulators
3. Join community study groups and discussions

### For Advanced Learners
1. Implement the algorithms and techniques discussed
2. Contribute to open-source quantum computing projects
3. Engage with research papers and cutting-edge developments

---

**Tags:** `quantum-computing` `quantum-ai` `research` `applications` `community`

*Join the discussion about this episode in our [community forum](https://github.com/yourusername/quantum-ai/discussions) and share your thoughts and questions!*
'''

    return content

def generate_topics_from_title(title):
    """Generate topic list based on video title."""
    topics = []
    
    if 'Communication' in title or 'Encryption' in title:
        topics.extend([
            "- Quantum communication protocols",
            "- Quantum encryption and cryptography",
            "- Quantum key distribution"
        ])
    
    if 'Education' in title:
        topics.extend([
            "- Quantum computing education strategies",
            "- Learning resources and curricula",
            "- Community building and outreach"
        ])
    
    if 'Machine Learning' in title:
        topics.extend([
            "- Quantum machine learning algorithms",
            "- Hybrid classical-quantum approaches",
            "- Optimization techniques"
        ])
    
    if 'IBM' in title:
        topics.extend([
            "- IBM Quantum platform and tools",
            "- Qiskit framework and applications",
            "- Industry partnerships and developments"
        ])
    
    if 'Chemistry' in title:
        topics.extend([
            "- Quantum chemistry applications",
            "- Molecular simulation and modeling",
            "- Drug discovery and materials science"
        ])
    
    if 'HPC' in title or 'Computing' in title:
        topics.extend([
            "- High-performance quantum computing",
            "- Classical-quantum hybrid systems",
            "- Computational complexity and advantages"
        ])
    
    if not topics:
        topics = [
            "- Quantum computing fundamentals",
            "- Practical applications and use cases",
            "- Research developments and innovations"
        ]
    
    return '\n'.join(topics)

def generate_summary_from_title(title):
    """Generate episode summary based on title."""
    if 'Communication' in title and 'Encryption' in title:
        return "This episode explores the fascinating world of quantum communications and encryption technologies. Learn about quantum key distribution, secure communication protocols, and the role of quantum mechanics in creating unbreakable encryption systems."
    
    elif 'Education' in title:
        return "A comprehensive discussion on quantum computing education, exploring effective teaching strategies, curriculum development, and community outreach initiatives. Discover how to make quantum concepts accessible to diverse audiences."
    
    elif 'Machine Learning' in title:
        return "Deep dive into the intersection of quantum computing and machine learning. Explore quantum algorithms for optimization, pattern recognition, and data analysis, along with practical implementations using current quantum platforms."
    
    elif 'Leadership' in title:
        return "Strategic insights into quantum computing leadership, energy considerations in quantum systems, error correction techniques, and the development of quantum AI agents. Includes discussions on industry partnerships and quantum foundries."
    
    elif 'Modelling' in title:
        return "Explore quantum modeling techniques and the development of quantum AI agents. This session covers theoretical foundations and practical applications in quantum system modeling and simulation."
    
    elif 'HPC' in title:
        return "Comprehensive overview of high-performance computing, quantum computing fundamentals, and artificial intelligence integration. Perfect introduction to the quantum computing landscape and its applications."
    
    else:
        return "A comprehensive exploration of quantum computing concepts, applications, and research developments. This session provides valuable insights for both beginners and advanced practitioners in the field."

def generate_detailed_topics(title):
    """Generate detailed topic breakdown."""
    sections = []
    
    if 'Communication' in title:
        sections.append("""
### Quantum Communications
- **Quantum Entanglement**: Understanding quantum correlations for communication
- **Quantum Teleportation**: Transferring quantum states across distances
- **Quantum Networks**: Building quantum communication infrastructure
""")
    
    if 'Encryption' in title:
        sections.append("""
### Quantum Encryption
- **Quantum Cryptography**: Principles of quantum-secure communication
- **Key Distribution**: Quantum key distribution protocols and implementations
- **Post-Quantum Cryptography**: Preparing for the quantum computing era
""")
    
    if 'Machine Learning' in title:
        sections.append("""
### Quantum Machine Learning
- **Quantum Algorithms**: Variational quantum algorithms for ML
- **Feature Mapping**: Quantum feature spaces and kernel methods
- **Optimization**: Quantum approaches to optimization problems
""")
    
    if 'Education' in title:
        sections.append("""
### Quantum Education
- **Curriculum Design**: Developing effective quantum computing courses
- **Hands-on Learning**: Laboratory exercises and practical implementations
- **Community Outreach**: Making quantum accessible to diverse audiences
""")
    
    if not sections:
        sections.append("""
### Core Topics
- **Theoretical Foundations**: Mathematical and physical principles
- **Practical Applications**: Real-world use cases and implementations
- **Future Directions**: Emerging trends and research opportunities
""")
    
    return ''.join(sections)

def load_existing_videos(directory):
    """Load existing video files to avoid duplicates."""
    existing = set()
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith('.md') and filename != 'index.md':
                existing.add(filename)
    return existing

def update_mkdocs_navigation(series_configs):
    """Update mkdocs.yml navigation with new videos."""
    mkdocs_path = '../mkdocs.yml'
    
    if not os.path.exists(mkdocs_path):
        print("mkdocs.yml not found")
        return False
    
    with open(mkdocs_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update navigation for each series
    for series_key, config in series_configs.items():
        nav_entries = []
        directory = config['directory']
        
        # Get all episode files
        episode_files = []
        if os.path.exists(directory):
            for filename in sorted(os.listdir(directory)):
                if filename.endswith('.md') and filename != 'index.md':
                    episode_files.append(filename)
        
        # Sort episodes by episode number if possible
        def extract_episode_num(filename):
            match = re.search(r'episode-(\d+)', filename)
            if match:
                return int(match.group(1))
            # Try to extract from title
            match = re.search(r'(\d+)', filename)
            if match:
                return int(match.group(1))
            return 999  # Put at end if no number found
        
        episode_files.sort(key=extract_episode_num)
        
        # Generate navigation entries
        nav_entries.append(f'      - Series Overview: {series_key}/index.md')
        
        for filename in episode_files:
            # Generate title from filename
            title = filename.replace('.md', '').replace('-', ' ').title()
            if len(title) > 40:
                title = title[:37] + '...'
            
            nav_entries.append(f'      - "{title}": {series_key}/{filename}')
        
        # Update the navigation section
        section_pattern = rf'(  - {config["nav_section"]}:\s*\n)(.*?)(\n  - [^:]+:|$)'
        replacement = f'\\1' + '\n'.join(nav_entries) + '\n\\3'
        
        content = re.sub(section_pattern, replacement, content, flags=re.DOTALL)
    
    # Write updated mkdocs.yml
    with open(mkdocs_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def update_series_index(directory, videos, series_name):
    """Update the series index page with new episodes."""
    index_path = os.path.join(directory, 'index.md')
    
    if not os.path.exists(index_path):
        print(f"Index file not found: {index_path}")
        return
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate episodes section
    episodes_section = "## Episodes\n\n"
    
    for i, video in enumerate(videos, 1):
        filename = sanitize_filename(video['title']) + '.md'
        
        # Extract episode number from title if possible
        title_match = re.search(r'#(\d+)', video['title'])
        if title_match:
            episode_display = f"Episode {title_match.group(1)}"
        else:
            episode_display = f"Episode {i}"
        
        # Clean title for display
        clean_title = video['title'].replace('Quantum AI', '').strip()
        if clean_title.startswith('#'):
            clean_title = clean_title[clean_title.find(':')+1:].strip() if ':' in clean_title else clean_title[clean_title.find('|')+1:].strip() if '|' in clean_title else clean_title
        
        episodes_section += f"""### {episode_display}: {clean_title}
**Duration:** {video['duration']}  
[Watch Episode →]({filename})

{generate_summary_from_title(video['title'])[:100]}...

"""
    
    # Replace the episodes section
    pattern = r'## Episodes.*?(?=\n## [^E]|\n\*New episodes|\Z)'
    content = re.sub(pattern, episodes_section.rstrip(), content, flags=re.DOTALL)
    
    # Write updated index
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Main function to update all playlists."""
    print("🚀 Starting playlist update...")
    
    changes_made = False
    
    for series_key, config in PLAYLISTS.items():
        print(f"\n📺 Processing {config['series_name']}...")
        
        # Create directory if it doesn't exist
        os.makedirs(config['directory'], exist_ok=True)
        
        # Fetch playlist videos
        videos = get_playlist_info(config['playlist_id'])
        
        if not videos:
            print(f"❌ No videos found for {config['series_name']}")
            continue
        
        print(f"✅ Found {len(videos)} videos")
        print("📅 Fetching upload dates for chronological sorting...")
        
        # Fetch upload dates for each video
        for i, video in enumerate(videos):
            print(f"   Fetching date for video {i+1}/{len(videos)}: {video['title'][:50]}...")
            upload_date = get_video_upload_date(video['video_id'])
            video['upload_date'] = upload_date
            video['upload_date_str'] = upload_date.strftime("%Y-%m-%d")
            time.sleep(1)  # Be respectful to YouTube servers
        
        # Sort videos using intelligent sorting (episode numbers + upload date)
        videos.sort(key=lambda x: get_sort_key(x))
        
        print(f"📊 Videos sorted intelligently by episode numbers and upload date")
        
        # Load existing videos
        existing_files = load_existing_videos(config['directory'])
        
        # Create pages for new videos
        new_videos = 0
        for i, video in enumerate(videos, 1):
            filename = sanitize_filename(video['title']) + '.md'
            filepath = os.path.join(config['directory'], filename)
            
            if filename not in existing_files:
                # Create new video page
                content = create_video_page(video, i, config['series_name'])
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"📄 Created: {filename}")
                new_videos += 1
                changes_made = True
        
        if new_videos == 0:
            print(f"✅ No new videos for {config['series_name']}")
        else:
            print(f"🎉 Created {new_videos} new video pages")
        
        # Update series index page
        update_series_index(config['directory'], videos, config['series_name'])
    
    if changes_made:
        # Update mkdocs navigation
        print("\n📝 Updating navigation...")
        update_mkdocs_navigation(PLAYLISTS)
        
        print("\n✅ Playlist update completed with changes!")
        return True
    else:
        print("\n✅ Playlist update completed - no changes needed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
