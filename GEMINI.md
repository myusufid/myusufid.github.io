# Project Overview

This project is a personal blog website for M Yusuf, a Backend Developer. It is a static website generated using a custom Python script. The blog features a clean, responsive design with light and dark themes, full-text search functionality, and syntax highlighting for code snippets.

## Key Technologies

*   **Static Site Generator:** Python
*   **Frontend:** HTML, CSS, JavaScript
*   **CSS Framework:** Bootstrap 5
*   **Search:** Lunr.js
*   **Syntax Highlighting:** Highlight.js

# Building and Running

The website is built using a Python script that processes content files and generates the final HTML pages.

**To add a new blog post:**

1.  Create a new HTML file in the `posts/content` directory.
2.  Add metadata to the top of the file in a comment block, including `title`, `description`, `date`, and `tags`.
3.  Write the blog post content in HTML below the metadata block.

**To build the website:**

Run the following command in the terminal:

```bash
python3 build.py
```

This will generate the static HTML files in the `posts` directory, update the home page with the latest posts, and create a search index.

# Development Conventions

*   **Content:** Blog post content is written in HTML and stored in the `posts/content` directory. The content of each post should be wrapped in an `<article class="blog-post">` tag. The title and date should be included at the top of the article body, for example:
    ```html
    <article class="blog-post">
        <h1>Post Title</h1>
        <div class="meta mb-4">YYYY-MM-DD</div>
        ...
    </article>
    ```
*   **Filenames:** The filename of the post in the `posts/content` directory must match the slug generated from the title. The slug is created by converting the title to lowercase, replacing spaces with hyphens, and removing colons. For example, a post with the title "My New Post" should have the filename `my-new-post.html`.
*   **Templates:** The base HTML template for all pages is `templates/base.html`.
*   **Styling:** Custom styles are defined in `styles.css`. The website uses Bootstrap 5 for its base styling.
*   **Scripts:** Custom JavaScript for theme switching and search is in `script.js`.
*   **Metadata:** Each blog post must contain a metadata block at the top of the file, formatted as follows. Make sure the `date` is always the current date:

```html
<!--
title: Your Post Title
description: A brief description of your post.
date: YYYY-MM-DD
tags: comma, separated, tags
image: /assets/images/your-image.png
image_credit: Source of the image
-->
```

# Security Notes

*   As this is a static website, the primary security concern is to ensure that no sensitive information is accidentally committed to the repository.
*   When adding new content, make sure it is free from any personal data or credentials.
*   Regularly review the content to prevent any potential security leaks.
