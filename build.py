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
        
        # Add pagination HTML
        pagination_html = '''
        <nav class="pagination-wrapper">
            <ul class="pagination justify-content-center">
        '''
        
        for i in range(total_pages):
            active_class = 'active' if i == page else ''
            pagination_html += f'''
                <li class="page-item {active_class}">
                    <a class="page-link" href="{'index.html' if i == 0 else f'page{i+1}.html'}">{i+1}</a>
                </li>
            '''
        
        pagination_html += '''
            </ul>
        </nav>
        '''
        
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        index_html = template.replace('<!-- CONTENT -->', '\n'.join(posts_html) + pagination_html)
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
    build_search_index(posts_metadata)
    print("Built index.html")

def build_search_index(posts_metadata):
    search_index = []
    for meta in posts_metadata:
        search_index.append({
            'title': meta['title'],
            'description': meta['description'],
            'content': meta['content'],  # You'll need to add content to metadata
            'url': f"posts/{generate_slug(meta['title'])}.html",
            'tags': meta['tags']
        })
    
    with open('search-index.json', 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False)

if __name__ == "__main__":
    build_site()
