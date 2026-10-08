#!/usr/bin/env python3
"""Generate names-only Markdown and static documentation using Python's standard library."""
import argparse
from collections import defaultdict
from html import escape
import json
import re
from pathlib import Path
import shutil

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
    return result

def build_site(data):
    out = ROOT / '_site'
    out.mkdir(exist_ok=True)
    sections, nav = [], []
    for track,title in TRACKS.items():
        nav += [f'<h2>{escape(title)}</h2><ul>']
        for section in [s for s in data if s['track'] == track]:
            ident=f"{track}-{section['slug']}"
            nav += [f'<li><a href="#{ident}">{escape(section["title"])}</a></li>']
            items=''.join(f'<li class="term">{escape(term)}</li>' for term in terms(section))
            sections += [f'<section class="category" id="{ident}" data-track="{track}"><p class="eyebrow">{escape(title)}</p><h2>{escape(section["title"])}</h2><ul class="terms">{items}</ul></section>']
        nav += ['</ul>']
    unique=len({t.casefold() for s in data for t in terms(s)})
    version=(ROOT/'VERSION').read_text().strip()
    document='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Find concepts for databases, distributed systems, architecture, RAG, prompts, and agents.">
<title>Software &amp; AI Engineering Concepts</title><link rel="stylesheet" href="assets/style.css"><script defer src="assets/search.js"></script></head>
<body><a class="skip" href="#main">Skip to concepts</a><header><a class="brand" href="./">Engineering concepts</a><a href="https://github.com/iamsaad640/software-and-ai-engineering-concepts-directory">GitHub</a></header>
<div class="layout"><nav aria-label="Categories">NAV</nav><main id="main"><p class="eyebrow">Software systems · LLM applications</p><h1>Software &amp; AI<br>Engineering Concepts</h1>
<p class="intro">Find what to study next. Browse software systems, LLM applications, and architecture—or search for a specific concept.</p><p class="meta">COUNT distinct terms · CATEGORIES categories · vVERSION</p>
<div class="search"><label for="search">Find a concept</label><input id="search" type="search" placeholder="Redis, sliding window, context engineering…" autocomplete="off"><label for="track">Topic</label><select id="track"><option value="all">All topics</option><option value="software">Software engineering</option><option value="ai">LLM applications</option><option value="principal">Architecture and leadership</option></select><button id="reset" type="button">Clear filters</button></div>
<p id="status" role="status" aria-live="polite"></p><p id="empty" hidden>No matching concepts. Try another term or clear the filters.</p>
CONTENT<footer><a href="catalog.json">Download concept list</a> · <a href="https://github.com/iamsaad640/software-and-ai-engineering-concepts-directory/blob/main/CONTRIBUTING.md">Contribute</a></footer></main></div></body></html>'''
    document=document.replace('NAV',''.join(nav)).replace('CONTENT',''.join(sections)).replace('COUNT',f'{unique:,}').replace('CATEGORIES',str(len(data))).replace('VERSION',version)
    (out/'index.html').write_text(document)
    (out/'catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    (out/'.nojekyll').touch()
    shutil.copytree(ROOT/'site-assets',out/'assets',dirs_exist_ok=True)

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
