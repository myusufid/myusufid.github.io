# Personal Blog - M Yusuf

A high-performance, static blog site generated with a custom Python script. It features a modern, responsive design using Tailwind CSS, dark/light mode, and client-side full-text search.

## Features

- **Static Site Generation:** Fast and secure HTML generation using Python.
- **Modern Design:** Built with **Tailwind CSS** for a clean, responsive layout.
- **Dark/Light Mode:** Automatic system detection with manual toggle preference saved in local storage.
- **Full-Text Search:** Client-side search powered by **Lunr.js**.
- **Code Highlighting:** Syntax highlighting for code blocks using **Highlight.js**.
- **SEO Optimized:** Automatic meta tags and social sharing support.

## Tech Stack

- **Core:** HTML5, CSS3 (Tailwind CSS), JavaScript (Vanilla)
- **Generator:** Python 3 (`build.py`)
- **Styling:** Tailwind CSS (via CDN with Typography plugin)
- **Fonts:** Inter (Body), JetBrains Mono (Code)
- **Search:** Lunr.js
- **Syntax Highlighting:** Highlight.js

## Development

### 1. Project Setup

Ensure you have Python 3 installed.

```bash
# Clone the repository
git clone https://github.com/myusufid/myusufid.github.io.git
cd myusufid.github.io

# (Optional) Create a virtual environment if needed for specific Python dependencies
python3 -m venv venv
source venv/bin/activate
```

### 2. Adding a New Post

Create a new HTML file in the `posts/content/` directory. The filename will be used as the URL slug (e.g., `my-new-post.html`).

Each post must start with a metadata block:

```html
<!--
title: My New Blog Post
description: A brief summary of the post content.
date: 2026-02-18
tags: python, web, tutorial
image: /assets/images/my-post-image.png
image_credit: Image Source
-->

<article class="blog-post">
    <p class="lead">Introduction paragraph...</p>
    
    <h2>Section Title</h2>
    <p>Content goes here...</p>
</article>
```

### 3. Building the Site

Run the build script to generate the static HTML pages:

```bash
python3 build.py
```

This will:
1. Parse all content files in `posts/content/`.
2. Generate individual blog post pages in `posts/`.
3. Update the `index.html` (Home) with the latest posts.
4. Generate `tags.html`.
5. Create/Update the search index (`search_index.json`).

### 4. Local Preview

You can serve the site locally using Python's built-in HTTP server:

```bash
python3 -m http.server 8000
```
Then visit `http://localhost:8000` in your browser.

## Directory Structure

```
.
├── assets/             # Images and static assets
├── posts/              # Generated HTML blog posts
│   └── content/        # Source HTML content files with metadata
├── templates/          # HTML templates
│   └── base.html       # Main layout template
├── build.py            # Static site generator script
├── script.js           # Frontend logic (Search, Theme Toggle)
├── styles.css          # Custom CSS overrides
├── index.html          # Generated Homepage
└── tags.html           # Generated Tags page
```

## License

This project is open source and available under the [MIT License](LICENSE).