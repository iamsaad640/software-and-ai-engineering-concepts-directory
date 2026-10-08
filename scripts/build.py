#!/usr/bin/env python3
"""Generate names-only Markdown and build Material for MkDocs documentation."""
import argparse
from collections import defaultdict
from html import escape
import hashlib
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TRACKS = {'software': 'Software engineering', 'ai': 'LLM applications', 'principal': 'Architecture and technical leadership'}

def load():
    return json.loads((ROOT / 'catalog/directory.json').read_text())

def terms(section):
    return [term for entry in section['entries'] for term in entry['terms']]

def markdown_files(data):
    result = {}
    index = ['# Concepts directory', '', '[Repository home](../README.md) · [Alphabetical index](glossary.md)', '',
             'Pick a topic to explore, or use the alphabetical index to find a specific term.', '']
    glossary = defaultdict(list)
    for track, title in TRACKS.items():
        index += [f'## {title}', '']
        for section in [s for s in data if s['track'] == track]:
            target = f"{track}/{section['slug']}.md"
            index += [f"- [{section['title']}]({target})"]
            lines = [f"# {section['title']}", '', '[Directory](../README.md) · [Alphabetical index](../glossary.md)', '', '## Concepts', '']
            for entry in section['entries']:
                lines += [f"- {'; '.join(entry['terms'])}"]
            lines += ['', '## Further reading', '', 'Reference links for this topic.', '']
            lines += [f'- [{name}]({url})' for name, url in section['references']]
            if section['slug'] == 'loop-engineering':
                lines += ['', '> “Loop engineering” is an emerging umbrella term; the execution mechanisms listed here are the concrete study topics.']
            result[f'docs/{target}'] = '\n'.join(lines) + '\n'
            for term in terms(section):
                glossary[term].append((section['title'],target))
        index += ['']
    result['docs/README.md'] = '\n'.join(index)
    lines = ['# Alphabetical concept index', '', '[Directory](README.md) · [Repository home](../README.md)', '',
             'Find a term and follow its links to the relevant categories.', '']
    current = None
    for term in sorted(glossary, key=str.casefold):
        letter = term[0].upper() if term[0].isalpha() else '#'
        if letter != current:
            lines += [f'## {letter}', '']
            current = letter
        links = ', '.join(f'[{title}]({target})' for title,target in glossary[term])
        lines += [f'- **{term}** — {links}']
    result['docs/glossary.md'] = '\n'.join(lines) + '\n'
    overview = []
    for track, title in TRACKS.items():
        topics = [section for section in data if section['track'] == track]
        overview += ['<details>', f'<summary>Read more: {title} ({len(topics)} topics)</summary>', '']
        overview += [f"- [{section['title']}](docs/{track}/{section['slug']}.md)" for section in topics]
        overview += ['', '</details>', '']
    readme = (ROOT / 'README.md').read_text()
    pattern = r'<!-- directory:start -->.*?<!-- directory:end -->'
    if len(re.findall(pattern, readme, flags=re.S)) != 1:
        raise ValueError('README must have exactly one directory block')
    block = '<!-- directory:start -->\n\n' + '\n'.join(overview) + '<!-- directory:end -->'
    result['README.md'] = re.sub(pattern, lambda match: block, readme, flags=re.S)
    llms = ['# Software & AI Engineering Concepts', '', '> A directory of software systems, LLM application engineering, and technical leadership concepts.', '',
            'Author and maintainer: Saad Ahmed (https://github.com/iamsaad640).',
            'This release lists concept names and reference links. Use the topic pages to locate terminology; they are not full tutorials.', '',
            '## Directory', '', '- [All topics](https://concepts.saad.run/docs/README.md)', '- [Alphabetical index](https://concepts.saad.run/docs/glossary.md)', '']
    for track, title in TRACKS.items():
        llms += [f'## {title}', '']
        llms += [f"- [{section['title']}](https://concepts.saad.run/docs/{track}/{section['slug']}.md)" for section in data if section['track'] == track]
        llms += ['']
    result['llms.txt'] = '\n'.join(llms)
    return result

def build_site(data):
    import yaml
    staging = ROOT / '_docs'
    out = ROOT / '_site'
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()
    for section in data:
        relative = f"{section['track']}/{section['slug']}.md"
        content = (ROOT/'docs'/relative).read_text().replace('[Directory](../README.md)', '[All topics](../topics.md)')
        destination = staging / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content)
    topics = (ROOT/'docs/README.md').read_text().replace('[Repository home](../README.md)', '[Home](index.md)')
    (staging/'topics.md').write_text(topics)
    glossary = (ROOT/'docs/glossary.md').read_text().replace('[Directory](README.md)', '[All topics](topics.md)').replace('[Repository home](../README.md)', '[Home](index.md)')
    (staging/'glossary.md').write_text(glossary)
    unique = len({term.casefold() for section in data for term in terms(section)})
    (staging/'index.md').write_text(f'''# Software & AI Engineering Concepts

Find the concepts behind reliable software and LLM applications.

Browse {len(data)} topics, search for a term, or use the directory to plan what to study next. The current edition lists concept names and reference links.

[Browse all topics](topics.md){{ .md-button .md-button--primary }}
[Find a term A–Z](glossary.md){{ .md-button }}

## Pick a starting point

- **Software systems:** [rate limiting](software/rate-limiting.md), [transactions](software/transactions.md), [distributed systems](software/distributed-systems.md), and [Redis](software/distributed-key-value-stores.md).
- **LLM applications:** [context engineering](ai/context-engineering.md), [RAG](ai/rag-and-retrieval.md), [agent loops](ai/loop-engineering.md), and [evaluations](ai/evaluation.md).
- **Architecture and leadership:** [technical strategy](principal/technical-strategy.md) and [engineering across teams](principal/organizational-engineering.md).

## Take the list with you

<a class="md-button" href="concepts.txt" download="engineering-concepts.txt">Download list (.txt)</a>
<a class="md-button" href="catalog.json" download="engineering-concepts.json">Download JSON</a>

{unique:,} distinct terms. Press **Ctrl+K** or **Cmd+K** to search.

Created and maintained by [Saad Ahmed](https://github.com/iamsaad640). [Suggest a concept](https://github.com/iamsaad640/software-and-ai-engineering-concepts-directory/issues/new/choose) or [contribute on GitHub](https://github.com/iamsaad640/software-and-ai-engineering-concepts-directory/blob/main/CONTRIBUTING.md).
''')
    shutil.copytree(ROOT/'site-assets', staging/'assets', dirs_exist_ok=True)
    config = yaml.safe_load((ROOT/'mkdocs.yml').read_text())
    for key in ('extra_javascript', 'extra_css'):
        fingerprinted = []
        for asset in config.get(key, []):
            source = staging / asset
            digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
            target = source.with_name(f'{source.stem}.{digest}{source.suffix}')
            shutil.copy2(source, target)
            fingerprinted.append(target.relative_to(staging).as_posix())
        config[key] = fingerprinted
    config['nav'] = [{'Home': 'index.md'}, {'All topics': 'topics.md'}]
    for track, title in TRACKS.items():
        config['nav'].append({title: [{section['title']: f"{track}/{section['slug']}.md"} for section in data if section['track'] == track]})
    config['nav'].append({'A–Z index': 'glossary.md'})
    generated_config = ROOT/'_mkdocs.yml'
    generated_config.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True))
    subprocess.run([sys.executable, '-m', 'mkdocs', 'build', '--strict', '--config-file', str(generated_config)], cwd=ROOT, check=True)
    (out/'catalog.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    text_lines = ['Software & AI Engineering Concepts', 'Author: Saad Ahmed', 'https://concepts.saad.run/', '']
    for section in data:
        text_lines += [section['title'], *('- '+term for term in terms(section)), '']
    (out/'concepts.txt').write_text('\n'.join(text_lines)+'\n')
    shutil.copytree(ROOT/'docs', out/'docs', dirs_exist_ok=True)
    shutil.copy2(ROOT/'README.md', out/'README.md')
    shutil.copy2(ROOT/'llms.txt', out/'llms.txt')
    (out/'CNAME').write_text('concepts.saad.run\n')
    (out/'.nojekyll').touch()
    (out/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: https://concepts.saad.run/sitemap.xml\n')

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true',help='Fail when generated Markdown is stale')
    parser.add_argument('--site',action='store_true',help='Also build _site')
    args=parser.parse_args()
    data=load()
    stale=[]
    for name,content in markdown_files(data).items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_text()!=content:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content)
    if stale:
        raise SystemExit('Stale generated files: '+', '.join(stale))
    if args.site:
        build_site(data)
    print(f'Validated generated content: {len(data)} categories')
