import os
import re
from datetime import datetime

def extract_metadata(content):
    metadata = {
        'title': '',
        'description': '',
        'date': '',
        'tags': '',
        'author': 'M Yusuf',
        'image': '',
        'keywords': ''
    }
    
    meta_match = re.search(r'<!--\s*(.*?)\s*-->', content, re.DOTALL)
    if meta_match:
        meta_text = meta_match.group(1)
        for line in meta_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()
    
    return metadata

def generate_slug(title):
    return title.lower().replace(' ', '-').replace(':', '')

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
    final_html = final_html.replace('<!-- CONTENT -->', content.strip())
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    return metadata

def build_index(posts_metadata, template_file, output_file):
    posts_html = []
    for meta in sorted(posts_metadata, key=lambda x: x['date'], reverse=True):
        posts_html.append(f'''
            <article class="post">
                <div class="meta">{meta['date']}</div>
                <h3>
                    <a href="posts/{generate_slug(meta['title'])}.html">{meta['title']}</a>
                </h3>
                <p>{meta['description']}</p>
                <div class="tags">
                    {' '.join(f'<span class="badge bg-light text-dark">#{tag.strip()}</span>' for tag in meta['tags'].split(','))}
                </div>
            </article>
        ''')
    
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    index_html = template.replace('<!-- CONTENT -->', '\n'.join(posts_html))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(index_html)

def build_site():
    # Setup paths
    content_dir = 'posts/content'
    template_dir = 'templates'
    output_dir = 'posts'
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Build all posts and collect metadata
    posts_metadata = []
    for filename in os.listdir(content_dir):
        if filename.endswith('.html'):
            content_path = os.path.join(content_dir, filename)
            template_path = os.path.join(template_dir, 'base.html')
            output_path = os.path.join(output_dir, filename)
            
            metadata = build_page(content_path, template_path, output_path)
            posts_metadata.append(metadata)
            print(f"Built {filename}")
    
    # Build index page
    build_index(
        posts_metadata,
        os.path.join(template_dir, 'base.html'),
        'index.html'
    )
    print("Built index.html")

if __name__ == "__main__":
    build_site()
