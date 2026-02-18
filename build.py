import os
import re
from datetime import datetime
import json

def extract_metadata(content):
    metadata = {
        'title': '',
        'description': '',
        'date': '',
        'tags': '',
        'author': 'M Yusuf',
        'image': '',
        'keywords': '',
        'content': ''  # Add content field
    }
    
    meta_match = re.search(r'<!--\s*(.*?)\s*-->', content, re.DOTALL)
    if meta_match:
        meta_text = meta_match.group(1)
        for line in meta_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()
    
    # Extract content by removing metadata
    metadata['content'] = re.sub(r'<!--\s*(.*?)\s*-->', '', content, flags=re.DOTALL).strip()
    return metadata

def generate_slug(title):
    return title.lower().replace(' ', '-').replace(':', '').replace(',', '').replace('(', '').replace(')', '').replace('*', '')

import html

def escape_code_blocks(content):
    # This regex matches <pre><code> blocks, capturing attributes and content
    # Group 1: <pre ...>
    # Group 2: <code ...> (attributes)
    # Group 3: Content inside code
    # Group 4: </code></pre>
    pattern = r'(<pre[^>]*>\s*)(<code[^>]*>)(.*?)(</code>\s*</pre>)'
    
    def replace_code(match):
        pre_tag = match.group(1)
        code_tag = match.group(2)
        code_content = match.group(3)
        end_tags = match.group(4)
        
        # Convert lang="rust" to class="language-rust" if present
        if 'lang=' in code_tag and 'class=' not in code_tag:
            code_tag = re.sub(r'lang=["\']([^"\']+)["\']', r'class="language-\1"', code_tag)
        elif 'lang=' in code_tag and 'class=' in code_tag:
             # parsing needed if both exist, but simple replacement might be enough
             lang_match = re.search(r'lang=["\']([^"\']+)["\']', code_tag)
             if lang_match:
                 lang = lang_match.group(1)
                 # Append to existing class
                 # Use lambda to access captured group safely in replacement if needed, but \1 works
                 code_tag = re.sub(r'class=["\']([^"\']+)["\']', f'class="language-{lang} \\1"', code_tag)
                 # Remove lang attribute
                 code_tag = re.sub(r'lang=["\']([^"\']+)["\']', '', code_tag)

        # Escape the inner content
        escaped_content = html.escape(code_content)
        
        return f'{pre_tag}{code_tag}{escaped_content}{end_tags}'
    
    return re.sub(pattern, replace_code, content, flags=re.DOTALL | re.IGNORECASE)

def build_page(content_file, template_file, output_file):
    # Read content and extract metadata
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata = extract_metadata(content)
    
    # Read template
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace metadata placeholders
    final_html = template
    for key, value in metadata.items():
        final_html = final_html.replace(f'<!-- {key.upper()} -->', value)
    
    # Remove metadata comment from content
    content = re.sub(r'<!--\s*(.*?)\s*-->', '', content, flags=re.DOTALL)
    
    # Strip redundant article tag, h1, and meta div that might be in the content file
    content = re.sub(r'<article[^>]*>', '', content)
    content = re.sub(r'</article>', '', content)
    content = re.sub(r'<h1>.*?</h1>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="meta[^>]*>.*?</div>', '', content, flags=re.DOTALL)
    
    # Create a nice header for the post
    post_header = f'''
    <header class="mb-8 space-y-4">
        <h1 class="text-4xl font-extrabold tracking-tight lg:text-5xl">{metadata['title']}</h1>
        <div class="flex items-center space-x-2 text-sm text-muted-foreground font-mono">
            <span>Published on {metadata['date']}</span>
            <span>•</span>
            <span>{metadata['author']}</span>
        </div>
    </header>
    '''
    
    # Escape HTML inside code blocks
    content = escape_code_blocks(content.strip())
    
    # Combine header and content
    final_content = post_header + content
    
    final_html = final_html.replace('<!-- CONTENT -->', final_content)

    # Replace image placeholder
    if metadata.get('image'):
        featured_image_html = f'''
        <div class="mb-10 overflow-hidden rounded-xl border bg-muted">
            <img src="{metadata['image']}" alt="{metadata['title']}" class="aspect-video w-full object-cover transition-all hover:scale-105">
            <div class="p-2 text-center text-xs text-muted-foreground italic border-t bg-background">
                Image source: {metadata.get('image_credit', 'Personal collection')}
            </div>
        </div>
        '''
        final_html = final_html.replace('<!-- FEATURED_IMAGE -->', featured_image_html)
    else:
        final_html = final_html.replace('<!-- FEATURED_IMAGE -->', '')
    
    
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    return metadata

def build_index(posts_metadata, template_file, output_file, posts_per_page=40):
    # Sort posts by date
    sorted_posts = sorted(posts_metadata, key=lambda x: x['date'], reverse=True)
    
    # Calculate total pages
    total_posts = len(sorted_posts)
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page
    
    for page in range(total_pages):
        start_idx = page * posts_per_page
        end_idx = start_idx + posts_per_page
        current_posts = sorted_posts[start_idx:end_idx]
        
        posts_html = []
        for meta in current_posts:
            tags_html = ' '.join(f'<span class="inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium bg-secondary text-secondary-foreground">#{tag.strip()}</span>' for tag in meta['tags'].split(','))
            
            posts_html.append(f'''
                <article class="group relative flex flex-col space-y-2 rounded-lg border p-6 hover:bg-muted/50 transition-colors mb-6">
                    <div class="text-xs font-medium text-muted-foreground font-mono">{meta['date']}</div>
                    <h2 class="text-2xl font-bold tracking-tight">
                        <a href="posts/{generate_slug(meta['title'])}.html" class="hover:underline">{meta['title']}</a>
                    </h2>
                    <p class="text-muted-foreground line-clamp-2">{meta['description']}</p>
                    <div class="flex flex-wrap gap-2 pt-2">
                        {tags_html}
                    </div>
                </article>
            ''')
        
        # Add pagination HTML (shadcn style)
        pagination_html = '''
        <nav class="flex items-center justify-center space-x-2 py-8" aria-label="Pagination">
        '''
        
        for i in range(total_pages):
            is_active = i == page
            active_classes = 'bg-primary text-primary-foreground hover:bg-primary/90' if is_active else 'border border-input bg-background hover:bg-accent hover:text-accent-foreground'
            
            pagination_html += f'''
                <a href="{'index.html' if i == 0 else f'page{i+1}.html'}" 
                   class="inline-flex items-center justify-center rounded-md w-10 h-10 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring {active_classes}">
                    {i+1}
                </a>
            '''
        
        pagination_html += '</nav>'
        
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        index_html = template.replace('<!-- CONTENT -->', '<div class="space-y-4">' + '\n'.join(posts_html) + '</div>' + pagination_html)
        index_html = index_html.replace('<!-- TITLE -->', 'Beranda')
        
        # Generate output filename
        output_name = 'index.html' if page == 0 else f'page{page+1}.html'
        output_path = os.path.join(os.path.dirname(output_file), output_name)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(index_html)


def build_site():
    # Setup paths
    content_dir = 'posts/content'
    template_dir = 'templates'
    output_dir = 'posts'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean up old pagination pages in the root directory
    for filename in os.listdir('.'):
        if filename.startswith('page') and filename.endswith('.html'):
            try:
                os.remove(filename)
                print(f"Removed old pagination page: {filename}")
            except Exception as e:
                print(f"Error removing {filename}: {e}")

    # Build all posts and collect metadata
    posts_metadata = []
    generated_files = set()
    
    for filename in sorted(os.listdir(content_dir)):
        if filename.endswith('.html'):
            content_path = os.path.join(content_dir, filename)
            template_path = os.path.join(template_dir, 'base.html')
            
            # Read content to get metadata (specifically title for slug)
            with open(content_path, 'r', encoding='utf-8') as f:
                content = f.read()
            metadata = extract_metadata(content)
            
            slug = generate_slug(metadata['title'])
            output_filename = f"{slug}.html"
            output_path = os.path.join(output_dir, output_filename)
            
            # Build the page
            build_page(content_path, template_path, output_path)
            posts_metadata.append(metadata)
            generated_files.add(output_filename)
            print(f"Built {output_filename} (from {filename})")
    
    # Clean up orphaned files in the output directory (files that were not generated this time)
    for filename in os.listdir(output_dir):
        if filename.endswith('.html') and filename not in generated_files:
            try:
                os.remove(os.path.join(output_dir, filename))
                print(f"Removed orphaned post: {filename}")
            except Exception as e:
                print(f"Error removing {filename}: {e}")

    # Build index page
    build_index(
        posts_metadata,
        os.path.join(template_dir, 'base.html'),
        'index.html'
    )
    build_search_index(posts_metadata)
    print("Built index.html")

    # Build tags page
    build_tags_page(
        posts_metadata,
        os.path.join(template_dir, 'base.html'),
        'tags.html'
    )
    print("Built tags.html")

def build_search_index(posts_metadata):
    search_index = []
    for meta in posts_metadata:
        search_index.append({
            'title': meta['title'],
            'description': meta['description'],
            'content': meta['content'],  # You'll need to add content to metadata
            'url': f"/posts/{generate_slug(meta['title'])}.html",
            'tags': meta['tags']
        })
    
    with open('search-index.json', 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False)

def build_tags_page(posts_metadata, template_file, output_file):
    tags_dict = {}
    total_posts = len(posts_metadata)
    
    # Group and count posts by tags
    for post in posts_metadata:
        for tag in post['tags'].split(','):
            tag = tag.strip()
            if tag not in tags_dict:
                tags_dict[tag] = []
            tags_dict[tag].append(post)
    
    # Generate stats section (shadcn card style)
    stats_html = f'''
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-10">
            <div class="rounded-xl border bg-card text-card-foreground shadow px-6 py-4">
                <div class="text-sm font-medium text-muted-foreground">Total Posts</div>
                <div class="text-2xl font-bold">{total_posts}</div>
            </div>
            <div class="rounded-xl border bg-card text-card-foreground shadow px-6 py-4">
                <div class="text-sm font-medium text-muted-foreground">Total Tags</div>
                <div class="text-2xl font-bold">{len(tags_dict)}</div>
            </div>
        </div>
    '''
    
    # Generate tag cloud HTML
    tag_cloud_html = '<div class="flex flex-wrap gap-2 mb-12">'
    for tag, posts in sorted(tags_dict.items()):
        tag_cloud_html += f'''
            <a href="#tag-{tag}" class="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-colors">
                #{tag} <span class="ml-1 text-muted-foreground text-xs">{len(posts)}</span>
            </a>
        '''
    tag_cloud_html += '</div>'
    
    # Generate post sections by tag
    tags_html = []
    for tag, posts in sorted(tags_dict.items()):
        posts_html = []
        for post in sorted(posts, key=lambda x: x['date'], reverse=True):
            posts_html.append(f'''
                <article class="group border-l-2 border-muted pl-4 py-2 hover:border-primary transition-colors mb-4">
                    <div class="text-xs font-mono text-muted-foreground">{post['date']}</div>
                    <h3 class="text-lg font-semibold"><a href="posts/{generate_slug(post['title'])}.html" class="hover:underline">{post['title']}</a></h3>
                </article>
            ''')
        
        tags_html.append(f'''
            <section id="tag-{tag}" class="mb-12 scroll-mt-20">
                <h2 class="text-2xl font-bold mb-6 flex items-center gap-2">
                    <span class="text-primary">#</span>{tag}
                </h2>
                <div class="space-y-2">
                    {''.join(posts_html)}
                </div>
            </section>
        ''')
    
    # Combine all content sections
    final_content = stats_html + tag_cloud_html + '\n'.join(tags_html)
    
    # Read template and create page
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace content and title
    tags_page = template.replace('<!-- CONTENT -->', final_content)
    tags_page = tags_page.replace('<!-- TITLE -->', 'Tags')
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(tags_page)

if __name__ == "__main__":
    build_site()
