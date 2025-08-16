# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static blog site for M Yusuf (Backend Developer) built with a custom Python static site generator. The site features blog posts about software development, DevOps, and programming tutorials, primarily in English and Indonesian.

## Development Commands

### Build the site
```bash
python3 build.py
```
This generates the static site by:
- Processing blog posts from `posts/content/` directory
- Applying the base template from `templates/base.html`
- Creating individual post pages in `posts/` directory
- Building index pages with pagination (40 posts per page)
- Generating search index (`search-index.json`)
- Creating tags page with tag cloud

### Local development
Since this is a static site, you can serve it locally with any HTTP server:
```bash
python3 -m http.server 8000
# or
npx serve .
```

## Architecture

### Static Site Generator (`build.py`)
- **Metadata extraction**: Parses HTML comments in content files for post metadata (title, description, date, tags, author, image)
- **Template system**: Uses placeholder replacement in `templates/base.html`
- **Content processing**: Processes content files from `posts/content/` to generate final HTML pages
- **Search indexing**: Creates Lunr.js compatible search index
- **Pagination**: Automatically splits posts across multiple index pages
- **Tag system**: Generates tag cloud and grouped post listings

### Frontend Architecture
- **Bootstrap 5**: Primary CSS framework
- **Dark/Light theme**: CSS custom properties with JavaScript theme switching
- **Search**: Lunr.js for client-side full-text search
- **Code highlighting**: Highlight.js with theme-aware syntax highlighting
- **Responsive design**: Mobile-first approach with Bootstrap grid

### Content Structure
- Blog posts stored as HTML files in `posts/content/`
- **Filename Convention**: The filename must match the slug generated from the title (lowercase, spaces replaced with hyphens, colons removed). Example: "My New Post" → `my-new-post.html`
- Each post has metadata in HTML comments at the top:
  ```html
  <!--
  title: Post Title
  description: A brief description of your post
  date: YYYY-MM-DD
  tags: comma, separated, tags
  author: M Yusuf
  image: /assets/images/your-image.png
  image_credit: Source of the image
  -->
  ```
- Content should include `<article class="blog-post">` wrapper, title as `<h1>`, and date as `<div class="meta mb-4">`

### Key Components
- `build.py`: Main static site generator with functions for page building, indexing, and pagination
- `templates/base.html`: Master template with placeholder system for content injection
- `script.js`: Theme switching, search functionality, and syntax highlighting initialization
- `styles.css`: CSS custom properties for theming and responsive design
- `search-index.json`: Generated search index for client-side search

## File Organization

```
├── build.py                 # Static site generator
├── templates/base.html      # Master template
├── posts/content/          # Source blog posts (HTML with metadata)
├── posts/                  # Generated post pages
├── assets/images/          # Blog images and favicons
├── styles.css             # Main stylesheet with theme variables
├── script.js              # Client-side JavaScript
├── search-index.json      # Generated search index
└── index.html             # Generated homepage
```

## Content Guidelines

- Write posts in HTML format with metadata comments
- Use semantic HTML structure within posts
- Include relevant tags for better categorization
- Add descriptions for SEO and search functionality
- Images should be optimized and placed in `assets/images/`
- **Date Management**: Always use the current date (YYYY-MM-DD format) when creating new posts or updating existing content
- **Article Structure**: Content must include proper structure with `<article class="blog-post">` wrapper, `<h1>` for title, and `<div class="meta mb-4">` for formatted date
- **File Naming**: Filename must match the slug from title (lowercase, spaces→hyphens, remove colons). Example: "My New Post" → `my-new-post.html`

## Security Guidelines

- **Content Safety**: Ensure all blog content is safe from security issues before publishing
- **No Sensitive Data**: Never include API keys, passwords, or sensitive credentials in posts
- **Sanitize User Input**: Although this is a static site, be careful with any external content or embedded code
- **Image Security**: Verify all images are from trusted sources and don't contain malicious content
- **External Links**: Review external links in posts to ensure they point to safe, legitimate resources

## Deployment

The site is designed for GitHub Pages deployment. After running `python3 build.py`, commit and push the generated files to deploy.