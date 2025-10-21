# YouTube Playlist Automation

This project includes automated systems to keep your website synchronized with your YouTube playlists.

## 🤖 Automatic Updates

### What Gets Updated Automatically

The automation system monitors two YouTube playlists:

1. **Monthly Series**: `PLbzgihkqSogoFQ4BNssbgdEJWQyU4C4Yo`
2. **Quantum AI Lab**: `PLbzgihkqSogor2r6XvsjvdgFIO770L4BG`

### When Updates Happen

- **Daily**: Every day at 6 AM UTC, GitHub Actions checks for new videos
- **Manual**: You can trigger updates manually from the GitHub Actions tab
- **On Push**: Updates run when you modify the automation scripts

### What Happens During Updates

1. **Fetch Videos**: Downloads latest video information from both playlists
2. **Create Pages**: Generates individual episode pages for new videos
3. **Update Navigation**: Adds new episodes to the website navigation
4. **Update Index**: Refreshes series overview pages with new episodes
5. **Commit Changes**: Automatically commits new content to the repository
6. **Deploy Site**: Rebuilds and deploys the website to GitHub Pages

## 📁 File Structure

```
├── .github/workflows/
│   └── update-playlists.yml      # GitHub Actions workflow
├── scripts/
│   └── update_playlists.py       # Main automation script
├── update_playlists.sh           # Manual update script
└── AUTOMATION.md                 # This documentation
```

## 🔧 Manual Updates

### Using the Manual Script

If you want to update playlists manually:

```bash
./update_playlists.sh
```

This will:
- Check both playlists for new videos
- Create pages for any new videos found
- Show you what changed
- Ask if you want to commit the changes

### Using Python Directly

For advanced users:

```bash
source venv/bin/activate
cd scripts
python update_playlists.py
```

## ⚙️ Configuration

### Playlist Configuration

Edit `scripts/update_playlists.py` to modify playlist settings:

```python
PLAYLISTS = {
    'monthly-series': {
        'playlist_id': 'PLbzgihkqSogoFQ4BNssbgdEJWQyU4C4Yo',
        'directory': 'docs/monthly-series',
        'nav_section': 'Monthly Series',
        'series_name': 'Monthly Series'
    },
    'quantum-ai-lab': {
        'playlist_id': 'PLbzgihkqSogor2r6XvsjvdgFIO770L4BG',
        'directory': 'docs/quantum-ai-lab',
        'nav_section': 'Quantum AI Lab',
        'series_name': 'Quantum AI Lab'
    }
}
```

### Schedule Configuration

Edit `.github/workflows/update-playlists.yml` to change the update schedule:

```yaml
schedule:
  - cron: '0 6 * * *'  # Daily at 6 AM UTC
```

## 📺 How New Videos Are Processed

### 1. Video Detection
- Fetches playlist information from YouTube
- Extracts video titles, durations, and IDs
- Compares with existing episodes to find new content

### 2. Page Generation
- Creates comprehensive episode pages with:
  - Embedded YouTube video player
  - Episode summary and description
  - Topic breakdown based on video title
  - Community discussion sections
  - Additional resources and next steps

### 3. Navigation Updates
- Adds new episodes to mkdocs.yml navigation
- Updates series overview pages
- Maintains chronological episode ordering

### 4. Content Enhancement
- Automatically generates topic lists based on video titles
- Creates contextual summaries and descriptions
- Adds relevant tags and metadata

## 🚀 GitHub Actions Workflow

### Triggers
- **Schedule**: Daily at 6 AM UTC
- **Manual**: Via GitHub Actions tab
- **Push**: When automation files are modified

### Permissions Required
- `contents: write` - To commit new files
- `pages: write` - To deploy to GitHub Pages
- `id-token: write` - For GitHub Pages deployment

### Environment Variables
No special environment variables or secrets are required. The workflow uses the default `GITHUB_TOKEN`.

## 🔍 Monitoring Updates

### Check Automation Status
1. Go to your GitHub repository
2. Click on the "Actions" tab
3. Look for "Update YouTube Playlists" workflows
4. Click on any run to see detailed logs

### What to Look For
- ✅ **Success**: New videos found and processed
- ✅ **Success (No Changes)**: No new videos, everything up to date
- ❌ **Failure**: Check logs for errors (usually network or parsing issues)

## 🛠️ Troubleshooting

### Common Issues

#### No New Videos Detected
- Verify playlist IDs are correct
- Check if videos are actually public
- YouTube may have changed their page structure

#### Build Failures
- Check mkdocs.yml syntax
- Verify all required dependencies are installed
- Look for file permission issues

#### Deployment Issues
- Ensure GitHub Pages is enabled
- Check repository permissions
- Verify workflow has necessary permissions

### Debug Mode

To run the script with more verbose output:

```bash
cd scripts
python -u update_playlists.py
```

## 📈 Benefits of Automation

### For Content Creators
- ✅ **No Manual Work**: Videos automatically appear on your website
- ✅ **Consistent Format**: All episodes follow the same professional structure
- ✅ **SEO Optimized**: Each page includes proper metadata and descriptions
- ✅ **Always Current**: Website stays synchronized with your YouTube content

### For Visitors
- ✅ **Fresh Content**: New episodes appear within 24 hours
- ✅ **Rich Experience**: More than just embedded videos - full episode guides
- ✅ **Easy Navigation**: Chronological ordering and clear episode structure
- ✅ **Mobile Friendly**: Responsive design works on all devices

## 🔄 Future Enhancements

Potential improvements to consider:

- **Webhook Integration**: Instant updates when videos are published
- **Video Transcripts**: Automatic transcript generation and inclusion
- **Social Media**: Auto-post to social media when new episodes are added
- **Analytics**: Track episode popularity and engagement
- **Email Notifications**: Notify subscribers of new episodes

---

*This automation system ensures your quantum computing lecture archive stays current with minimal manual intervention!*

