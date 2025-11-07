#!/usr/bin/env python3
"""
Analyze a markdown knowledge repository to inform skill design.

Usage:
  python analyze_knowledge_repo.py <repo-path> [--output <report-path>]

Output:
  - Content structure analysis
  - Topic clustering
  - Linking pattern analysis
  - Token usage estimates
  - Recommended skill configuration

Examples:
  python analyze_knowledge_repo.py ~/docs/dao-frameworks
  python analyze_knowledge_repo.py ./knowledge-garden --output ./analysis.md
"""

import argparse
import os
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter
import yaml


def analyze_repository(repo_path):
    """Analyze markdown repository structure and content."""

    repo_path = Path(repo_path)
    if not repo_path.exists():
        print(f"Error: Repository path {repo_path} does not exist")
        return None

    analysis = {
        'path': str(repo_path),
        'files': [],
        'total_files': 0,
        'total_size': 0,
        'frontmatter_fields': Counter(),
        'tags': Counter(),
        'wikilinks': [],
        'backlinks': defaultdict(list),
        'file_structure': {},
        'topics': [],
        'estimated_tokens': 0
    }

    # Scan all markdown files
    md_files = list(repo_path.glob('**/*.md'))
    analysis['total_files'] = len(md_files)

    for md_file in md_files:
        file_info = analyze_file(md_file, repo_path)
        analysis['files'].append(file_info)
        analysis['total_size'] += file_info['size']
        analysis['estimated_tokens'] += file_info['estimated_tokens']

        # Aggregate frontmatter fields
        for field in file_info['frontmatter'].keys():
            analysis['frontmatter_fields'][field] += 1

        # Aggregate tags
        for tag in file_info['tags']:
            analysis['tags'][tag] += 1

        # Aggregate wikilinks
        analysis['wikilinks'].extend(file_info['wikilinks'])

        # Build backlink map
        for link in file_info['wikilinks']:
            analysis['backlinks'][link].append(file_info['relative_path'])

    # Analyze structure
    analysis['file_structure'] = build_directory_tree(md_files, repo_path)

    # Identify topics (from directory names and common tags)
    analysis['topics'] = identify_topics(analysis)

    return analysis


def analyze_file(file_path, repo_root):
    """Analyze a single markdown file."""

    content = file_path.read_text(encoding='utf-8', errors='ignore')

    file_info = {
        'path': str(file_path),
        'relative_path': str(file_path.relative_to(repo_root)),
        'size': len(content),
        'estimated_tokens': len(content.split()) * 1.3,  # Rough estimate
        'frontmatter': {},
        'tags': [],
        'wikilinks': [],
        'headings': [],
        'has_code_blocks': False
    }

    # Parse frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if frontmatter_match:
        try:
            file_info['frontmatter'] = yaml.safe_load(frontmatter_match.group(1)) or {}
        except yaml.YAMLError:
            file_info['frontmatter'] = {}

    # Extract tags from frontmatter
    if 'tags' in file_info['frontmatter']:
        tags = file_info['frontmatter']['tags']
        if isinstance(tags, list):
            file_info['tags'].extend(tags)
        elif isinstance(tags, str):
            file_info['tags'].append(tags)

    # Extract hashtags from content
    hashtags = re.findall(r'#(\w+)', content)
    file_info['tags'].extend(hashtags)

    # Extract wikilinks
    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
    file_info['wikilinks'] = wikilinks

    # Extract headings
    headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
    file_info['headings'] = headings

    # Check for code blocks
    file_info['has_code_blocks'] = bool(re.search(r'```', content))

    return file_info


def build_directory_tree(files, repo_root):
    """Build a tree structure of directories and file counts."""

    tree = defaultdict(int)
    for file_path in files:
        relative = file_path.relative_to(repo_root)
        if len(relative.parts) > 1:
            directory = str(relative.parent)
            tree[directory] += 1
        else:
            tree['root'] += 1

    return dict(tree)


def identify_topics(analysis):
    """Identify main topics from directory names and common tags."""

    topics = []

    # Topics from directory names
    for directory in analysis['file_structure'].keys():
        if directory != 'root':
            topics.append(directory.split('/')[0])

    # Topics from most common tags
    for tag, count in analysis['tags'].most_common(10):
        if tag not in topics:
            topics.append(tag)

    return list(set(topics))


def estimate_loading_strategy(analysis):
    """Recommend loading strategy based on repository size."""

    total_tokens = analysis['estimated_tokens']
    file_count = analysis['total_files']

    if total_tokens < 5000 and file_count < 10:
        return 'always', 'Small knowledge base - can load most content'
    elif total_tokens < 20000 and file_count < 50:
        return 'selective', 'Medium knowledge base - use keyword or topic-based triggers'
    else:
        return 'on-demand', 'Large knowledge base - load only when explicitly needed'


def generate_report(analysis, output_path=None):
    """Generate analysis report in markdown format."""

    loading_strategy, strategy_note = estimate_loading_strategy(analysis)

    report = f"""# Knowledge Repository Analysis

**Repository**: `{analysis['path']}`
**Analysis Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}

## Summary

- **Total Files**: {analysis['total_files']} markdown documents
- **Total Size**: {analysis['total_size']:,} bytes
- **Estimated Tokens**: ~{int(analysis['estimated_tokens']):,} tokens
- **Topics Identified**: {len(analysis['topics'])}
- **Unique Tags**: {len(analysis['tags'])}
- **Wikilinks Found**: {len(analysis['wikilinks'])}

## Repository Structure

### Directory Organization

"""

    for directory, count in sorted(analysis['file_structure'].items()):
        report += f"- `{directory}`: {count} files\n"

    report += f"""

### Main Topics

Based on directory names and common tags:

"""

    for topic in analysis['topics'][:10]:
        report += f"- {topic}\n"

    report += f"""

## Content Patterns

### Frontmatter Usage

"""

    if analysis['frontmatter_fields']:
        report += "Common frontmatter fields:\n\n"
        for field, count in analysis['frontmatter_fields'].most_common(10):
            percentage = (count / analysis['total_files']) * 100
            report += f"- `{field}`: {count} files ({percentage:.0f}%)\n"
    else:
        report += "No YAML frontmatter detected\n"

    report += f"""

### Tag Distribution

"""

    if analysis['tags']:
        report += "Most common tags:\n\n"
        for tag, count in analysis['tags'].most_common(10):
            report += f"- `#{tag}`: {count} occurrences\n"
    else:
        report += "No tags detected\n"

    report += f"""

### Linking Patterns

"""

    wikilink_count = len(analysis['wikilinks'])
    if wikilink_count > 0:
        report += f"- **Total wikilinks**: {wikilink_count}\n"
        report += f"- **Average per file**: {wikilink_count / analysis['total_files']:.1f}\n"

        # Most linked-to pages
        if analysis['backlinks']:
            report += "\nMost referenced pages:\n\n"
            sorted_backlinks = sorted(analysis['backlinks'].items(), key=lambda x: len(x[1]), reverse=True)
            for page, references in sorted_backlinks[:5]:
                report += f"- `{page}`: {len(references)} references\n"
    else:
        report += "No wikilinks detected\n"

    report += f"""

## Recommended Skill Configuration

### Skill Type

"""

    # Recommend skill type based on content
    if 'template' in str(analysis['tags']).lower() or 'framework' in str(analysis['tags']).lower():
        skill_type = 'framework-guidance'
        report += f"**Recommended**: `{skill_type}`\n\n"
        report += "Repository appears to contain frameworks or templates. Consider creating a framework-guidance skill.\n"
    else:
        skill_type = 'knowledge-retrieval'
        report += f"**Recommended**: `{skill_type}`\n\n"
        report += "Repository appears to be general knowledge content. Consider creating a knowledge-retrieval skill.\n"

    report += f"""

### Loading Strategy

**Recommended**: `{loading_strategy}`

{strategy_note}

"""

    if loading_strategy == 'selective':
        report += "\nSuggested trigger keywords:\n\n"
        for topic in analysis['topics'][:5]:
            report += f"- {topic}\n"

    report += f"""

### Token Budget Estimates

Based on repository size and structure:

| Operation | Estimated Tokens | Notes |
|-----------|------------------|-------|
| Skill metadata | ~100 | Name + description |
| SKILL.md body | ~2000-2500 | Core capabilities and patterns |
| Quick reference | ~500-1000 | Common patterns extracted |
| Single doc lookup | ~{int(analysis['estimated_tokens'] / analysis['total_files']):.0f} | Average per file |
| Multi-doc synthesis | ~{int(analysis['estimated_tokens'] / analysis['total_files'] * 3):.0f} | 3 files combined |
| Full knowledge base | ~{int(analysis['estimated_tokens']):,} | All content (use on-demand) |

### Suggested Structure

```
skill-name/
├── SKILL.md
├── scripts/
├── references/
│   ├── quick-reference.md      # Top patterns/concepts (~500-1000 tokens)
"""

    for topic in analysis['topics'][:3]:
        report += f"│   ├── {topic.lower().replace(' ', '-')}.md\n"

    report += """└── assets/
    └── templates/              # If framework-guidance type
```

### Next Steps

1. Run `init_knowledge_skill.py` with `--type {skill_type}` template
2. Copy key documents to `references/` directory
3. Create quick-reference guide with most common patterns
4. Configure loading triggers based on suggested keywords
5. Test with representative queries
6. Validate and package

## Sample Skill Configuration

```yaml
---
name: [your-skill-name]
description: [Brief description mentioning {', '.join(analysis['topics'][:3])}. Use when users ask about {analysis['topics'][0] if analysis['topics'] else 'relevant topics'}.]
---
```

## Analysis Details

### Individual Files

Top 10 largest files by estimated token count:

"""

    sorted_files = sorted(analysis['files'], key=lambda x: x['estimated_tokens'], reverse=True)
    for i, file_info in enumerate(sorted_files[:10], 1):
        report += f"{i}. `{file_info['relative_path']}`: ~{int(file_info['estimated_tokens']):,} tokens\n"

    if output_path:
        Path(output_path).write_text(report)
        print(f"Analysis report written to: {output_path}")
    else:
        print(report)

    return report


def main():
    parser = argparse.ArgumentParser(
        description='Analyze markdown knowledge repository to inform skill design',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('repo_path', help='Path to markdown knowledge repository')
    parser.add_argument('--output', '-o', help='Output path for analysis report (markdown file)')

    args = parser.parse_args()

    analysis = analyze_repository(args.repo_path)
    if analysis:
        generate_report(analysis, args.output)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
