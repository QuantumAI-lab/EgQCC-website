# Community Lecture Archive

[![Deploy to GitHub Pages](https://github.com/GamalMoneep/Quantum_ai/workflows/Deploy%20to%20GitHub%20Pages/badge.svg)](https://github.com/GamalMoneep/Quantum_ai/actions)
[![MkDocs](https://img.shields.io/badge/MkDocs-Material-blue.svg)](https://squidfunk.github.io/mkdocs-material/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)

A professional lecture archive website built with MkDocs Material theme, showcasing weekly quantum computing lectures and monthly community events.

## 🌟 Features

- **📚 Weekly Lectures**: Comprehensive quantum computing content with video recordings
- **🎯 Monthly Events**: Community meetups with workshops and networking
- **👥 Contributors**: Team profiles with social media links
- **📖 Resources**: Curated learning materials and tools
- **🔍 SEO Optimized**: Meta descriptions, sitemap, and search engine friendly
- **📱 Responsive Design**: Mobile-friendly with Material theme
- **🚀 Auto-Deployment**: GitHub Actions workflow for seamless updates

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/GamalMoneep/Quantum_ai.git
   cd Quantum_ai
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run locally**
   ```bash
   mkdocs serve
   ```
   
   Visit `http://127.0.0.1:8000` to view the site.

## 📁 Project Structure

```
Quantum_ai/
├── docs/
│   ├── index.md                 # Homepage
│   ├── lectures/                # Weekly lectures
│   │   ├── index.md
│   │   ├── week-01.md
│   │   ├── week-02.md
│   │   └── week-03.md
│   ├── events/                  # Monthly events
│   │   ├── index.md
│   │   └── january-2024.md
│   ├── resources/               # Learning resources
│   │   └── index.md
│   ├── contributors/            # Team profiles
│   │   └── index.md
│   └── assets/                  # Images and styles
│       ├── stylesheets/
│       └── contributors/
├── .github/workflows/           # GitHub Actions
│   └── deploy.yml
├── mkdocs.yml                   # MkDocs configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 📝 Adding New Content

### Adding a New Lecture

1. Create a new file in `docs/lectures/` (e.g., `week-04.md`)
2. Use the template structure:
   ```markdown
   ---
   description: "Week 4: [Title] - [Brief description for SEO, 150-160 characters]"
   ---
   
   # Week 4: [Lecture Title]
   **Date:** YYYY-MM-DD  
   **Duration:** X minutes  
   **Last Updated:** YYYY-MM-DD
   
   ## Overview
   Brief description...
   
   ## Video
   [YouTube Link](https://youtube.com/watch?v=VIDEO_ID)
   
   ## Materials
   - [Slides (PDF)](github-link)
   - [Code Repository](github-link)
   
   ## Topics Covered
   - Topic 1
   - Topic 2
   
   ## Version History
   - **YYYY-MM-DD**: Initial release
   ```

3. Add to navigation in `mkdocs.yml`
4. Update `docs/lectures/index.md` with a link

### Adding a New Event

1. Create a new file in `docs/events/` (e.g., `february-2024.md`)
2. Follow the same template structure as lectures
3. Update navigation and overview page

### SEO Guidelines

- **Page titles**: Keep under 60 characters
- **Meta descriptions**: 150-160 characters, compelling and descriptive
- **Headings**: Use proper H1, H2, H3 hierarchy
- **URLs**: Keep clean and descriptive (MkDocs handles this automatically)

## 🚀 Deployment

### Automatic Deployment

The site automatically deploys to GitHub Pages when you push to the `main` or `master` branch.

1. **Push your changes**
   ```bash
   git add .
   git commit -m "Add new lecture: Week 4"
   git push origin master
   ```

2. **Monitor deployment**
   - Check the [GitHub Actions](https://github.com/GamalMoneep/Quantum_ai/actions) tab
   - Deployment typically takes 2-3 minutes
   - Site will be available at `https://gamalmoneep.github.io/Quantum_ai/`

### Manual Deployment

If needed, you can deploy manually:

```bash
mkdocs gh-deploy
```

## 🛠️ Configuration

### Customizing the Theme

Edit `mkdocs.yml` to customize:
- Colors and fonts
- Navigation structure
- Social media links
- SEO settings

### Adding Custom CSS

Custom styles are in `docs/assets/stylesheets/extra.css`:
- Contributor card styling
- Responsive design improvements
- Custom button effects

## 📊 Content Versioning

- Track major updates with "Last Updated" timestamps
- Use version history sections for significant changes
- Keep version notes brief but informative
- Update dates when content changes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-content`)
3. Add your content following the templates
4. Commit your changes (`git commit -m 'Add amazing content'`)
5. Push to the branch (`git push origin feature/amazing-content`)
6. Open a Pull Request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/GamalMoneep/Quantum_ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GamalMoneep/Quantum_ai/discussions)
- **Email**: your-email@example.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) for the beautiful theme
- [GitHub Pages](https://pages.github.com/) for hosting
- The quantum computing community for inspiration and content

---

**Built with ❤️ by the Quantum Computing Community**
