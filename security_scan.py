import os
import re
import sys
import html

# High-risk patterns for a backend developer's blog
PATTERNS = {
    "Generic API Key": r'(?i)(api[_-]?key|secret|token|auth|password)["\s:][\s=]{1,3}["\']?([a-zA-Z0-9\-_]{16,})["\']?',
    "AWS Access Key": r'AKIA[0-9A-Z]{16}',
    "AWS Secret Key": r'(?i)aws[_-]?secret[_-]?access[_-]?key["\s:][\s=]{1,3}["\']?([a-zA-Z0-9/+=]{40})["\']?',
    "GitHub Personal Access Token": r'ghp_[a-zA-Z0-9]{36}',
    "Stripe Secret Key": r'sk_live_[0-9a-zA-Z]{24}',
    "Slack Webhook": r'https://hooks.slack.com/services/T[a-zA-Z0-9_]+/B[a-zA-Z0-9_]+/[a-zA-Z0-9_]+',
    "Private SSH Key": r'-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----',
    "Local Path Leak": r'/Users/[a-zA-Z0-9.-]+/',
    "Internal IP Leak": r'192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}',
    "Env File Leak": r'\.env\s*=',
}

def scan_file(file_path):
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for patterns
            for name, pattern in PATTERNS.items():
                matches = re.finditer(pattern, content)
                for match in matches:
                    # Capture context
                    start = max(0, match.start() - 20)
                    end = min(len(content), match.end() + 20)
                    context = content[start:end].replace('\n', ' ')
                    issues.append({
                        "type": name,
                        "line": content.count('\n', 0, match.start()) + 1,
                        "match": match.group(0),
                        "context": f"...{context}..."
                    })
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return issues

def main():
    target_dirs = ['posts', '.']
    found_any = False
    
    print("🚀 Starting Security Scan of generated HTML files...\n")
    
    for directory in target_dirs:
        if not os.path.exists(directory):
            continue
            
        for root, _, files in os.walk(directory):
            if 'content' in root: continue
                
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    issues = scan_file(file_path)
                    
                    if issues:
                        found_any = True
                        print(f"⚠️ Found {len(issues)} issue(s) in: {file_path}")
                        for issue in issues:
                            print(f"   [{issue['type']}] Line {issue['line']}: {issue['context']}")
                            m = issue['match']
                            masked = m[:4] + "*" * (len(m) - 8) + m[-4:] if len(m) > 8 else "****"
                            print(f"   Match: {masked}\n")

    if not found_any:
        print("✅ No sensitive keys or leaks found in generated HTML.")
        sys.exit(0)
    else:
        print("❌ Scan completed with findings.")
        sys.exit(1)

if __name__ == "__main__":
    main()
