# Content Addition Guide

This guide helps maintainers add new content to the Community Lecture Archive following our established patterns and best practices.

## 📝 Adding New Lectures

### Step 1: Create the Lecture File

1. Create a new file in `docs/lectures/` with the naming convention:
   - `week-XX.md` (e.g., `week-04.md`, `week-05.md`)
   - Use leading zeros for single digits (e.g., `week-01.md`)

### Step 2: Use the Template Structure

```markdown
---
description: "Week X: [Title] - [Brief description for SEO, exactly 150-160 characters]"
---

# Week X: [Lecture Title]
**Date:** YYYY-MM-DD  
**Duration:** X minutes  
**Last Updated:** YYYY-MM-DD

## Overview
[2-3 sentence description of what the lecture covers and who it's for]

## Video
[Watch on YouTube](https://youtube.com/watch?v=VIDEO_ID)

## Materials
- [Slides (PDF)](https://github.com/GamalMoneep/Quantum_ai/raw/main/slides/week-XX-title.pdf)
- [Code Repository](https://github.com/GamalMoneep/quantum-examples)

## Topics Covered
- [Topic 1]
- [Topic 2]
- [Topic 3]
- [Topic 4]
- [Topic 5]

## Version History
- **YYYY-MM-DD**: Initial release
```

### Step 3: Update Navigation

Add the new lecture to `mkdocs.yml`:

```yaml
nav:
  - Lectures:
      - Overview: lectures/index.md
      - "Week 1: Introduction to Quantum Computing": lectures/week-01.md
      - "Week 2: Quantum Algorithms": lectures/week-02.md
      - "Week 3: Quantum Machine Learning": lectures/week-03.md
      - "Week 4: [New Title]": lectures/week-04.md  # Add this line
```

### Step 4: Update Overview Page

Add a link to the new lecture in `docs/lectures/index.md`:

```markdown
### Week 4: [Lecture Title]
**Date:** 2024-02-05 | **Duration:** 75 minutes
[View Lecture →](week-04.md)

[Brief description of the lecture content]
```

## 🎯 Adding New Events

### Step 1: Create the Event File

1. Create a new file in `docs/events/` with the naming convention:
   - `[month]-[year].md` (e.g., `february-2024.md`, `march-2024.md`)

### Step 2: Use the Event Template

```markdown
---
description: "[Month] [Year] Community Meetup - [Brief description for SEO, exactly 150-160 characters]"
---

# [Month] [Year] Community Meetup
**Date:** YYYY-MM-DD  
**Duration:** X minutes  
**Last Updated:** YYYY-MM-DD

## Overview
[2-3 sentence description of the event]

## Event Details
- **Location:** [Virtual/In-person location]
- **Registration:** [Eventbrite/Registration link]
- **Recording:** [Watch on YouTube](https://youtube.com/watch?v=EVENT_VIDEO_ID)

## Agenda
- **6:00 PM**: Welcome and introductions
- **6:15 PM**: [Activity 1]
- **7:30 PM**: [Activity 2]
- **8:00 PM**: [Activity 3]
- **8:30 PM**: Closing remarks

## Materials
- [Workshop Slides](https://github.com/GamalMoneep/Quantum_ai/raw/main/events/[month]-[year]-workshop.pdf)
- [Additional Materials](https://github.com/GamalMoneep/Quantum_ai/raw/main/events/[filename].pdf)

## Topics Covered
- [Topic 1]
- [Topic 2]
- [Topic 3]

## Version History
- **YYYY-MM-DD**: Initial release
```

### Step 3: Update Navigation and Overview

Follow the same steps as lectures to update `mkdocs.yml` and `docs/events/index.md`.

## 🔍 SEO Best Practices

### Meta Descriptions (150-160 characters)

**Good examples:**
- "Week 4: Quantum Error Correction - Learn about error correction codes, fault tolerance, and how to build reliable quantum computers."
- "February 2024 Community Meetup - Hands-on quantum computing workshop with networking and Q&A. Join our monthly community event for learning and connection."

**Bad examples:**
- "Week 4 lecture" (too short)
- "This lecture covers quantum error correction in great detail with many examples and practical applications that you can use in your own quantum computing projects" (too long)

### Page Titles

- Keep under 60 characters
- Include key terms
- Be descriptive but concise

### Headings

- Use proper H1, H2, H3 hierarchy
- H1: Page title (only one per page)
- H2: Major sections
- H3: Subsections

## 📊 Content Versioning

### When to Update "Last Updated"

- New slides or materials added
- Video link updated
- Significant content corrections
- New topics added to existing lectures

### Version History Format

```markdown
## Version History
- **2024-01-15**: Initial release
- **2024-01-20**: Updated slides with corrections
- **2024-01-25**: Added new code examples
```

## 🖼️ Adding Images

### Contributor Photos

1. Add photos to `docs/assets/contributors/`
2. Use consistent naming: `[name]-photo.jpg`
3. Recommended size: 150px width
4. Format: JPG or PNG

### Other Images

1. Add to `docs/assets/images/`
2. Use descriptive filenames
3. Optimize for web (compress if needed)

## 🔗 Internal Linking

### Linking Between Pages

```markdown
[Link text](relative/path/to/page.md)
[Link text](../path/to/page.md)
```

### Examples

```markdown
- Start with [Week 1: Introduction to Quantum Computing](lectures/week-01.md)
- Check out our [monthly community meetups](events/january-2024.md)
- Find additional materials in our [resources section](resources/index.md)
```

## 🚀 Deployment Checklist

Before pushing new content:

- [ ] All meta descriptions are 150-160 characters
- [ ] Navigation is updated in `mkdocs.yml`
- [ ] Overview pages include new content links
- [ ] All internal links work correctly
- [ ] Images are properly sized and optimized
- [ ] Version history is updated if needed
- [ ] Content follows the template structure

## 📞 Getting Help

- Check existing content for examples
- Review the main README.md for setup instructions
- Open an issue for questions or problems
- Follow the established patterns for consistency

---

**Remember**: Consistency is key! Follow the established patterns to maintain the professional look and feel of the archive.
